from tkinter import Frame, Canvas, Scrollbar


class Device():
    def __init__(self, frame):
        
        self.canvas = Canvas(frame, relief='flat', borderwidth=0)

        self.canvas.pack(expand='True', fill='both', padx=10, pady=10)

        self.frame = Frame(self.canvas, padx=15, pady=15, borderwidth=0, relief='flat')

        self.scroll_horizontal = Scrollbar(self.canvas, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scroll_horizontal.set)
        self.scroll_horizontal_state = False
        
        self.scroll_vertical = Scrollbar(self.canvas, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_vertical.set)
        self.scroll_vertical_state = False

        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        
        self.canvas.bind("<Configure>", self.canvas_update)
        self.frame.bind("<Configure>", self.frame_update)


    def on_scrollwheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_horizontal_scroll(self, frame_width, canvas_width):
        if self.scroll_horizontal_state:
            if frame_width<=canvas_width - 25:
                self.canvas.xview_moveto('0.0')
                self.scroll_horizontal.pack_forget()
                self.scroll_horizontal_state = False
            else:
                self.canvas.configure(scrollregion = self.canvas.bbox('all'))
        elif frame_width>canvas_width - 25:
            self.scroll_horizontal.pack(side='bottom', fill='x', anchor='sw')
            self.canvas.configure(scrollregion = self.canvas.bbox('all'))
            self.scroll_horizontal_state = True

    def update_vertical_scroll(self, frame_height, canvas_height):
        if self.scroll_vertical_state:
            if frame_height<=canvas_height - 25:
                self.scroll_vertical.pack_forget()
                self.canvas.yview_moveto('0.0')
                self.canvas.unbind_all("<MouseWheel>")
                self.scroll_vertical_state = False
            else:
                self.canvas.configure(scrollregion = self.canvas.bbox('all'))
        elif frame_height>canvas_height - 25:
            self.canvas.bind_all("<MouseWheel>", self.on_scrollwheel)
            self.scroll_vertical.pack(side='right', fill='y')
            self.canvas.configure(scrollregion = self.canvas.bbox('all'))
            self.scroll_vertical_state = True

    def scroll_update(self, event):
        if event.widget is self.canvas:
            canvas_height = event.height
            canvas_width = event.width
        else:
            self.canvas.update() 
            canvas_height = self.canvas.winfo_height()
            canvas_width = self.canvas.winfo_width()
        
        if event.widget is self.frame:
            frame_height = event.height
            frame_width = event.width
        else:
            self.frame.update()
            frame_height = self.frame.winfo_height()
            frame_width = self.frame.winfo_width()

        self.update_horizontal_scroll(frame_width, canvas_width)  

        self.update_vertical_scroll(frame_height, canvas_height)          
    
    def canvas_update(self, event):
        canvas_height = event.height
        canvas_width = event.width
        
        self.frame.update()
        frame_height = self.frame.winfo_height()
        frame_width = self.frame.winfo_width()

        self.update_horizontal_scroll(frame_width, canvas_width)  

        self.update_vertical_scroll(frame_height, canvas_height)     

    def frame_update(self, event):
        self.canvas.update() 
        canvas_height = self.canvas.winfo_height()
        canvas_width = self.canvas.winfo_width()
        
        frame_height = event.height
        frame_width = event.width

        self.update_horizontal_scroll(frame_width, canvas_width)  

        self.update_vertical_scroll(frame_height, canvas_height)
