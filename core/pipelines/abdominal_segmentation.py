"""
This pipeline performs automatic multi-organ segmentation on abdominal CT with Dense
V-networks. It leverages a pre-trained network built with Niftynet.

Model: https://github.com/NifTK/NiftyNetModelZoo/blob/master/dense_vnet_abdominal_ct_model_zoo.md
Paper: Eli Gibson, Francesco Giganti, Yipeng Hu, Ester Bonmati, Steve Bandula, Kurinchi Gurusamy,
Brian Davidson, Stephen P. Pereira, Matthew J. Clarkson and Dean C. Barratt (2017), Automatic
multi-organ segmentation on abdominal CT with dense v-networks https://doi.org/10.1109/TMI.2018.2806309
"""

import os
import logging

from core.adapters.dicom_file import flip_numpy_array_dimensions_y_only
from core.adapters.file_loader import read_input_path_as_np_array
from core.adapters.nifti_file import (
    convert_np_ndarray_to_nifti_image,
    read_nifti_as_np_array,
    write_nifti_image,
)
from core.adapters.glb_file import write_mesh_as_glb_with_colour
from core.adapters.trimesh_converter import convert_meshes_trimesh
from core.client.viewer import view_mesh
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import (
    downscale_and_conditionally_crop,
    seperate_segmentation,
)
from models.model_controller import get_seg_types
from models.dense_vnet_abdominal_ct.model import abdominal_model

this_plid = os.path.basename(__file__).replace(".py", "")
hu_threshold = 0


def run(
    input_path: str, output_path: str, segment_type: list, open_viewer=True
) -> None:
    logging.info("Starting abdominal pipeline")
    dicom_image_array = read_input_path_as_np_array(input_path)
    crop_dicom_image_array = downscale_and_conditionally_crop(dicom_image_array)
    # NOTE: Numpy array is flipped in the Y axis here as this is the specific image input for the NiftyNet model
    crop_dicom_image_array = flip_numpy_array_dimensions_y_only(crop_dicom_image_array)

    nifti_image = convert_np_ndarray_to_nifti_image(crop_dicom_image_array)
    initial_nifti_output_file_path = abdominal_model.get_input_path()
    write_nifti_image(nifti_image, initial_nifti_output_file_path)
    segmented_nifti_output_file_path = abdominal_model.predict()

    segmented_array = read_nifti_as_np_array(
        segmented_nifti_output_file_path, normalise=False
    )

    meshes = [
        generate_mesh(segment, 0)
        for segment in seperate_segmentation(
            segmented_array, unique_values=segment_type
        )
    ]

    if open_viewer:
        meshes = convert_meshes_trimesh(meshes)
        segment_dict = get_seg_types(this_plid)
        mesh_names = [k for k, v in segment_dict.items() if v in segment_type]
        view_mesh(meshes=meshes, mesh_names=mesh_names, output_file=output_path)
    else:
        write_mesh_as_glb_with_colour(meshes, output_path)

    abdominal_model.cleanup()
    logging.info("Abdominal pipeline finished successfully")
