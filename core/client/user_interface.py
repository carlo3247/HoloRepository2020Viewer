import logging
import re
import os
import tkinter as tk  # python 3
from PIL import Image, ImageTk
from tkinter import font as tkfont  # python 3
from tkinter import messagebox
from tkinter import font as tkFont
from tkinter import filedialog


from core.pipelines.pipelines_controller import (
    get_pipeline_description,
    load_pipeline_dynamically,
)
from models.model_controller import (
    get_seg_types,
    get_file_types,
    get_req_modalities,
    get_proc_seg_types,
)


def get_information(plid):
    pipeline_description = get_pipeline_description(plid)
    model_file_types = get_file_types(plid)
    model_req_mods = get_req_modalities(plid)

    information = (
        pipeline_description + "\n\nInput must be " + " or ".join(model_file_types)
    )
    return (
        information
        if plid != "brain_segmentation"
        else information
        + "\n3 input scans (modalities) required of types "
        + ", ".join(model_req_mods)
        + "\n"
    )


def generate(entries, plid):
    output_path = entries["Output File"].get()
    segment_type = list(entries["seg_types"].curselection())
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
        logging.info("Loading and initializing bone pipeline dynamically")
        pipeline_module = load_pipeline_dynamically(plid)
        pipeline_module.run(input_dir, output_path, segment_type)
        logging.info("Done.")


def browsefunc(entry):
    folder_selected = filedialog.askdirectory()
    entry.insert(tk.END, folder_selected)


def browsefile(entry):
    file_selected = filedialog.askopenfilename(
        filetypes=(("Compressed NifTI", "*.nii.gz"), ("All files", "*"))
    )
    entry.insert(tk.END, file_selected)


def create_form(root, plid):
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
        input_row = tk.Frame(root)
        input_ent = tk.Entry(input_row)
        input_lab = tk.Label(
            input_row,
            width=15,
            text="Input",
            anchor="w",
            font=("Helvetica", 15, "bold"),
        )
        input_lab.pack(side=tk.LEFT)
        input_row.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx=5, pady=5)
        input_ent.pack(
            side=tk.LEFT, expand=tk.YES, fill=tk.X,
        )
        browse_button = tk.Button(
            input_row,
            text="Browse Input File",
            font=40,
            command=lambda: browsefile(input_ent),
        )
        browse_dir_button = tk.Button(
            input_row,
            text="Browse Input Directory",
            font=40,
            command=lambda: browsefunc(input_ent),
        )
        browse_button.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        browse_dir_button.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        entries["Input"] = input_ent
    else:
        input_row = tk.Frame(root)
        input_ent = tk.Entry(input_row)
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
            side=tk.LEFT, expand=tk.YES, fill=tk.X,
        )
        browse_button = tk.Button(
            input_row,
            text="Browse Input File",
            font=40,
            command=lambda: browsefile(input_ent),
        )
        browse_dir_button = tk.Button(
            input_row,
            text="Browse Input Directory",
            font=40,
            command=lambda: browsefunc(input_ent),
        )
        browse_button.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        browse_dir_button.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        entries["Flair Input"] = input_ent

        input_row_2 = tk.Frame(root)
        input_ent_2 = tk.Entry(input_row_2)
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
            side=tk.LEFT, expand=tk.YES, fill=tk.X,
        )
        browse_button_2 = tk.Button(
            input_row_2,
            text="Browse Input File",
            font=40,
            command=lambda: browsefile(input_ent_2),
        )
        browse_dir_button_2 = tk.Button(
            input_row_2,
            text="Browse Input Directory",
            font=40,
            command=lambda: browsefunc(input_ent_2),
        )
        browse_button_2.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        browse_dir_button_2.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        entries["T1 Input"] = input_ent_2

        input_row_3 = tk.Frame(root)
        input_ent_3 = tk.Entry(input_row_3)
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
            side=tk.LEFT, expand=tk.YES, fill=tk.X,
        )
        browse_button_3 = tk.Button(
            input_row_3,
            text="Browse Input File",
            font=40,
            command=lambda: browsefile(input_ent_3),
        )
        browse_dir_button_3 = tk.Button(
            input_row_3,
            text="Browse Input Directory",
            font=40,
            command=lambda: browsefunc(input_ent_3),
        )
        browse_button_3.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        browse_dir_button_3.pack(side=tk.RIGHT, fill=tk.X, padx=20)
        entries["IR Input"] = input_ent_3

    output_row = tk.Frame(root)
    output_lab = tk.Label(
        output_row,
        width=15,
        text="Output File",
        anchor="w",
        font=("Helvetica", 15, "bold"),
    )
    out_ent = tk.Entry(output_row)
    out_ent.insert(tk.END, "output.glb")
    output_row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    output_lab.pack(side=tk.LEFT)
    out_ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries["Output File"] = out_ent

    next_row = tk.Frame(root)
    seg_types = get_seg_types(plid).keys()

    next_row = tk.Frame(root)
    next_row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    type_label = tk.Label(
        next_row,
        text="Please select one or more types",
        anchor="w",
        font=("Helvetica", 15, "bold"),
    )
    type_label.grid(row=0, column=0, padx=10)

    listbox = tk.Listbox(next_row, selectmode="multiple")
    for item in seg_types:
        listbox.insert(tk.END, item)
    listbox.grid(row=0, column=10, padx=10)
    entries["seg_types"] = listbox

    silence_log = tk.IntVar()
    silence_button = tk.Checkbutton(
        next_row, text="Silence logging ", variable=silence_log
    )
    silence_button.grid(row=0, column=40, padx=30)
    entries["silence_log"] = silence_log

    return entries


