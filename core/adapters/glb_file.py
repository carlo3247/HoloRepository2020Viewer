"""
This module contains functionality related to writing a mesh to disk as an GLB file.
"""
import numpy as np
import trimesh
from trimesh import repair


def write_mesh_as_glb(meshes, output_obj_file_path: str, metadata={}) -> None:
    scene = trimesh.Scene(metadata=metadata)
    for mesh in meshes:
        mesh2 = trimesh.Trimesh(vertices=mesh[0], faces=mesh[1], vertex_normals=mesh[2])

        repair.fix_inversion(mesh2)
        scene.add_geometry(mesh2)
    scene.export(output_obj_file_path)


def write_mesh_as_glb_with_colour(
    meshes, output_obj_file_path: str, colour, metadata={}
) -> None:
    scene = trimesh.Scene(metadata=metadata)
    index = 0
    for mesh in meshes:
        mesh2 = trimesh.Trimesh(vertices=mesh[0],
                                faces=mesh[1],
                                vertex_normals=mesh[2],
                                vertex_colors=colour[index]
                                )

        repair.fix_inversion(mesh2)
        mesh2.visual.material = trimesh.visual.material.SimpleMaterial(
            diffuse=np.asarray(colour[index]))
        scene.add_geometry(mesh2)
        index += 1
    scene.export(output_obj_file_path)
