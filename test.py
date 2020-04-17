import argparse
from core.pipelines.pipelines_controller import get_pipelines_ids_list

parser = argparse.ArgumentParser(description='A tool to generate a 3-D model from an imaging study')
parser.add_argument('pipeline', metavar='P', type=str,  choices=get_pipelines_ids_list(),
                    help='Segmentation pipeline options include {} '.format(', '.join(get_pipelines_ids_list())))
parser.add_argument('input', metavar='i', type=str, nargs='+',
                    help='Specify a single directory or mulitple directories containing scans in the form of NIfTI or DICOM')
parser.add_argument('ouput', metavar='o', type=str,
                    help='Specify a single output file in the form of a glb file')

parser.add_argument('-type', metavar='m', nargs='+', default=1,
                    help='Specify the segmentation types')

args = parser.parse_args()
print(args.accumulate(args.integers))