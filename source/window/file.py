from tkinter import filedialog as fd

def load() -> str:
    filetypes = (
        ('meter files', '*.json'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='',
        filetypes=filetypes)

    print(
        'Selected File: ',
        filename
    )
    return filename

def save_as() -> str:
    filetypes = (
        ('meter files', '*.json'),
        ('All files', '*.*')
    )

    filename = fd.asksaveasfilename(
        title='Select a file',
        initialdir='',
        filetypes=filetypes)

    print(
        'Selected File: ',
        filename
    )
    return filename