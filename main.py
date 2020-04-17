from core.pipelines.kidney_segmentation import run

input_dir = "./samples/kidney/kidney.nii.gz"
flair = "./samples/brain/FLAIR.nii.gz"
t1 = "./samples/brain/reg_T1.nii.gz"
ir = "./samples/brain/reg_IR.nii.gz"
output_path = "output.glb"

run(input_dir, output_path)
