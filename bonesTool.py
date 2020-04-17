import argparse
# from core.pipelines.pipelines_controller import get_pipelines_ids_list
import json
from core.pipelines.bone_segmentation import run

with open('core/pipelines/pipelines.json') as f:
  pipelineData = json.load(f)

pipelineDescription = pipelineData['bone_segmentation']['description']

parser = argparse.ArgumentParser(description=pipelineDescription)
parser.add_argument('input', metavar='i', type=str,
                    help='Specify the path to the directory containing the scans in the form of DICOM')
parser.add_argument('output', metavar='o', type=str,
                    help='Specify the path of a single output file in the form of a glb file')

args = parser.parse_args()



input_dir = args.input
output_path = args.output

run(input_dir, output_path)