import argparse
from argparse import RawTextHelpFormatter
import json
from core.pipelines.kidney_segmentation import run

from core.pipelines.pipelines_controller import get_pipeline_description

from models.model_controller import (get_seg_types, 
get_file_types, get_proc_seg_types)


pipelineDescription = get_pipeline_description('kidney_segmentation')

modelSegTypes = get_seg_types('kidney_segmentation')
modelProcSegTypes = get_proc_seg_types('kidney_segmentation')
modelFileTypes = get_file_types('kidney_segmentation')


parser = argparse.ArgumentParser(description=pipelineDescription+'\n'+
'Input file must be of type ' + ', '.join(modelFileTypes) + 
'\nDefault segmentaion: kidneys & tumor ', 
formatter_class=RawTextHelpFormatter)

parser.add_argument('input', metavar='i', type=str,
                    help='Specify the path to the directory containing the input scans')
parser.add_argument('output', metavar='o', type=str,
                    help='Specify the path of a single output file in the form of a glb file')
parser.add_argument('-type', metavar='t', type=int, nargs="*", default=[1,2], choices=range(0,len(modelSegTypes)),
    help="Specify the type of brain segmentation through an integer. Multiple integers can be supplied"
    +'\n'+'Segmentation types include ' + modelProcSegTypes)

args = parser.parse_args()

input_dir = args.input
output_path = args.output
segment_type = args.type

run(input_dir, output_path, segment_type)
