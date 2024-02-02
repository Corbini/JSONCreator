from tkinter import Canvas, PhotoImage, Text, Frame, Scrollbar
from source.button import Button

from source.frame.parameter import Parameter


def create_menu(self):
        self.options = Frame(
            self,
            bg = "#363131",
            width = 250,
            height=800
        )

        # self.options.place(x = 744, y = 0)
        self.options.pack(side='right', anchor='ne', fill='y')
        
        self.button_1 = Button(
            master=self.options,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.event_generate('<<tree_new>>'),
            relief="flat"
        )
        self.button_1.load_image("assets/frame_main/button_1.png")
        self.button_1.place(
            x=35,
            y=50.0,
            width=187.0,
            height=50.0
        )


        button_image_2 = PhotoImage(
            file="assets/frame_main/button_2.png")
        self.button_2 = Button(
            master=self.options,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.event_generate("<<load>>"),
        )
        
        self.button_2.load_image("assets/frame_main/button_2.png")
        self.button_2.place(
            x=35,
            y=266.66668701171875,
            width=187.0,
            height=50.0
        )

        self.button_3 = Button(
            master=self.options,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.event_generate("<<save_as>>"),
        )
        self.button_3.load_image("assets/frame_main/button_3.png")
        self.button_3.place(
            x=35,
            y=483.3333740234375,
            width=187.0,
            height=50.0
        )

        self.button_4 = Button(
            master=self.options,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.event_generate("<<quit>>"),
            relief="flat"
        )
        self.button_4.load_image("assets/frame_main/button_4.png")
        self.button_4.place(
            x=35,
            y=700.0,
            width=187.0,
            height=50.0
        )

        self.tree_canvas = Canvas(self)

        self.tree_canvas.pack(side='left', expand='True', fill='both', padx=10, pady=10)
        
        self.tree_frame = Frame(self.tree_canvas, padx=2, pady=2, borderwidth=0, relief='flat')

        self.scroll = Scrollbar(self, orient='vertical', command=self.tree_canvas.yview)
        self.tree_canvas.configure(yscrollcommand=self.scroll.set)

        self.tree_canvas.create_window((0, 0), window=self.tree_frame, anchor='nw')
        
        self.tree_frame.bind("<Configure>", lambda event: self.scroll_show(event))


def on_scrollwheel(self, event):
     self.tree_canvas.yview_scroll(int(-1*(event.delta/120)), "units")


def scroll_show(self, event):
    if event.widget is self.tree_canvas:
        canvas_height = event.height
    else:
        self.tree_canvas.update()
        canvas_height = self.tree_canvas.winfo_height()
    
    if event.widget is self.tree_frame:
        frame_height = event.height
    else:
        self.tree_frame.update()
        frame_height = self.tree_frame.winfo_height()

    if frame_height>canvas_height - 25:
        self.scroll.pack(side='right', fill='y')
            
        self.tree_canvas.configure(scrollregion = self.tree_canvas.bbox('all'))
        self.bind_all("<MouseWheel>", self.on_scrollwheel)
        self.tree_frame.bind("<Configure>", lambda event: self.scroll_hide(event))
        
def scroll_hide(self, event):
    if event.widget is self.tree_canvas:
        canvas_height = event.height
    else:
        self.tree_canvas.update()
        canvas_height = self.tree_canvas.winfo_height()
    
    if event.widget is self.tree_frame:
        frame_height = event.height
    else:
        self.tree_frame.update()
        frame_height = self.tree_frame.winfo_height()

    if frame_height<=canvas_height - 25:
        self.scroll.pack_forget()

        self.tree_canvas.unbind_all("<MouseWheel>")
        self.tree_canvas.yview_scroll(-100, "units")
        self.tree_frame.bind("<Configure>", lambda event: self.scroll_show(event))
    else:
        self.tree_canvas.configure(scrollregion = self.tree_canvas.bbox('all'))
