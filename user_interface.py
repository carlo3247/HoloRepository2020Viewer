import logging
import re
import os
import tkinter as tk  # python 3
from PIL import Image, ImageTk
from tkinter import font as tkfont  # python 3
from tkinter import messagebox
from tkinter import font as tkFont
from tkinter import filedialog
from core.wrappers import holo_registration_wrapper
from core.wrappers import external_2d_viewer


from core.pipelines.pipelines_controller import (
    get_pipeline_description,
    load_pipeline_dynamically,
    get_pipelines_ids_list,
)
from models.model_controller import (
    get_seg_types,
    get_file_types,
    get_req_modalities,
    get_proc_seg_types,
)


text_font_size = 15
title_font_size = 40
form_button_text_size = 20
form_entry_width = 100


def get_information(plid):
    pipeline_description = get_pipeline_description(plid)
    model_file_types = get_file_types(plid)
    model_req_mods = get_req_modalities(plid)

    information = (
        pipeline_description
        + "\n\nInput must be "
        + " or ".join(model_file_types)
        + "."
    )
    return (
        information + "\n"
        if plid != "brain_segmentation"
        else information
        + "\n3 input scans (modalities) required of types "
        + ", ".join(model_req_mods)
        + "\n"
    )


def generate(entries, plid, ar_view):
    output_path = entries["Output File"].get()
    segment_type = list(entries["seg_types"].curselection())
    segment_type = [s + 1 for s in segment_type]
    quiet = entries["silence_log"].get()

    if plid != "brain_segmentation":
        input_dir = entries["Input"].get()
    else:
        flair_dir = entries["Flair Input"].get()
        t1_dir = entries["T1 Input"].get()
        ir_dir = entries["IR Input"].get()
        input_dir = [flair_dir, t1_dir, ir_dir]

    if (
        (plid == "brain_segmentation" and "" in input_dir)
        or input_dir == ""
        or output_path == ""
        or not segment_type
    ):
        messagebox.showerror(
            "Error",
            "Please ensure input/s, an output path, and segmentation type is inputted",
        )
    else:
        logging.basicConfig(
            level=logging.ERROR if quiet else logging.INFO,
            format="%(asctime)s - %(module)s:%(levelname)s - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
        )
        messagebox.showinfo(
            "Help",
            """This may take a while...\n\nPlease click ok to continue and check console output for progress""",
        )
        logging.info("Loading and initializing pipeline dynamically")
        pipeline_module = load_pipeline_dynamically(plid)
        if ar_view:
            pipeline_module.run(input_dir, output_path, segment_type, False)
            holo_registration_wrapper.start_viewer(output_path, plid)
        else:
            pipeline_module.run(input_dir, output_path, segment_type)
        logging.info("Done.")


def browsefunc(entry):
    folder_selected = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(tk.END, folder_selected)


def browsefile(entry):
    file_selected = filedialog.askopenfilename(
        filetypes=(("Compressed NifTI", "*.nii.gz"), ("All files", "*"))
    )
    entry.delete(0, tk.END)
    entry.insert(tk.END, file_selected)


def openViewer():
    plid = "glb_importer"
    file_selected = filedialog.askopenfilename(
        filetypes=(("glb file", "*.glb"), ("All files", "*"))
    )
    if file_selected != "":
        pipeline_module = load_pipeline_dynamically(plid)
        pipeline_module.run(file_selected)


