import tkinter as tk

from core.pipelines.pipelines_controller import (
    get_pipeline_description,
    load_pipeline_dynamically,
)
from models.model_controller import get_seg_types, get_file_types, get_proc_seg_types


LARGE_FONT= ("Verdana", 12)


class HoloPipelinesInterface(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (PipelinePage, parameterPage, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PipelinePage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class PipelinePage(tk.Frame):


    def __init__(self, parent, controller):
        description="""
        This is a tool to use the local version of the HoloPipelines.
        Please select one of the pipelines to proceed
        """
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=description, font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Bones",
                            command=lambda: controller.show_frame(parameterPage), highlightbackground='#3E4149')
        button.pack()

        button2 = tk.Button(self, text="Lung",
                            command=lambda: controller.show_frame(PageTwo), highlightbackground='#3E4149')
        button2.pack()

        button3 = tk.Button(self, text="Kidney",
                            command=lambda: controller.show_frame(PageTwo), highlightbackground='#3E4149')
        button3.pack()

        button4 = tk.Button(self, text="Abdominal",
                            command=lambda: controller.show_frame(PageTwo), highlightbackground='#3E4149')
        button4.pack()

        button5 = tk.Button(self, text="Brain",
                            command=lambda: controller.show_frame(PageTwo), highlightbackground='#3E4149')
        button5.pack()


class parameterPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(PipelinePage), highlightbackground='#3E4149')
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo), highlightbackground='#3E4149')
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(PipelinePage), highlightbackground='#3E4149')
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne), highlightbackground='#3E4149')
        button2.pack()
        


app = HoloPipelinesInterface()
app.wm_geometry("700x500")
app.mainloop()