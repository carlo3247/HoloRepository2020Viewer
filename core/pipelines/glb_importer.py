
import os
import logging
import trimesh

from core.adapters.trimesh_converter import convert_meshes_trimesh
from core.client.viewer import view_mesh



this_plid = os.path.basename(__file__).replace(".py", "")

# For this pipeline, take into account anything > 0 from the generated segmentation
hu_threshold = 0


def run(input_file: str) -> None:
    logger = logging.getLogger("glb_importer")
    logger.info("READING_INPUT")
    trimesh_scene = trimesh.load(input_file)
    if isinstance(trimesh_scene, trimesh.scene.scene.Scene):
        meshes = trimesh_scene.dump()
        for mesh in meshes:
            mesh.visual.vertex_colors = [0.5,0.5,0.5]
    else:
        meshes = trimesh_scene

    logger.info("Viewing")
    print(type(meshes))
    view_mesh(meshes, input_file)
