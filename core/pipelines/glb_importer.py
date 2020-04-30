import os
import logging
import trimesh
from trimesh.visual import ColorVisuals
from core.adapters.trimesh_converter import convert_meshes_trimesh
from core.client.viewer import view_mesh

import numpy as np


this_plid = os.path.basename(__file__).replace(".py", "")

# For this pipeline, take into account anything > 0 from the generated segmentation
hu_threshold = 0


def run(input_file: str) -> None:
    trimesh_scene = trimesh.load(input_file)
    if isinstance(trimesh_scene, trimesh.scene.scene.Scene):
        meshes = trimesh_scene.dump()
        for mesh in meshes:
            mesh.visual = ColorVisuals(
                mesh=mesh, vertex_colors=mesh.visual.material.baseColorFactor
            )
    else:
        meshes = trimesh_scene
    mesh_names = ["segmentation {}".format(i + 1) for i in range(len(meshes))]
    view_mesh(meshes=meshes, mesh_names=mesh_names, output_file=input_file)


def get_random_rgb_colours():
    return list(np.random.rand(3))
