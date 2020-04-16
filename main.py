from core.pipelines.lung_segmentation import run

input_dir = "./samples/normal-chest-lung"
output_path = "output.glb"

run(input_dir, output_path)