def create_form(root, plid):
    input_form = tk.Frame(root)
    input_form.pack(padx=50)

    fields = (
        ["Input", "Output File"]
        if plid != "brain_segmentation"
        else [
            "Flair Input Directory",
            "T1 Input Directory",
            "IR Input Directory",
            "Output File",
        ]
    )

    entries = {}

    if plid != "brain_segmentation":
        input_row = tk.Frame(input_form)
        input_ent = tk.Entry(input_row, width=form_entry_width)
        input_lab = tk.Label(
            input_row,
            width=15,
            text="Input",
            anchor="w",
            font=("Helvetica", 15, "bold"),
        )
        input_lab.pack(side=tk.LEFT)
        input_row.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx=5)
        input_ent.pack(
            side=tk.LEFT, fill=tk.X,
        )
        browse_button = tk.Button(
            input_row,
            text="Browse NiFTI File",
            font=form_button_text_size,
            command=lambda: browsefile(input_ent),
        )
        browse_dir_button = tk.Button(
            input_row,
            text="Browse DICOM Directory",
            font=form_button_text_size,
            state=tk.NORMAL if plid != "kidney_segmentation" else tk.DISABLED,
            command=lambda: browsefunc(input_ent),
        )
        browse_button.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        browse_dir_button.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        entries["Input"] = input_ent
    else:
        input_row = tk.Frame(input_form)
        input_ent = tk.Entry(input_row, width=form_entry_width)
        input_lab = tk.Label(
            input_row,
            width=15,
            text="Flair Input",
            anchor="w",
            font=("Helvetica", 15, "bold"),
        )
        input_lab.pack(side=tk.LEFT)
        input_row.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx=5, pady=5)
        input_ent.pack(
            side=tk.LEFT, fill=tk.X,
        )
        browse_button = tk.Button(
            input_row,
            text="Browse NiFTI File",
            font=form_button_text_size,
            command=lambda: browsefile(input_ent),
        )
        browse_dir_button = tk.Button(
            input_row,
            text="Browse DICOM Directory",
            font=form_button_text_size,
            command=lambda: browsefunc(input_ent),
        )
        browse_button.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        browse_dir_button.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        entries["Flair Input"] = input_ent

        input_row_2 = tk.Frame(input_form)
        input_ent_2 = tk.Entry(input_row_2, width=form_entry_width)
        input_lab_2 = tk.Label(
            input_row_2,
            width=15,
            text="T1 Input",
            anchor="w",
            font=("Helvetica", 15, "bold"),
        )
        input_lab_2.pack(side=tk.LEFT)
        input_row_2.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx=5, pady=5)
        input_ent_2.pack(
            side=tk.LEFT, fill=tk.X,
        )
        browse_button_2 = tk.Button(
            input_row_2,
            text="Browse NiFTI File",
            font=form_button_text_size,
            command=lambda: browsefile(input_ent_2),
        )
        browse_dir_button_2 = tk.Button(
            input_row_2,
            text="Browse DICOM Directory",
            font=form_button_text_size,
            command=lambda: browsefunc(input_ent_2),
        )
        browse_button_2.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        browse_dir_button_2.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        entries["T1 Input"] = input_ent_2

        input_row_3 = tk.Frame(input_form)
        input_ent_3 = tk.Entry(input_row_3, width=form_entry_width)
        input_lab_3 = tk.Label(
            input_row_3,
            width=15,
            text="IR Input",
            anchor="w",
            font=("Helvetica", 15, "bold"),
        )
        input_lab_3.pack(side=tk.LEFT)
        input_row_3.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx=5, pady=5)
        input_ent_3.pack(
            side=tk.LEFT, fill=tk.X,
        )
        browse_button_3 = tk.Button(
            input_row_3,
            text="Browse NiFTI File",
            font=form_button_text_size,
            command=lambda: browsefile(input_ent_3),
        )
        browse_dir_button_3 = tk.Button(
            input_row_3,
            text="Browse DICOM Directory",
            font=form_button_text_size,
            command=lambda: browsefunc(input_ent_3),
        )
        browse_button_3.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        browse_dir_button_3.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        entries["IR Input"] = input_ent_3

    output_row = tk.Frame(input_form)
    output_lab = tk.Label(
        output_row,
        width=15,
        text="Output File",
        anchor="w",
        font=("Helvetica", text_font_size, "bold"),
    )
    out_ent = tk.Entry(output_row, width=form_entry_width)
    out_ent.insert(tk.END, "output.glb")
    output_row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    output_lab.pack(side=tk.LEFT)
    out_ent.pack(side=tk.LEFT, fill=tk.X)
    entries["Output File"] = out_ent

    seg_types = get_seg_types(plid).keys()

    next_row = tk.Frame(input_form)
    next_row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    type_label = tk.Label(
        next_row,
        text="Please select one or more types",
        anchor="w",
        font=("Helvetica", text_font_size, "bold"),
    )
    type_label.grid(row=0, column=0, padx=(0, 10))
    # listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    scrollbar = tk.Scrollbar(next_row, orient=tk.VERTICAL)
    listbox = tk.Listbox(
        next_row,
        font=("Helvetica", 15),
        height=min(len(seg_types), 7),
        selectmode="multiple",
        yscrollcommand=scrollbar.set,
    )
    scrollbar.config(command=listbox.yview)
    if len(seg_types) >= 7:
        scrollbar.grid(row=0, column=42, sticky="nse")

    for item in seg_types:
        listbox.insert(tk.END, item)
    if len(seg_types) == 1:  # if only one item pre-select it
        listbox.selection_set(0, tk.END)
    listbox.grid(row=0, column=40, padx=10)
    entries["seg_types"] = listbox

    silence_log = tk.IntVar()
    silence_button = tk.Checkbutton(
        next_row, text="Silence logging ", variable=silence_log
    )
    silence_button.grid(row=0, column=80, padx=30)
    entries["silence_log"] = silence_log

    return entries


