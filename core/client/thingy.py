import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.helv20 = tkfont.Font(family='Helvetica', size=20)
        self.state("zoomed")
        self.title("HoloPipelinesLocal")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="HoloPipelinesLocal")
        title.config(font=("Courier", 44))
        title.pack(pady=20)

        description="""
                This tool will open a CT/MRI scan, identify key anatomical structures, and extract them. The structures can then be viewable
                through a 3D model viewer or an AR viewer. The tool uses local versions of the HoloPipelines.
                Please select one of the pipelines to launch
                """
        description_label = tk.Label(self, text=description, wraplength='500')
        description_label.config(font=('Helvetica', 15, 'bold'))
        description_label.pack(side=tk.TOP,pady=10)
            
        
        button = tk.Button(self, text="Bone",command=None, highlightbackground='#3E4149', font=self.helv20)
        button.pack(pady=10)

        button2 = tk.Button(self, text="Lung",command=None, highlightbackground='#3E4149', font=self.helv20)
        button2.pack(pady=10)

        button3 = tk.Button(self, text="Kidney",command=None, highlightbackground='#3E4149', font=self.helv20)
        button3.pack(pady=10)

        button4 = tk.Button(self, text="Abdominal",command=None, highlightbackground='#3E4149', font=self.helv20)
        button4.pack(pady=10)

        button5 = tk.Button(self, text="Brain",command=None, highlightbackground='#3E4149', font=self.helv20)
        button5.pack(pady=10)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()