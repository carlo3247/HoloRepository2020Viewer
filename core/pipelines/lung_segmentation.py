"""
This pipeline performs automatic segmentation of lungs. It uses an existing algorithmic
implementation for the actual segmentation.

Algorithm: https://github.com/wanwanbeen/ct_lung_segmentation
Paper: Discriminative Localization in CNNs for Weakly-Supervised Segmentation of Pulmonary Nodules
Xinyang Feng, Jie Yang, Andrew F. Laine, Elsa D. Angelini
"""
import os
import logging

from core.adapters.dicom_file import read_dicom_as_np_ndarray_and_normalise

from core.adapters.glb_file import write_mesh_as_glb
from core.adapters.trimesh_converter import convert_meshes_trimesh
from core.client.viewer import view_mesh
from core.services.marching_cubes import generate_mesh
from core.services.np_image_manipulation import downscale_and_conditionally_crop
from core.third_party.lung_and_airway_segmentation import perform_lung_segmentation


this_plid = os.path.basename(__file__).replace(".py", "")

# For this pipeline, take into account anything > 0 from the generated segmentation
hu_threshold = 0


def run(input_dir: str, output_path: str, segment_type: list) -> None:
    logging.info("Starting lung pipeline")
    image_data = read_dicom_as_np_ndarray_and_normalise(input_dir)

    image_data = downscale_and_conditionally_crop(image_data)
    segmented_lung, segmented_airway = perform_lung_segmentation(image_data)

    meshes = []
    if 1 in segment_type:  # lung segmentation
        meshes.append(generate_mesh(segmented_lung, hu_threshold))
    if 2 in segment_type:  # airway segmentation
        meshes.append(generate_mesh(segmented_airway, hu_threshold))

    if len(meshes) == 0:
        raise Exception(
            "No valid segmentation specified, segmentation type must be either 1 or 2"
        )

    meshes = convert_meshes_trimesh(meshes)
    view_mesh(meshes, output_path)
    logging.info("Lung pipeline finished successfully")
