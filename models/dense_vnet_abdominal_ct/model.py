import os
import subprocess

# TODO change with local nifty root
UPLOAD_FOLDER = "~/niftynet/data/dense_vnet_abdominal_ct/"
OUTPUT_FOLDER = "~/niftynet/models/dense_vnet_abdominal_ct/segmentation_output/"


class Abdominal_model():

    # put your initialization code here
    def __init__(self, saved_path):
        self.config_path = saved_path
        self.input_path = os.path.join(UPLOAD_FOLDER, "abdominal.nii.gz")
        self.output_path = os.path.join(
            OUTPUT_FOLDER, "abdominal__niftynet_out.nii.gz")

    def get_input_path(self):
        return self.input_path

    def predict(self):
        subprocess.run(
            [
                "net_segment",
                "inference",
                "-c",
                self.config_path
            ]
        )
        return self.output_path

    def cleanup(self):
        os.remove(self.input_path)
        os.remove(self.output_path)


SAVED_CONFIG_PATH = "./models/dense_vnet_abdominal_ct/config.ini"
abdominal_model = Abdominal_model(SAVED_CONFIG_PATH)
