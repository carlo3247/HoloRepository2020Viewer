"""
This module contains functionality related to writing a mesh to disk as an GLB file.
"""
import numpy as np
import math

import trimesh
from trimesh import visual
from trimesh import repair

from vtkplotter import vtk2trimesh

import logging




def write_mesh_as_glb_with_colour(
        meshes, output_obj_file_path: str, metadata={}
) -> None:
    scene = trimesh.Scene(metadata=metadata)
    index = 0
    for mesh in meshes:
        mesh2 = vtk2trimesh(mesh)

        repair.fix_inversion(mesh2)
        print(type((mesh.color().tolist())))
        mesh2.visual.material = trimesh.visual.material.SimpleMaterial(
            diffuse=np.asarray(mesh.color().tolist()+[mesh.alpha()]))
        scene.add_geometry(mesh2)
    scene.export(output_obj_file_path)
