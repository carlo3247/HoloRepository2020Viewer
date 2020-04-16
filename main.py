from core.pipelines.brain_segmentation import run

input_dir = "./samples/normal-chest-lung"
flair = "./samples/brain/FLAIR.nii.gz"
t1 = "./samples/brain/reg_T1.nii.gz"
ir = "./samples/brain/reg_IR.nii.gz"
output_path = "output.glb"

run(flair, t1, ir, output_path)
