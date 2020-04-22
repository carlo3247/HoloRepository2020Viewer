try:
    from Tkinter import *
except ImportError:
    from tkinter import *
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

    information = pipeline_description + "\n\nInput files must be of type " + " or ".join(model_file_types)
    return information if plid != "brain_segmentation" else information + "\n3 input scans (modalities) required of types " + ", ".join(model_req_mods)+'\n'

def generate(entries, plid):
    output_path = entries['Output File'].get()
    segment_type=list(entries['seg_types'].curselection())
    quiet = entries['silence_log'].get()

    if plid!='brain_segmentation':
        input_dir = entries['Input Directory'].get()
    else:
         flair_dir = entries['Flair Input Directory'].get()
         t1_dir = entries['T1 Input Directory'].get()
         ir_dir = entries['IR Input Directory'].get()
         input_dir=[flair_dir,t1_dir,ir_dir]

   
    if (plid == 'brain_segmentation' and '' in input_dir) or input_dir=='' or output_path=='' or not segment_type:
        messagebox.showerror("Error", "Please ensure input directory/ies, an output path, and segmentation type is inputted")
    else:
         pipeline_module = load_pipeline_dynamically(plid)
         pipeline_module.run(input_dir, output_path, segment_type)

def browsefunc(entry):
    folder_selected = filedialog.askdirectory()
    entry.insert(END, folder_selected) 

def create_form(root, plid):
    fields=['Input Directory', 'Output File'] if plid !='brain_segmentation' else ['Flair Input Directory', 'T1 Input Directory', 'IR Input Directory', 'Output File']

    entries = {}

    if(plid!='brain_segmentation'):
        input_row = Frame(root)
        input_ent = Entry(input_row)
        input_lab = Label(input_row, width=15, text='Input Directory', anchor='w',font=('Helvetica', 15, 'bold'))
        input_lab.pack(side=LEFT)
        input_row.pack(side=TOP,expand=YES, fill=X, padx=5, pady=5)
        input_ent.pack(side=LEFT)
        browse_button=Button(input_row,text="Browse Input Directory",font=40,command=lambda: browsefunc(input_ent))
        browse_button.pack(side=RIGHT,fill=X, padx=20)
        entries['Input Directory']=input_ent
    else:
        input_row = Frame(root)
        input_ent = Entry(input_row)
        input_lab = Label(input_row, width=15, text='Flair Input Directory', anchor='w',font=('Helvetica', 15, 'bold'))
        input_lab.pack(side=LEFT)
        input_row.pack(side=TOP,expand=YES, fill=X, padx=5, pady=5)
        input_ent.pack(side=LEFT)
        browse_button=Button(input_row,text="Browse Input Directory",font=40,command=lambda: browsefunc(input_ent))
        browse_button.pack(side=RIGHT,fill=X, padx=20)
        entries['Flair Input Directory']=input_ent

        input_row_2 = Frame(root)
        input_ent_2 = Entry(input_row_2)
        input_lab_2 = Label(input_row_2, width=15, text='T1 Input Directory', anchor='w',font=('Helvetica', 15, 'bold'))
        input_lab_2.pack(side=LEFT)
        input_row_2.pack(side=TOP,expand=YES, fill=X, padx=5, pady=5)
        input_ent_2.pack(side=LEFT)
        browse_button_2=Button(input_row_2,text="Browse Input Directory",font=40,command=lambda: browsefunc(input_ent_2))
        browse_button_2.pack(side=RIGHT,fill=X, padx=20)
        entries['T1 Input Directory']=input_ent_2

        input_row_3 = Frame(root)
        input_ent_3 = Entry(input_row_3)
        input_lab_3 = Label(input_row_3, width=15, text='IR Input Directory', anchor='w',font=('Helvetica', 15, 'bold'))
        input_lab_3.pack(side=LEFT)
        input_row_3.pack(side=TOP,expand=YES, fill=X, padx=5, pady=5)
        input_ent_3.pack(side=LEFT)
        browse_button_3=Button(input_row_3,text="Browse Input Directory",font=40,command=lambda: browsefunc(input_ent_3))
        browse_button_3.pack(side=RIGHT,fill=X, padx=20)
        entries['IR Input Directory']=input_ent_3
    
    output_row = Frame(root)
    output_lab = Label(output_row, width=15, text='Output File', anchor='w',font=('Helvetica', 15, 'bold'))
    out_ent = Entry(output_row)
    output_row.pack(side=TOP, fill=X, padx=5, pady=5)
    output_lab.pack(side=LEFT)
    out_ent.pack(side=RIGHT, expand=YES, fill=X)
    entries['Output File']=out_ent


    
    next_row = Frame(root)
    seg_types = get_seg_types(plid).keys()

    next_row = Frame(root)
    next_row.pack(side=TOP, fill=X, padx=5, pady=5)
    type_label = Label(next_row, text="Please select one or more types", anchor='w',font=('Helvetica', 15, 'bold'))
    type_label.grid(row=0,column=0,padx=10)

    listbox = Listbox(next_row ,selectmode = "multiple")
    for item in seg_types:
        listbox.insert(END, item)
    listbox.grid(row=0,column=10,padx=10)
    entries['seg_types']=listbox

    silence_log = IntVar()
    silence_button= Checkbutton(next_row, text="Silence logging ", variable=silence_log)
    silence_button.grid(row=0,column=40,padx=30)
    entries['silence_log']=silence_log

    return entries