def help_box(plid):
    if plid != "brain_segmentation":
        messagebox.showinfo(
            "Help",
            """Input : Select a compressed NifTi file or directory containing DICOM scans through the file or folder browser\n\nOuput Directory: Specify the path to the output. e.g. path/output.glb\n\nType: Specify the segmentation/s to be generated """,
        )
    else:
        messagebox.showinfo(
            "Help",
            """Input : Select a compressed NifTi file or directory containing DICOM scans through the file or folder browser\n\n Inputs required: T2-Flair, T1, T1-Intermediate Representation scans\n\nOuput Directory: Specify the path to the output. e.g. path/output.glb\n\nType: Specify the segmentation/s to be generated """,
        )


def add_logo_frame(root):
    logo_path = "./core/client/logos"
    logo_frame = tk.Frame(root)
    for logo in os.listdir(logo_path):
        image = Image.open(os.path.join(logo_path, logo))
        image = image.resize((100, 100), Image.ANTIALIAS)
        simg = ImageTk.PhotoImage(image)
        my = tk.Label(logo_frame, image=simg)
        my.image = simg
        my.pack(side=tk.LEFT, padx=20, pady=50)
    logo_frame.pack(anchor=tk.NW, padx=0.5, pady=0.5)


class ViewerApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

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

        plids = [
            "brain_segmentation",
            "lung_segmentation",
            "kidney_segmentation",
            "bone_segmentation",
            "abdominal_organs_segmentation",
        ]

        self.frames = {}
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

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller, plids):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        add_logo_frame(self)

        title = tk.Label(self, text="HoloPipelines 2020 Viewer")
        title.config(font=("Futura", 44, "bold"))
        title.pack(pady=20)

        description = """
            This tool will open a CT/MRI scan, identify key anatomical structures, and extract them. The structures becomes viewable
            through a 3D model viewer or an AR viewer. The tool uses local versions of the HoloPipelines.
            Please select one of the pipelines to launch
            """
        description_label = tk.Label(self, text=description)
        description_label.config(font="Helvetica 13 bold")
        description_label.pack(anchor=tk.CENTER, pady=10)

        menu_1_label = tk.Label(self, text="Generate from scan:")
        menu_1_label.config(font="Helvetica 13 bold")
        menu_1_label.pack(anchor=tk.CENTER, pady=10)

        helv20 = tkFont.Font(family="Helvetica", size=20)

        for plid in plids:
            title = re.sub(r"_segmentation", "", plid).title()
            button = tk.Button(
                self,
                text=title,
                command=lambda p=plid: controller.show_frame(p),
                highlightbackground="#3E4149",
                font=helv20,
                width=20,
            )
            button.pack(pady=10)

        menu_2_label = tk.Label(self, text="View existing model:")
        menu_2_label.config(font="Helvetica bold")
        menu_2_label.pack(anchor=tk.CENTER, pady=10)

        view_button = tk.Button(
            self,
            text="Open viewer",
            command=lambda p=plid: controller.show_frame(p),
            highlightbackground="#3E4149",
            font=helv20,
            width=20,
        )
        view_button.pack(pady=10)


class ParameterPage(tk.Frame):
    def __init__(self, parent, controller, plid):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title = re.sub(r"_segmentation", "", plid).title()
        tool_title = tk.Label(self, text=title, font=("Futura", 44, "bold"))
        tool_title.pack(pady=20)

        tool_information = get_information(plid)
        tool_description_label = tk.Label(self, text=tool_information, wraplength=500)
        tool_description_label.pack()

        ents = create_form(self, plid)
        buttonFont = tkFont.Font(family="Helvetica", size=28)
        b1 = tk.Button(self, text="3D View", command=lambda e=ents: generate(e, plid),)
        b1.pack(side=tk.LEFT, padx=20, pady=50)
        b2 = tk.Button(self, text="AR View", command=None)
        b2.pack(side=tk.LEFT, padx=20, pady=50)
        b3 = tk.Button(self, text="Help", command=lambda: help_box(plid),)
        b3.pack(side=tk.RIGHT, padx=20, pady=50)
        b4 = tk.Button(
            self, text="Back", command=lambda: controller.show_frame("StartPage"),
        )
        b4.pack(side=tk.RIGHT, padx=20, pady=50)


class SplashScreen(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.state("zoomed")
        self.title_font = tkfont.Font(
            family="Helvetica", size=18, weight="bold", slant="italic"
        )

        # the container is where we'll stack a bunch of frames
        # on tk.TOP of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)

        self.title("tk")
        self.configure()

        add_logo_frame(self)

        lbl1 = tk.Label(
            self,
            text="""\n\n
        Main authors: Immanuel Baskaran, Abhinath Kumar, Carlo Winkelhake, Daren Alfred
        \n
        Supervisors: Prof. Dean Mohamedally, Prof. Neil Sebire
        \n\n
        Built at University College London in cooperation with Intel and GOSH DRIVE.
        """,
        )
        lbl1.config(font=("Helvetica", 13))
        lbl1.pack(anchor=tk.CENTER, pady=100)


if __name__ == "__main__":
    app = SplashScreen()

    def call_mainroot(app):
        app.destroy()
        app = ViewerApp()

    app.after(500, lambda: call_mainroot(app))
    app.mainloop()
