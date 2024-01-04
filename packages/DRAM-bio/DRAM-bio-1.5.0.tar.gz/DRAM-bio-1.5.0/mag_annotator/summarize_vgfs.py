"""DRAM-v distillation functions"""
import re
from os import path, mkdir
from functools import partial
from collections import defaultdict, Counter
from datetime import datetime
import warnings
import logging

import pandas as pd
import altair as alt

from mag_annotator.database_handler import DatabaseHandler
from mag_annotator.utils import setup_logger
from mag_annotator.summarize_genomes import get_ids_from_annotations_by_row, \
    get_ids_from_annotations_all, get_ordered_uniques, check_columns

VOGDB_TYPE_NAMES = {'Xr': 'Viral replication genes', 'Xs': 'Viral structure genes',
                    'Xh': 'Viral genes with host benefits', 'Xp': 'Viral genes with viral benefits',
                    'Xu': 'Viral genes with unknown function', 'Xx': 'Viral hypothetical genes'}
VIRUS_STATS_COLUMNS = ['VIRSorter category', 'Circular', 'Prophage', 'Gene count', 'Strand switches',
                       'potential AMG count', 'Transposase present', 'Possible Non-Viral Contig']
VIRAL_DISTILLATE_COLUMNS = ['gene', 'scaffold', 'gene_id', 'gene_description', 'category', 'header',
                            'subheader', 'module', 'auxiliary_score', 'amg_flags']
VIRAL_LIQUOR_HEADERS = ['Category', 'Function', 'AMG Genes', 'Genes Present', 'Contig Name', 'Present in Contig']
HEATMAP_CELL_HEIGHT = 10
HEATMAP_CELL_WIDTH = 10

defaultdict_list = partial(defaultdict, list)


def add_custom_ms(annotations, distillate_form):
    metabolic_genes = set(distillate_form.index)

    new_amg_flags = list()
    for gene, row in annotations.iterrows():
        if 'M' in row['amg_flags']:
            new_amg_flags.append(row['amg_flags'])
        else:
            gene_annotations = set(get_ids_from_annotations_all(pd.DataFrame(row).transpose()).keys())
            if len(metabolic_genes & gene_annotations) > 0:
                new_amg_flags.append(row['amg_flags'] + 'M')
            else:
                new_amg_flags.append(row['amg_flags'])
    return new_amg_flags


def filter_to_amgs(annotations, max_aux=4, remove_transposons=True, remove_fs=False):
    amgs = annotations[((annotations['amg_flags'].str.contains('M')) &
                          (annotations['amg_flags'].str.contains('V') == False) &
                          (annotations['amg_flags'].str.contains('A') == False) &
                          (annotations['amg_flags'].str.contains('P') == False) &
                          (annotations['auxiliary_score'] <= max_aux)
                           )]
    if remove_transposons:
        amgs = amgs[(amgs['amg_flags'].str.contains('T') == False)]
    if remove_fs:
        amgs = amgs[(amgs['amg_flags'].str.contains('F') == False)]
    return amgs


def get_strand_switches(strandedness):
    switches = 0
    strand = strandedness[0]
    for i in range(len(strandedness)):
        if strandedness[i] != strand:
            switches += 1
            strand = strandedness[i]
    return switches


def make_viral_stats_table(annotations, potential_amgs, groupby_column='scaffold'):
    amg_counts = potential_amgs.groupby(groupby_column).size()
    viral_stats_series = list()
    for scaffold, frame in annotations.groupby(groupby_column):
        # get virus information
        virus_categories = re.findall(r'-cat_\d$', scaffold)
        if len(virus_categories) > 0:
            virus_category = int(virus_categories[0].split('_')[-1])  # viral category
            virus_prophage = virus_category in [4, 5]  # virus is prophage
        else:
            virus_category = None
            virus_prophage = None
        virus_circular = len(re.findall(r'-circular-cat_\d$', scaffold)) == 1  # virus is circular
        virus_num_genes = len(frame)  # number of genes on viral contig
        virus_strand_switches = get_strand_switches(frame.strandedness)  # number of strand switches
        if scaffold in amg_counts:
            virus_number_amgs = amg_counts[scaffold]  # number of potential amgs
        else:
            virus_number_amgs = 0
        virus_transposase_present = sum(frame.is_transposon) > 0  # transposase on contig
        # virus_j_present = sum(['J' in i if not pd.isna(i) else False for i in frame.amg_flags]) > 0
        virus_j_present = sum([i == 'Xh' if not pd.isna(i) else False
                               for i in frame['vogdb_categories']]) / frame.shape[0]
        virus_data = pd.Series([virus_category, virus_circular, virus_prophage, virus_num_genes, virus_strand_switches,
                                virus_number_amgs, virus_transposase_present, virus_j_present],
                               index=VIRUS_STATS_COLUMNS, name=scaffold)
        # get vogdb categories
        # when vogdb has multiple categories only the first is taken
        gene_counts = Counter([i.split(';')[0] for i in frame.vogdb_categories.replace('', 'Xx')])
        named_gene_counts = {VOGDB_TYPE_NAMES[key]: value for key, value in gene_counts.items()}
        gene_counts_series = pd.Series(named_gene_counts, name=scaffold)
        viral_stats_series.append(pd.concat([virus_data, gene_counts_series]))
    return pd.DataFrame(viral_stats_series).fillna(0)


