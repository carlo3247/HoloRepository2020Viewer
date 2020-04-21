try:
    from Tkinter import *
except ImportError:
    from tkinter import *
    from tkinter import messagebox


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
    if plid!='brain_segmentation':
        input_dir = entries['Input Directory'].get()
    else:
         flair_dir = entries['Flair Input Directory'].get()
         t1_dir = entries['T1 Input Directory'].get()
         ir_dir = entries['IR Directory'].get()
         input_dir=[flair_dir,t1_dir,ir_dir]

    output_path = entries['Output File'].get()
    segment_type=list(entries['seg_types'].curselection())
    quiet = entries['silence_log'].get()

   

    if input_dir=='' or output_path=='' or segment_type=='':
        messagebox.showerror("Error", "Please ensure an input directory, an output path, and segmentation type is inputted")
    else:
         pipeline_module = load_pipeline_dynamically(plid)
         pipeline_module.run(input_dir, output_path, segment_type)


def create_form(root, plid):
    fields=['Input Directory', 'Output File'] if plid !='brain_segmentation' else ['Flair Input Directory', 'T1 Input Directory', 'IR Input Directory', 'Output File']

    entries = {}
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=15, text=field, anchor='w',font=('Helvetica', 15, 'bold'))
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries[field]=ent
    
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


 
def parameter_window(tool:str,plid:str)->None:

    root.destroy()
    pipeline_window = Tk()
    if plid=="brain_segmentation":
        pipeline_window.geometry("700x700")
    else:
        pipeline_window.geometry("700x600")
    pipeline_window.title(tool)

    tool_title = Label(pipeline_window, text=tool,wraplength=500)
    tool_title.config(font=("Courier", 44))
    tool_title.pack(pady=20)

    tool_information = get_information(plid)
    tool_description_label = Label(pipeline_window, text=tool_information,wraplength=500)
    tool_description_label.pack()

    ents = create_form(pipeline_window, plid) 
    b1 = Button(pipeline_window, text='Generate', command=lambda e=ents: generate(e, plid))
    b1.pack(side=BOTTOM , padx=5, pady=50) 


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
    description_label.config(font=("Arial", 15))
    description_label.pack(pady=10,padx=10)
        
    button = Button(root, text="HoloBone",command=lambda: parameter_window("HoloBone", "bone_segmentation"), highlightbackground='#3E4149')
    button.pack(pady=10)

    button2 = Button(root, text="HoloLung",command=lambda: parameter_window("HoloLung", "lung_segmentation"), highlightbackground='#3E4149')
    button2.pack(pady=10)

    button3 = Button(root, text="HoloKidney",command=lambda: parameter_window("HoloKidney", "kidney_segmentation"), highlightbackground='#3E4149')
    button3.pack(pady=10)

    button4 = Button(root, text="HoloAbdominal",command=lambda: parameter_window("HoloAbdominal", "abdominal_organs_segmentation"), highlightbackground='#3E4149')
    button4.pack(pady=10)

    button5 = Button(root, text="HoloBrain",command=lambda: parameter_window("HoloBrain", "brain_segmentation"), highlightbackground='#3E4149')
    button5.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    root = Tk()
    root.geometry("700x500")
    root.title("HoloPipelinesLocal")
    main()