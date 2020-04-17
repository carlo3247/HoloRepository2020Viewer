import argparse
from argparse import RawTextHelpFormatter
from core.pipelines.lung_segmentation import run
from core.pipelines.pipelines_controller import get_pipeline_description
from models.model_controller import (get_seg_types,
                                     get_file_types, get_proc_seg_types)


pipeline_description = get_pipeline_description('lung_segmentation')

model_seg_types = get_seg_types('lung_segmentation')
model_proc_seg_types = get_proc_seg_types('lung_segmentation')
model_file_types = get_file_types('lung_segmentation')


parser = argparse.ArgumentParser(description=pipeline_description+'\n' +
                                 'Input file must be of type ' + ', '.join(model_file_types) +
                                 '\nDefault segmentaion: lung ',
                                 formatter_class=RawTextHelpFormatter)

parser.add_argument('input', metavar='i', type=str,
                    help='Specify the path to the directory containing the input scans')
parser.add_argument('output', metavar='o', type=str,
                    help='Specify the path of a single output file in the form of a glb file')
parser.add_argument('-type', metavar='t', type=int, default=1, choices=range(0, len(model_seg_types)),
                    help="Specify the type of lung segmentation through an integer"+'\n'+'Segmentation types include ' + model_proc_seg_types)

args = parser.parse_args()

input_dir = args.input
output_path = args.output
segment_type = args.type

run(input_dir, output_path, segment_type)
