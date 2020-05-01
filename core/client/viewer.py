import logging
from vtkplotter import trimesh2vtk, interactive, colors, Text2D
from vtkplotter import Plotter, settings
from core.adapters.vtk_to_glb import write_mesh_as_glb_with_colour
from core.wrappers import holo_registration_wrapper
from core.wrappers import external_2d_viewer

index = 0
font_style = "arial"


def view_mesh(
    meshes: list,
    output_file: str,
    mesh_names: list = [],
    patient_data="",
    plid="",
    scan_path="",
):
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

    def ar_view():
        save()
        holo_registration_wrapper.start_viewer(output_file, plid)

    def save():
        write_mesh_as_glb_with_colour(vmeshes, output_file)

    def open_scan():
        external_2d_viewer.start(scan_path)

    vp = Plotter(
        sharecam=False,
        bg="./core/client/images/hologram_icon2.png",
        bg2="black",
        shape=[1, 1],
        interactive=False,
    )
    # pos = position corner number: horizontal [1-4] or vertical [11-14]
    vp.addSlider2D(slider1, -9, 9, value=0, pos=4, title="color number")

    left_side_x = 0.1

    vp.addSlider2D(
        slider2,
        xmin=0.00,
        xmax=1.00,
        value=0.5,
        pos=14,
        c="blue",
        title="alpha value (opacity)",
    )

    bu = vp.addButton(
        buttonfunc,
        pos=(0.5, 0.05),  # x,y fraction from bottom left corner
        states=mesh_names,
        font=font_style,  # arial, courier, times
        size=25,
        bold=True,
        italic=False,
    )

    save_button = vp.addButton(
        save,
        pos=(left_side_x, 0.05),  # x,y fraction from bottom left corner
        states=["Save"],
        font=font_style,  # arial, courier, times
        size=25,
        bold=True,
        italic=False,
    )

    if holo_registration_wrapper.is_supported(plid):
        ar_button = vp.addButton(
            ar_view,
            pos=(left_side_x, 0.20),
            states=["AR View"],
            font=font_style,
            size=25,
            bold=True,
            italic=False,
        )

    if scan_path != "":
        scan_button = vp.addButton(
            open_scan,
            pos=(left_side_x, 0.15),
            states=["2D View"],
            font=font_style,
            size=25,
            bold=True,
            italic=False,
        )

    bg_button = vp.addButton(
        background_swap,
        pos=(left_side_x, 0.10),  # x,y fraction from bottom left corner
        states=["black", "white"],
        font=font_style,
        size=25,
        bold=True,
        italic=False,
    )

    for i in range(0, len(meshes)):
        vmeshes.append(trimesh2vtk(meshes[i], alphaPerCell=True))
    doc = Text2D(patient_data, pos=4, c=(0, 113, 197))
    vp.backgroundRenderer.GetActiveCamera().Zoom(1.3)
    vp.show(doc)
    vp.show(vmeshes)
    interactive()
