
from vtkplotter import trimesh2vtk,vtk2trimesh,load,datadir,interactive,addons

from vtkplotter import Plotter,settings
import threading
import random

from core.adapters.vtk_to_glb import write_mesh_as_glb_with_colour

index = 0
rotate_mesh = False

def view_mesh(meshes,output_file):
    settings.useDepthPeeling = True
    vmeshes = []

    def slider1(widget, event):
        value = widget.GetRepresentation().GetValue()
        vmeshes[index].color(value)

    def slider2(widget, event):
        value = widget.GetRepresentation().GetValue()
        vmeshes[index].opacity(value)


    def buttonfunc():
        global index
        bu.switch()
        index = int(bu.status().split(':')[1])



    def save():
        write_mesh_as_glb_with_colour(vmeshes,output_file)

    vp = Plotter(axes=0,bg="black",interactive=False)
    # pos = position corner number: horizontal [1-4] or vertical [11-14]
    vp.addSlider2D(slider1, -9, 9, value=0, pos=4, title="color number")

    vp.addSlider2D(slider2, xmin=0.01, xmax=0.99, value=0.5,
                   pos=14, c="blue", title="alpha value (opacity)")


    bu = vp.addButton(
        buttonfunc,
        pos=(0.5, 0.05),  # x,y fraction from bottom left corner
        states= ["Segmentation : "+str(i) for i in range(0,len(meshes))] ,
        font="courier",  # arial, courier, times
        size=25,
        bold=True,
        italic=False,
    )

    save_button = vp.addButton(
        save,
        pos=(0.5, 0.10),  # x,y fraction from bottom left corner
        states=["Save"],
        font="courier",  # arial, courier, times
        size=25,
        bold=True,
        italic=False,
    )



    for i in range(0,len(meshes)):
        vtk = trimesh2vtk(meshes[0], alphaPerCell=True)
        vmeshes.append(vtk)

    vp.show(vmeshes, rate=60, interactorStyle=0)
    interactive()