def make_viral_distillate(potential_amgs, genome_summary_form, amg_database, logger):
    """Make a summary of what in our database makes something a AMG or likly AMG to dram"""
    # Transform the amg database to make it more workable
    def look_up_metabolic_info(search_db, match_db, match_db_name):
        id_genes = set(match_db.index)
        return (
            (search_db
             .assign(gene_id = lambda x: x['ids'].apply(lambda y: y & id_genes))
             )[['gene_id', 'scaffold', 'auxiliary_score', 'amg_flags']]
            .explode('gene_id')
            .dropna(subset=['gene_id'])
            .merge(match_db, how='left', left_on='gene_id', right_index=True)
            .assign(gene_id_origin=match_db_name))

    amg_database_frame = (amg_database
                          .melt(value_vars=['KO', 'EC', 'PFAM'],
                                id_vars=['gene', 'module', 'metabolism',
                                         'reference', 'verified'],
                                value_name='gene_id')
                          .drop('variable', axis=1)
                          .assign(
                              gene_id=lambda x: x['gene_id'].apply(
                                  lambda y: [i.strip() for i in str(y).split(';')]))
                          .explode('gene_id')
                          .dropna(subset='gene_id')
                          .set_index('gene_id')
                          .rename(columns = {'gene': 'gene_description'})
                          )
    potential_amgs = potential_amgs.assign(ids=get_ids_from_annotations_by_row(potential_amgs))
    metabolic_df = look_up_metabolic_info(potential_amgs, genome_summary_form, 'genome_summary_form')
    amg_df = look_up_metabolic_info(potential_amgs, amg_database_frame, 'amg_database')
    missing = list(set(potential_amgs.index) - (set(metabolic_df.index) | (set(amg_df.index)) ))
    # evaluate what is mising
    logger.warning(f"No distillate information found for {len(missing)} genes.")
    logger.debug('\n'.join(missing))


    summary = pd.concat([
        metabolic_df,
        amg_df,
        potential_amgs.loc[missing, ['scaffold', 'auxiliary_score', 'amg_flags']]])
    summary.reset_index(inplace=True, drop=False, names='gene')
    return summary


def make_vgf_order(amgs):
    amg_score_dict = {scaffold: ((1/frame['auxiliary_score']).sum(), len(frame))
                      for scaffold, frame in amgs.groupby('scaffold')}
    amg_scores = pd.DataFrame.from_dict(amg_score_dict, columns=['AMG_score', 'AMG_count'],
                                        orient='index')
    return list(amg_scores.sort_values(['AMG_score', 'AMG_count'], ascending=False).index)


def make_amg_count_column(potential_amgs, vgf_order=None):
    # build count column
    amg_counts = pd.DataFrame(Counter(potential_amgs.scaffold).items(), columns=['Contig Name', 'Number'])
    amg_counts['AMG Count'] = 'AMG Count'
    text = alt.Chart(amg_counts, width=HEATMAP_CELL_WIDTH+10, height=HEATMAP_CELL_HEIGHT*len(amg_counts)).encode(
                     x=alt.X('AMG Count', title=None, axis=alt.Axis(labelLimit=0, labelAngle=90)),
                     y=alt.Y('Contig Name', title=None, axis=alt.Axis(labelLimit=0), sort=vgf_order),
                     text='Number'
                    ).mark_text()
    return text


def make_viral_functional_df(annotations, genome_summary_form, groupby_column='scaffold'):
    # build dict of ids per genome
    vgf_to_id_dict = defaultdict(defaultdict_list)
    for vgf, frame in annotations.groupby(groupby_column, sort=False):
        for gene, id_list in get_ids_from_annotations_by_row(frame).items():
            for id_ in id_list:
                vgf_to_id_dict[vgf][id_].append(gene)
    # build long from data frame
    rows = list()
    for category, category_frame in genome_summary_form.groupby('sheet'):
        for header, header_frame in category_frame.groupby('module'):
            header_id_set = set(header_frame.index.to_list())
            curr_rows = list()
            for vgf, id_dict in vgf_to_id_dict.items():
                present_in_bin = False
                functions_present = list()
                amgs_present = list()
                for id_, amgs in id_dict.items():
                    if id_ in header_id_set:
                        present_in_bin = True
                        functions_present.append(id_)
                        amgs_present += amgs
                curr_rows.append([category, header, ', '.join(amgs_present), ', '.join(functions_present), vgf,
                                  present_in_bin])
            if sum([i[-1] for i in curr_rows]) > 0:
                rows += curr_rows
    return pd.DataFrame(rows, columns=VIRAL_LIQUOR_HEADERS)