def help_box(plid):
    if plid!="brain_segmentation":
        messagebox.showinfo("Help", """Input Directory: Select the directory containing the scans\n\nOuput Directory: Specify the path to the output. e.g. path/output.glb\n\nType: Specify the segmentation/s to be generated """)
    else:
        messagebox.showinfo("Help", """Input Directories: Select the directories containing the T2-Flair, T1, T1-Intermediate Representation scans\n\nOuput Directory: Specify the path to the output. e.g. path/output.glb\n\nType: Specify the segmentation/s to be generated """)
     
 
def parameter_window(tool:str,plid:str)->None:

    root.destroy()
    pipeline_window = Tk()
    # pipeline_window.resizable(False, False)
    if plid=="brain_segmentation":
        pipeline_window.geometry("700x700")
    else:
        pipeline_window.geometry("700x600")
    pipeline_window.title(tool)
    pipeline_window.configure(background='#62cbf5')

    tool_title = Label(pipeline_window, text=tool,wraplength=500)
    tool_title.config(font=("Courier", 44))
    tool_title.pack(pady=20)

    tool_information = get_information(plid)
    tool_description_label = Label(pipeline_window, text=tool_information,wraplength=500)
    tool_description_label.pack()

    ents = create_form(pipeline_window, plid) 
    buttonFont = tkFont.Font(family='Helvetica', size=28)
    b1 = Button(pipeline_window, text='Generate', command=lambda e=ents: generate(e, plid), font=buttonFont)
    b1.pack(side=LEFT , padx=20, pady=50) 
    b2 = Button(pipeline_window, text='Help', command=lambda: help_box(plid), font=buttonFont)
    b2.pack(side=RIGHT , padx=20, pady=50) 


    pipeline_window.mainloop()

def main():
    title = Label(root, text="HoloPipelinesLocal",wraplength=500)
    title.config(font=("Courier", 44))
    title.pack(pady=20)

    description="""
            This is a tool that launches the local versions of the HoloPipelines.
            Please select one of the pipelines to launch
            """
    description_label = Label(root, text=description)
    description_label.config(font=('Helvetica', 15, 'bold'),background='#62cbf5')
    description_label.pack(side=TOP,pady=10)
        
    helv20 = tkFont.Font(family='Helvetica', size=20)
    button = Button(root, text="HoloBone",command=lambda: parameter_window("HoloBone", "bone_segmentation"), highlightbackground='#3E4149', font=helv20)
    button.pack(pady=10)

    button2 = Button(root, text="HoloLung",command=lambda: parameter_window("HoloLung", "lung_segmentation"), highlightbackground='#3E4149', font=helv20)
    button2.pack(pady=10)

    button3 = Button(root, text="HoloKidney",command=lambda: parameter_window("HoloKidney", "kidney_segmentation"), highlightbackground='#3E4149', font=helv20)
    button3.pack(pady=10)

    button4 = Button(root, text="HoloAbdominal",command=lambda: parameter_window("HoloAbdominal", "abdominal_organs_segmentation"), highlightbackground='#3E4149', font=helv20)
    button4.pack(pady=10)

    button5 = Button(root, text="HoloBrain",command=lambda: parameter_window("HoloBrain", "brain_segmentation"), highlightbackground='#3E4149', font=helv20)
    button5.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    root = Tk()
    root.geometry("700x500")
    # root.resizable(False, False)
    root.title("HoloPipelinesLocal")
    root.configure(background='#62cbf5')
    main()