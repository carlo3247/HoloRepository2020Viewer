from core.pipelines.bone_segmentation import run

input_dir = "./samples/left-scfe-pelvis-bone"
output_dir = "output.glb"

run(input_dir, output_dir)