def make_viral_functional_heatmap(functional_df, vgf_order=None):
    # build heatmaps
    charts = list()
    for i, (group, frame) in enumerate(functional_df.groupby('Category', sort=False)):
        # set variables for chart
        function_order = get_ordered_uniques(list(frame['Function']))
        num_vgfs_in_frame = len(set(frame['Contig Name']))
        chart_width = HEATMAP_CELL_WIDTH * len(function_order)
        chart_height = HEATMAP_CELL_HEIGHT * num_vgfs_in_frame
        # set up colors for chart
        rect_colors = alt.Color('Present in Contig',
                                legend=alt.Legend(symbolType='square', values=[True, False]),
                                sort=[True, False],
                                scale=alt.Scale(range=['#e5f5f9', '#2ca25f']))
        # define chart
        # TODO: Figure out how to angle title to take up less space
        c = alt.Chart(frame, title=alt.TitleParams(group)).encode(
            x=alt.X('Function', title=None, axis=alt.Axis(labelLimit=0, labelAngle=90), sort=function_order),
            y=alt.Y('Contig Name', axis=alt.Axis(title=None, labels=False, ticks=False), sort=vgf_order),
            tooltip=[alt.Tooltip('Contig Name'),
                     alt.Tooltip('Category'),
                     alt.Tooltip('Function'),
                     alt.Tooltip('AMG Genes'),
                     alt.Tooltip('Genes Present')]
        ).mark_rect().encode(color=rect_colors).properties(
            width=chart_width,
            height=chart_height)
        charts.append(c)
    # merge and return
    function_heatmap = alt.hconcat(*charts, spacing=5)
    return function_heatmap


def summarize_vgfs(input_file, output_dir, groupby_column='scaffold', max_auxiliary_score=3,
                   remove_transposons=False, remove_fs=False, custom_distillate=None,
                   log_file_path:str=None, config_loc=None):
    # make output folder
    mkdir(output_dir)
    if log_file_path is None:
        log_file_path = path.join(output_dir, "distill.log")
    logger = logging.getLogger('distillation_log')
    setup_logger(logger, log_file_path)
    logger.info(f"The log file is created at {log_file_path}")


    # set up
    annotations = pd.read_csv(input_file, sep='\t', index_col=0).fillna('')
    database_handler = DatabaseHandler(logger, config_loc=config_loc)
    if database_handler.config["dram_sheets"].get('genome_summary_form') is None:
        raise ValueError('Genome summary form location must be set in order to summarize genomes')
    genome_summary_form = pd.read_csv(database_handler.config['dram_sheets']['genome_summary_form'], sep='\t', index_col=0)
    if custom_distillate is not None:
        custom_distillate_form = pd.read_csv(custom_distillate, sep='\t', index_col=0)
        genome_summary_form = pd.concat([genome_summary_form, custom_distillate_form])
        # add M's from custom distillate
        annotations['amg_flags'] = add_custom_ms(annotations, custom_distillate_form)
    logger.info('Retrieved database locations and descriptions')

    # get potential AMGs
    potential_amgs = filter_to_amgs(annotations, max_aux=max_auxiliary_score,
                                    remove_transposons=remove_transposons, remove_fs=remove_fs)
    check_columns(potential_amgs, logger)
    logger.info('Determined potential amgs')

    # make distillate
    viral_genome_stats = make_viral_stats_table(annotations, potential_amgs, groupby_column)
    viral_genome_stats.to_csv(path.join(output_dir, 'vMAG_stats.tsv'), sep='\t')
    logger.info('Calculated viral genome statistics')

    viral_distillate = make_viral_distillate(
        potential_amgs,
        genome_summary_form,
        pd.read_csv(database_handler.config["dram_sheets"].get('amg_database'), sep='\t'),
        logger)
    viral_distillate.to_csv(path.join(output_dir, 'amg_summary.tsv'), sep='\t', index=None)
    logger.info('Generated AMG summary')

    # make liquor
    vgf_order = make_vgf_order(potential_amgs)
    amg_column = make_amg_count_column(potential_amgs, vgf_order)
    viral_function_df = make_viral_functional_df(potential_amgs, genome_summary_form, groupby_column=groupby_column)
    viral_functional_heatmap = make_viral_functional_heatmap(viral_function_df, vgf_order)
    product = alt.hconcat(amg_column, viral_functional_heatmap, spacing=5)
    product.save(path.join(output_dir, 'product.html'))
    logger.info('Generated product heatmap')
    logger.info("Completed distillation")
