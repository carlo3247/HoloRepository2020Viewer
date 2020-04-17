import argparse
from core.pipelines.pipelines_controller import get_pipeline_description
from core.pipelines.bone_segmentation import run


pipeline_description = get_pipeline_description('bone_segmentation')

parser = argparse.ArgumentParser(description=pipeline_description)
parser.add_argument('input', metavar='i', type=str,
                    help='Specify the path to the directory containing the scans in the form of DICOM')
parser.add_argument('output', metavar='o', type=str,
                    help='Specify the path of a single output file in the form of a glb file')

args = parser.parse_args()


input_dir = args.input
output_path = args.output

run(input_dir, output_path)