def help_box(plid):
    if plid != "brain_segmentation":
        messagebox.showinfo(
            "Help",
            """Input : Select a compressed NifTi file (*.nii.gz) OR directory containing DICOM (*.dcm) scans through the file or folder browser\n\nOuput Directory: Specify the path to the output. e.g. path/output.glb\n\nType: Specify the segmentation/s to be generated\n\nAR View only suported on Windows OS""",
        )
    else:
        messagebox.showinfo(
            "Help",
            """Input : Select a compressed NifTi file (*.nii.gz) OR directory containing DICOM (*.dcm) scans through the file or folder browser\n\n Inputs required: T2-Flair, T1, T1-Intermediate Representation scans\n\nOuput Directory: Specify the path to the output. e.g. path/output.glb\n\nType: Specify the segmentation/s to be generated\n\nAR View only suported on Windows OS""",
        )


def add_logo_frame(root):
    logo_path = "./core/client/logos"
    logo_frame = tk.Frame(root)
    for logo in os.listdir(logo_path):
        image = Image.open(os.path.join(logo_path, logo))
        image = image.resize((75, 75), Image.ANTIALIAS)
        simg = ImageTk.PhotoImage(image)
        my = tk.Label(logo_frame, image=simg)
        my.image = simg
        my.pack(side=tk.LEFT, padx=20, pady=5)
    logo_frame.pack(anchor=tk.NW)


class ViewerApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("HoloRepository 2020 Viewer")
        self.iconbitmap("./core/client/images/favicon.ico")
        self.state("zoomed")
        self.title_font = tkfont.Font(
            family="Helvetica", size=18, weight="bold", slant="italic"
        )

        # the container is where we'll stack a bunch of frames
        # on tk.TOP of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        plids = get_pipelines_ids_list()
        plids.remove("glb_importer")

        self.frames = {}
        splash_screen = SplashScreen(
            parent=container,
            controller=self,
            next_screen_func=lambda x: self.show_frame("StartPage"),
        )
        self.frames["SplashScreen"] = splash_screen
        splash_screen.grid(row=0, column=0, sticky="nsew")
        start_page = StartPage(parent=container, controller=self, plids=plids)
        self.frames["StartPage"] = start_page
        start_page.grid(row=0, column=0, sticky="nsew")
        for plid in plids:
            frame = ParameterPage(parent=container, controller=self, plid=plid)
            self.frames[plid] = frame

            # put all of the pages in the same location;
            # the one on the tk.TOP of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SplashScreen")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller, plids):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        add_logo_frame(self)

        title = tk.Label(self, text="HoloRepository 2020 Viewer")
        title.config(font=("Futura", title_font_size, "bold"))
        title.pack()

        description = "This tool will open a CT/MRI scan from a local file, identify key anatomical structures, and extract them. The structures become viewable through a 3D model viewer or an AR viewer. The tool uses local versions of the HoloPipelines.\n\nPlease select one of the pipelines to launch."
        description_label = tk.Label(self, text=description, wraplength=800)
        description_label.config(font=("Helvetica", text_font_size))
        description_label.pack(anchor=tk.CENTER, pady=10)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack()

        generate_frame = tk.Frame(buttons_frame)
        generate_frame.pack(side=tk.LEFT)

        view_frame = tk.Frame(buttons_frame)
        view_frame.pack(anchor=tk.NW, padx=50)

        menu_1_label = tk.Label(generate_frame, text="Generate from scan:")
        menu_1_label.config(font=("Helvetica", 13, "bold"))
        menu_1_label.pack(anchor=tk.CENTER, pady=10)

        helv20 = tkFont.Font(family="Helvetica", size=20)

        for plid in plids:
            title = re.sub(r"_segmentation", "", plid).title()
            button = tk.Button(
                generate_frame,
                text=title,
                command=lambda p=plid: controller.show_frame(p),
                highlightbackground="#3E4149",
                font=helv20,
                width=20,
            )
            button.pack(pady=(0, 10))

        menu_2_label = tk.Label(view_frame, text="View existing model:")
        menu_2_label.config(font=("Helvetica", 13, "bold"))
        menu_2_label.pack(anchor=tk.CENTER, pady=10)

        view_button = tk.Button(
            view_frame,
            text="Open viewer",
            command=lambda: openViewer(),
            highlightbackground="#3E4149",
            font=helv20,
            width=20,
        )
        view_button.pack(anchor=tk.NE)

        footer_frame = tk.Frame(self)
        footer_frame.pack(side=tk.RIGHT, anchor=tk.SE)

        about_button = tk.Button(
            footer_frame,
            text="About",
            command=lambda: controller.show_frame("SplashScreen"),
            highlightbackground="#3E4149",
            font=helv20,
            width=10,
        )
        about_button.pack(side=tk.RIGHT, anchor=tk.SE, padx=20, pady=(0, 10))


