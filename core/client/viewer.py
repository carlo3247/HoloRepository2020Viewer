import logging
from vtkplotter import trimesh2vtk,interactive,colors,Text2D
from vtkplotter import Plotter, settings
from core.adapters.vtk_to_glb import write_mesh_as_glb_with_colour

index = 0


def view_mesh(meshes: list, output_file: str, mesh_names: list = [], patient_data = ""):
    logging.info("Opening mesh viewer.")
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
        index = mesh_names.index(bu.status())

    def background_swap():
        bg_button.switch()
        vp.backgroundRenderer.SetBackground(colors.getColor(bg_button.status()))

    def save():
        write_mesh_as_glb_with_colour(vmeshes, output_file)

    vp = Plotter(sharecam=False,
                 bg="./core/client/images/hologram_icon2.png",
                 bg2='black',shape=[1,1],interactive=False)
    # pos = position corner number: horizontal [1-4] or vertical [11-14]
    vp.addSlider2D(slider1, -9, 9, value=0, pos=4, title="color number")

    vp.addSlider2D(
        slider2,
        xmin=0.01,
        xmax=0.99,
        value=0.5,
        pos=14,
        c="blue",
        title="alpha value (opacity)",
    )

    bu = vp.addButton(
        buttonfunc,
        pos=(0.5, 0.05),  # x,y fraction from bottom left corner
        states=mesh_names,
        font="courier",  # arial, courier, times
        size=25,
        bold=True,
        italic=False,
    )

    save_button = vp.addButton(
        save,
        pos=(0.5, 0.15),  # x,y fraction from bottom left corner
        states=["Save"],
        font="courier",  # arial, courier, times
        size=25,
        bold=True,
        italic=False,
    )

    bg_button = vp.addButton(
        background_swap,
        pos=(0.5, 0.10),  # x,y fraction from bottom left corner
        states=["black","white"],
        font="courier",  # arial, courier, times
        size=25,
        bold=True,
        italic=False,
    )


    for i in range(0, len(meshes)):
        vmeshes.append(trimesh2vtk(meshes[i], alphaPerCell=True))
    doc = Text2D(patient_data, pos=4,c=(0,113,197))
    vp.backgroundRenderer.GetActiveCamera().Zoom(1.3)
    vp.show(doc)
    vp.show(vmeshes)
    interactive()
