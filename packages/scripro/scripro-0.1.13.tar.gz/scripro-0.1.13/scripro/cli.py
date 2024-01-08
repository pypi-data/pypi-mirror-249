import argparse
from .supercell import *
from .utils import *
import sys
from numpy import require


def run_enrich(args):
    feature_matrix_path = args.feature_matrix
    num = args.cell_num
    species = args.species
    #project = args.project
    min_cell = args.min_cells  # for removing few features cells
    #min_peaks = args.min_peaks  # for removing few cells features
    #max_peaks = args.max_peaks  # for removing doublet cells
    n_cores = args.n_cores

    print_log('Reading Files, Please wait ...')
    if feature_matrix_path.endswith('.h5'):
        feature_matrix = sc.read_10x_h5(feature_matrix_path, gex_only=False)
    elif feature_matrix_path.endswith('.h5ad'):
        feature_matrix = sc.read_h5ad(feature_matrix_path)
    else:
        feature_matrix = sc.read_10x_mtx(feature_matrix_path)
    feature_matrix.var_names_make_unique()
    
    sc.pp.filter_genes(feature_matrix, min_cells=min_cell)
    sc.pp.normalize_total(feature_matrix, target_sum=1e4)
    sc.pp.log1p(feature_matrix)
    sc.pp.highly_variable_genes(feature_matrix,n_top_genes=3000)
    feature_matrix.raw = feature_matrix
    feature_matrix = feature_matrix[:, feature_matrix.var.highly_variable]
    #sc.pp.regress_out(self.adata, ['total_counts', 'pct_counts_mt'])
    sc.pp.scale(feature_matrix, max_value=10)
    sc.tl.pca(feature_matrix,svd_solver='arpack')
    sc.pp.neighbors(feature_matrix, n_neighbors=10, n_pcs=40)
    sc.tl.umap(feature_matrix)
    sc.tl.leiden(feature_matrix,resolution=0.6)
    
    test_data = scripro.Ori_Data(feature_matrix,Cell_num=num)
    test_data.get_positive_marker_gene_parallel(cores=n_cores)
    rna_seq_data = scripro.SCRIPro_RNA(n_cores,species,test_data,assays=['Direct','DNase','H3K27ac'])
    rna_seq_data.cal_ISD_cistrome()
    rna_seq_data.get_P_value_matrix()
    rna_seq_data.get_chip_matrix()
    rna_seq_data.P_value_matrix
    rna_seq_data.get_tf()
    rna_seq_data.tf_score.to_csv('output.csv', index=False, sep=',')
    return 


def main():
    argparser = prepare_argparser()
    args = argparser.parse_args()
    subcommand  = args.subcommand
    if subcommand == "enrich":
        try:
            run_enrich(args)
        except MemoryError:
            sys.exit( "MemoryError occurred.")
    elif subcommand == "format":
        pass

    return

def prepare_argparser():
    description = "%(prog)s"
    epilog = "For command line options of each command, type: %(prog)s COMMAND -h"
    argparser = argparse.ArgumentParser( description = description, epilog = epilog )
    argparser.add_argument( "--version", action="version", version="0.1.6")
    subparsers = argparser.add_subparsers( dest = 'subcommand' )
    subparsers.required = True
    add_enrich_parser(subparsers)
    return argparser


def add_enrich_parser( subparsers ):
    """Add main function 'enrich' argument parsers.
    """
    argparser_enrich = subparsers.add_parser("enrich", help="Main function.")

    # group for input files
    group_input = argparser_enrich.add_argument_group( "Input files arguments" )
    group_input.add_argument( "-i", "--input_feature_matrix", dest = "feature_matrix", type = str, required = True,
                              help = 'A cell by peak matrix . REQUIRED.' )
    group_input.add_argument( "-n", "--cell_number", dest = "cell_num", type = int, required = True,
                              help = 'Supercell Cell Number . REQUIRED.' )
    group_input.add_argument( "-s", "--species", dest = "species", choices= ['hs', 'mm'], required = True,
                              help = 'Species. "hs"(human) or "mm"(mouse). REQUIRED.' )
    # group for output files
    '''
    group_output = argparser_enrich.add_argument_group( "Output arguments" )
    group_output.add_argument( "-p", "--project", dest = "project", type = str, default = "" ,
                               help = 'Project name, which will be used to generate output files folder. DEFAULT: Random generate.')
    '''
    # group for preprocessing
    group_preprocessing = argparser_enrich.add_argument_group( "Preprocessing paramater arguments" )
    group_preprocessing.add_argument( "--min_cells", dest = "min_cells", type = str, default = 'auto',
                                      help='Minimal cell cutoff for features. Auto will take 0.05%% of total cell number.DEFAULT: "auto".')
    group_other = argparser_enrich.add_argument_group( "Other options" )
    group_other.add_argument( "-t", '--thread', dest='n_cores', type = int, default = 8,
                              help="Number of cores use to run SCRIP. DEFAULT: 16.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupted!\n")
        sys.exit(0)