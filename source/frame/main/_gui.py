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

        self.tree_canvas = Canvas(self, relief='flat', borderwidth=0)

        self.tree_canvas.pack(expand='True', fill='both', padx=10, pady=10)

        self.tree_frame = Frame(self.tree_canvas, padx=15, pady=15, borderwidth=0, relief='flat')

        self.scroll_horizontal = Scrollbar(self.tree_canvas, orient='horizontal', command=self.tree_canvas.xview)
        self.tree_canvas.configure(xscrollcommand=self.scroll_horizontal.set)
        self.scroll_horizontal_state = False
        
        self.scroll_vertical = Scrollbar(self.tree_canvas, orient='vertical', command=self.tree_canvas.yview)
        self.tree_canvas.configure(yscrollcommand=self.scroll_vertical.set)
        self.scroll_vertical_state = False

        self.tree_canvas.create_window((0, 0), window=self.tree_frame, anchor='nw')
        
        self.tree_canvas.bind("<Configure>", self.scroll_update)
        self.tree_frame.bind("<Configure>", self.scroll_update)

def on_scrollwheel(self, event):
     self.tree_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def scroll_update(self, event):
    if event.widget is self.tree_canvas:
        canvas_height = event.height
        canvas_width = event.width
    else:
        self.tree_canvas.update()
        canvas_height = self.tree_canvas.winfo_height()
        canvas_width = self.tree_canvas.winfo_width()
    
    if event.widget is self.tree_frame:
        frame_height = event.height
        frame_width = event.width
    else:
        self.tree_frame.update()
        frame_height = self.tree_frame.winfo_height()
        frame_width = self.tree_frame.winfo_width()

    if self.scroll_horizontal_state:
        if frame_width<=canvas_width - 25:
            self.scroll_horizontal.pack_forget()
            self.tree_canvas.xview_scroll(0, "units")
            self.scroll_horizontal_state = False
        else:
            self.tree_canvas.configure(scrollregion = self.tree_canvas.bbox('all'))
    elif frame_width>canvas_width - 25:
        self.scroll_horizontal.pack(side='bottom', fill='x', anchor='sw')
        self.tree_canvas.configure(scrollregion = self.tree_canvas.bbox('all'))
        self.scroll_horizontal_state = True
        
 
    if self.scroll_vertical_state:
        if frame_height<=canvas_height - 25:
            self.scroll_vertical.pack_forget()

            self.tree_canvas.unbind_all("<MouseWheel>")
            self.tree_canvas.yview_scroll(0, "units")
            self.scroll_vertical_state = False
        else:
            self.tree_canvas.configure(scrollregion = self.tree_canvas.bbox('all'))
    elif frame_height>canvas_height - 25:
        self.bind_all("<MouseWheel>", self.on_scrollwheel)
        self.scroll_vertical.pack(side='right', fill='y')
        self.tree_canvas.configure(scrollregion = self.tree_canvas.bbox('all'))
        self.scroll_vertical_state = True
