import os
import shutil
import subprocess

UPLOAD_FOLDER = "./models/dense_vnet_abdominal_ct/input/"
OUTPUT_FOLDER = "./models/dense_vnet_abdominal_ct/output/"


class Abdominal_model():

    # put your initialization code here
    def __init__(self, saved_path):
        self.config_path = saved_path
        os.mkdir(UPLOAD_FOLDER)
        os.mkdir(OUTPUT_FOLDER)
        self.input_path = os.path.join(UPLOAD_FOLDER, "abdominal.nii.gz")
        self.output_path = os.path.join(
            OUTPUT_FOLDER, "window_seg_abdominal__niftynet_out.nii.gz")

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
        shutil.rmtree(UPLOAD_FOLDER)
        shutil.rmtree(OUTPUT_FOLDER)


SAVED_CONFIG_PATH = "./models/dense_vnet_abdominal_ct/config.ini"
abdominal_model = Abdominal_model(SAVED_CONFIG_PATH)
