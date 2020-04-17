import argparse 
from argparse import RawTextHelpFormatter
import json
from core.pipelines.brain_segmentation import run

from core.pipelines.pipelines_controller import get_pipeline_description
from models.model_controller import (get_seg_types, 
get_file_types, get_req_modalities, get_proc_seg_types)


pipelineDescription = get_pipeline_description('brain_segmentation')

modelSegTypes = get_seg_types('brain_segmentation')
modelProcSegTypes = get_proc_seg_types('brain_segmentation')
modelFileTypes = get_file_types('brain_segmentation')
modelReqMods = get_req_modalities('brain_segmentation')

parser = argparse.ArgumentParser(description=pipelineDescription +
'\n3 input scans (modalities) required of types ' + ', '.join(modelReqMods) +
'\nInput files must be of type ' + ' or '.join(modelFileTypes) + 
'\nDefault segmentaion: cortical_gray_matter ', 
formatter_class=RawTextHelpFormatter)

parser.add_argument('flair_input', metavar='t2-f',type=str,
                    help='Specify the path to the directory containing the T2-FLAIR input scans')
parser.add_argument('t1_input', metavar='t1', type=str,
                    help='Specify the path to the directory containing the T1 input scans')
parser.add_argument('ir_input', metavar='t1-i',type=str,
                    help='Specify the path to the directory containing the T1-IR input scans')
parser.add_argument('output', metavar='o', type=str,
                    help='Specify the path of a single output file in the form of a glb file')
parser.add_argument('-type', metavar='t', type=int, default=[1], choices=range(0,len(modelSegTypes)),
    help="Specify the type of brain segmentation through an integer. Multiple integers can be supplied"+
    '\n'+'Segmentation types include ' + modelProcSegTypes)

args = parser.parse_args()

print(args)

flair_input_directory = args.flair_input
t1_input_directory = args.t1_input
ir_input_directory = args.ir_input
output_path = args.output
segment_type = args.type

run(flair_input_directory, t1_input_directory, ir_input_directory, output_path, segment_type)
