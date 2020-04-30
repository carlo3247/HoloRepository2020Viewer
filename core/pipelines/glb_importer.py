
import os

from trimesh import load_mesh
from trimesh import scene


from core.client.viewer import view_mesh

import numpy as np



this_plid = os.path.basename(__file__).replace(".py", "")

# For this pipeline, take into account anything > 0 from the generated segmentation
hu_threshold = 0


def run(input_file: str) -> None:
    trimesh_scene = load_mesh(input_file)
    if isinstance(trimesh_scene, scene.Scene):
        meshes = trimesh_scene.dump()
    else:
        meshes = trimesh_scene
    mesh_names = ["segmentation {}".format(i+1) for i in range(len(meshes))]
    view_mesh(meshes=meshes, mesh_names=mesh_names, output_file=input_file)

def get_random_rgb_colours():
    return list(np.random.rand(3))