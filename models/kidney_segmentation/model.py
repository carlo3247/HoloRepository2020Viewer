import os
import logging
from miscnn.data_loading.interfaces.nifti_io import NIFTI_interface
from miscnn.data_loading.data_io import Data_IO
from miscnn.processing.data_augmentation import Data_Augmentation
from miscnn.processing.subfunctions.normalization import Normalization
from miscnn.processing.subfunctions.clipping import Clipping
from miscnn.processing.subfunctions.resampling import Resampling
from miscnn.processing.preprocessor import Preprocessor
from miscnn.neural_network.architecture.unet.standard import Architecture
from miscnn.neural_network.model import Neural_Network
from miscnn.neural_network.metrics import dice_soft, dice_crossentropy, tversky_loss
import shutil

path_prefix = "./models/kidney_segmentation/"


class Kidney_model:
    def __init__(self, saved_path):

        self.input_path = os.path.join(path_prefix, "input/")
        os.mkdir(self.input_path)

        interface = NIFTI_interface(pattern="input", channels=1, classes=3)

        # data_path = os.path.join(path_prefix, upload_folder)
        data_io = Data_IO(interface, path_prefix)

        data_aug = Data_Augmentation(
            cycles=2,
            scaling=True,
            rotations=True,
            elastic_deform=True,
            mirror=True,
            brightness=True,
            contrast=True,
            gamma=True,
            gaussian_noise=True,
        )

        sf_normalize = Normalization(z_score=True)
        sf_clipping = Clipping(min=-79, max=304)
        sf_resample = Resampling((3.22, 1.62, 1.62))

        subfunctions = [sf_resample, sf_clipping, sf_normalize]

        pp = Preprocessor(
            data_io,
            data_aug=data_aug,
            batch_size=1,
            subfunctions=subfunctions,
            prepare_subfunctions=True,
            analysis="patchwise-crop",
            patch_shape=(48, 128, 128),
        )
        pp.patchwise_overlap = (12, 32, 32)

        unet_standard = Architecture()
        self.model = Neural_Network(
            preprocessor=pp,
            architecture=unet_standard,
            loss=tversky_loss,
            metrics=[dice_soft, dice_crossentropy],
            batch_queue_size=1,
            workers=1,
            learninig_rate=0.0001,
        )

        self.model.load(saved_path)

    def get_input_path(self):
        return os.path.join(self.input_path, "imaging.nii.gz")

    def predict(self):
        logging.info("Segmenting kidney...")
        # predict the image called imaging.nii in the specified folder and saves the result in predictions/foldername.nii
        self.model.predict(["input"])
        logging.info("Sucessfully segmented kidney")
        return os.path.abspath("./predictions/input.nii.gz")

    def cleanup(self):
        logging.info("Cleaning up kidney model temporary files")
        shutil.rmtree(self.input_path)
        shutil.rmtree(os.path.abspath("./predictions/"))


SAVED_MODEL_PATH = os.path.join(path_prefix, "kidney_model_miscnn")
kidney_model = Kidney_model(SAVED_MODEL_PATH)
