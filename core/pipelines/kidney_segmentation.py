"""
This pipeline performs automatic kidney segmentation on abdominal CT with a 3d UNet.
It leverages a pre-trained network built with MISCNN.
"""

import os
import logging

from core.adapters.nifti_file import (
    read_nifti_as_np_array,
    read_nifti_image,
    write_nifti_image,
)
from core.adapters.file_loader import read_input_path_as_np_array
from core.adapters.file_loader import get_metadata
from core.adapters.trimesh_converter import convert_meshes_trimesh
from core.client.viewer import view_mesh
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import seperate_segmentation
from core.adapters.glb_file import write_mesh_as_glb_with_colour
from models.kidney_segmentation.model import kidney_model
from models.model_controller import get_seg_types

this_plid = os.path.basename(__file__).replace(".py", "")


def run(
    input_path: str,
    output_path: str,
    segment_type: list,
    iterations: int,
    open_viewer=True,
) -> None:
    logging.info("Starting kidney pipeline")
    image = read_nifti_image(input_path)
    initial_nifti_output_file_path = kidney_model.get_input_path()
    write_nifti_image(image, initial_nifti_output_file_path)
    segmented_nifti_output_file_path = kidney_model.predict()

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
        metadata = get_metadata(input_path)
        meshes = convert_meshes_trimesh(meshes, iterations)
        segment_dict = get_seg_types(this_plid)
        mesh_names = [k for (k, v) in segment_dict.items() if v in segment_type]
        view_mesh(
            meshes=meshes,
            mesh_names=mesh_names,
            output_file=output_path,
            patient_data=metadata,
            plid=this_plid,
            scan_path=input_path,
        )
    else:
        write_mesh_as_glb_with_colour(meshes, output_path, iterations)

    kidney_model.cleanup()
    logging.info("Kidney pipeline finished successfully")