class ParameterPage(tk.Frame):
    def __init__(self, parent, controller, plid):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        add_logo_frame(self)
        title = re.sub(r"_segmentation", "", plid).title()
        tool_title = tk.Label(
            self, text=title, font=("Futura", title_font_size, "bold")
        )
        tool_title.pack()

        tool_information = (
            get_information(plid)
            + "Please click the help button and view the instructions before proceeding"
        )
        tool_description_label = tk.Label(self, text=tool_information, wraplength=800)
        tool_description_label.config(font=("Helvetica", text_font_size))
        tool_description_label.pack()

        ents = create_form(self, plid)
        buttonFont = tkFont.Font(family="Helvetica", size=form_button_text_size)
        viewer_btn = tk.Button(
            self,
            text="3D View",
            font=buttonFont,
            command=lambda e=ents: generate(e, plid, False),
        )
        viewer_btn.pack(side=tk.LEFT, anchor=tk.SE, padx=20, pady=10)

        external_2d_btn = tk.Button(
            self,
            text="2D View",
            font=buttonFont,
            state=tk.NORMAL if "Input" in ents else tk.DISABLED,
            command=lambda e=ents: external_2d_viewer.start(e["Input"].get()),
        )
        external_2d_btn.pack(side=tk.LEFT, anchor=tk.SE, padx=20, pady=10)

        ar_view_btn = tk.Button(
            self,
            text="AR View",
            font=buttonFont,
            state=tk.NORMAL
            if holo_registration_wrapper.is_supported(plid)
            else tk.DISABLED,
            command=lambda e=ents: generate(e, plid, True),
        )
        ar_view_btn.pack(side=tk.LEFT, anchor=tk.SE, padx=20, pady=10)

        help_btn = tk.Button(
            self, text="Help", font=buttonFont, command=lambda: help_box(plid),
        )
        help_btn.pack(side=tk.RIGHT, anchor=tk.SW, padx=20, pady=10)

        back_btn = tk.Button(
            self,
            text="Back",
            font=buttonFont,
            command=lambda: controller.show_frame("StartPage"),
        )
        back_btn.pack(side=tk.RIGHT, anchor=tk.SW, padx=20, pady=10)


class SplashScreen(tk.Frame):
    def __init__(self, parent, controller, next_screen_func):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<Button-1>", next_screen_func)
        self.title_font = tkfont.Font(
            family="Helvetica", size=18, weight="bold", slant="italic"
        )

        add_logo_frame(self)

        image = Image.open(os.path.join("./core/client/images/hologram_icon.png"))
        image = image.resize((150, 150), Image.ANTIALIAS)
        tk_img = ImageTk.PhotoImage(image)
        imgLbl = tk.Label(self, image=tk_img)
        imgLbl.image = tk_img
        imgLbl.bind("<Button-1>", next_screen_func)
        imgLbl.pack(anchor=tk.CENTER, pady=(50, 20))

        lbl1 = tk.Label(
            self,
            text="""\n
        This 2020 edition of the HoloRepository, HoloPipelines and HoloRegistration components is intended for local PC/Laptop viewing of CT/MRI scans in 3D. Further editions for Azure, HoloLens 2 and for Intel™ Technologies including the Intel NUC platforms are available on holorepository.com and https://github.com/AppertaFoundation/HoloRepository-2020.
        \n
        Main authors: Immanuel Baskaran, Abhinath Kumar, Carlo Winkelhake, Daren Alfred
        Supervisors: Prof. Dean Mohamedally, Prof. Neil Sebire, Sheena Visram
        """,
            wraplength=900,
        )
        lbl2 = tk.Label(
            self,
            text="""
        Disclaimer: This system is a Proof of Concept, provided as is, and not for redeployment or use in medical scenarios without further development. It does not meet any medical guidelines and is intended to show potential usage and design for future workflows of using Holographics and 3D imaging of CT scans. Use at your own risk.
        \n\n
        Built at University College London in cooperation with Intel and GOSH DRIVE.
        It is licenced for open source use under AGPLv3.
        """,
            wraplength=900,
        )
        lbl1.bind("<Button-1>", next_screen_func)
        lbl1.config(font=("Helvetica", text_font_size))
        lbl1.pack(anchor=tk.CENTER, pady=(0, 5))
        lbl2.bind("<Button-1>", next_screen_func)
        lbl2.config(font=("Helvetica", text_font_size - 3))
        lbl2.pack(anchor=tk.CENTER, pady=0)


if __name__ == "__main__":
    app = ViewerApp()
    # def next_screen_func(app):
    # app.show_frame("StartPage")
    # app.after(10000, lambda: call_mainroot(app))
    app.mainloop()
