"""
This pipeline performs automatic multi-organ segmentation on abdominal CT with Dense
V-networks. It leverages a pre-trained network built with Niftynet and running in a
separate container.

Model: https://github.com/NifTK/NiftyNetModelZoo/blob/master/dense_vnet_abdominal_ct_model_zoo.md
Paper: Eli Gibson, Francesco Giganti, Yipeng Hu, Ester Bonmati, Steve Bandula, Kurinchi Gurusamy,
Brian Davidson, Stephen P. Pereira, Matthew J. Clarkson and Dean C. Barratt (2017), Automatic
multi-organ segmentation on abdominal CT with dense v-networks https://doi.org/10.1109/TMI.2018.2806309
"""

import os

from core.adapters.dicom_file import (
    read_dicom_as_np_ndarray_and_normalise,
    flip_numpy_array_dimensions_y_only,
)

from core.adapters.nifti_file import (
    convert_dicom_np_ndarray_to_nifti_image,
    read_nifti_as_np_array,
    write_nifti_image,
)
from core.adapters.glb_file import write_mesh_as_glb
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import downscale_and_conditionally_crop

from models.dense_vnet_abdominal_ct.model import abdominal_model

this_plid = os.path.basename(__file__).replace(".py", "")
hu_threshold = 0


def run(dicom_directory_path: str, output_path: str) -> None:

    dicom_image_array = read_dicom_as_np_ndarray_and_normalise(
        dicom_directory_path)
    # NOTE: Numpy array is flipped in the Y axis here as this is the specific image input for the NiftyNet model
    # dicom_image_array = flip_numpy_array_dimensions_y_only(dicom_image_array)
    crop_dicom_image_array = downscale_and_conditionally_crop(
        dicom_image_array)
    crop_dicom_image_array = flip_numpy_array_dimensions_y_only(
        crop_dicom_image_array)

    nifti_image = convert_dicom_np_ndarray_to_nifti_image(
        crop_dicom_image_array)
    initial_nifti_output_file_path = abdominal_model.get_input_path()
    write_nifti_image(nifti_image, initial_nifti_output_file_path)

    segmented_nifti_output_file_path = abdominal_model.predict()

    segmented_array = read_nifti_as_np_array(
        segmented_nifti_output_file_path, normalise=False
    )

    meshes = [generate_mesh(segmented_array, hu_threshold)]
    write_mesh_as_glb(meshes, output_path)
