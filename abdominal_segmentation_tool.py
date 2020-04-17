import argparse 
from argparse import RawTextHelpFormatter
import json
from core.pipelines.abdominal_organs_segmentation import run

from core.pipelines.pipelines_controller import get_pipeline_description
from models.model_controller import (get_seg_types, 
get_file_types, get_req_modalities, get_proc_seg_types)


pipelineDescription = get_pipeline_description('abdominal_organs_segmentation')

modelSegTypes = get_seg_types('abdominal_organs_segmentation')
modelProcSegTypes = get_proc_seg_types('abdominal_organs_segmentation')
modelFileTypes = get_file_types('abdominal_organs_segmentation')
modelReqMods = get_req_modalities('abdominal_organs_segmentation')

parser = argparse.ArgumentParser(description=pipelineDescription  +
'\nInput files must be of type ' + ' or '.join(modelFileTypes) + 
'\nDefault segmentaion: spleen & liver & stomach ', 
formatter_class=RawTextHelpFormatter)

parser.add_argument('input', metavar='i', type=str,
                    help='Specify the path to the directory containing the input scans')
parser.add_argument('output', metavar='o', type=str,
                    help='Specify the path of a single output file in the form of a glb file')
parser.add_argument('-type', metavar='t', type=int, nargs="*", default=[1,5,6], choices=range(0,len(modelSegTypes)),
    help="Specify the type of abdominal segmentation through an integer. Multiple integers can be supplied"
    +'\n'+'Segmentation types include ' + modelProcSegTypes)

args = parser.parse_args()

input_dir = args.input
output_path = args.output
segment_type = args.type

run(input_dir, output_path, segment_type)
