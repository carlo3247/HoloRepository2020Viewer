from core.pipelines.abdominal_organs_segmentation import run

input_dir = "./samples/abdominal/normal-abdomen"
flair = "./samples/brain/FLAIR.nii.gz"
t1 = "./samples/brain/reg_T1.nii.gz"
ir = "./samples/brain/reg_IR.nii.gz"
output_path = "output.glb"

run(input_dir, output_path)
