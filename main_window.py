from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox

from image import Img
from settings import FORMATS, POSITIONS
from watermark import Watermark


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.config_window()
        self.create_widgets()
        self.setup_widgets_layout()
        self.all_images = []
        # Window display
        self.mainloop()

    def config_window(self):
        self.title("Image Watermarking")
        self.resizable(False, False)
        self.config(pady=20, padx=20)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        self.top_label = Label(self, text="Protect Your Images", height=4, fg="blue")
        self.top_label.config(font=("Arial", 15))
        self.files_list = Listbox(self, width=54, activestyle=None)
        self.browse_button = Button(text="Browse", width=12, command=self.add_image)
        self.select_all_button = Button(text="Delete all", width=12, command=self.delete_all)
        self.start_button = Button(text="Start", width=12, command=self.run_watermarking)
        self.wm_pos_label = Label(self, text='Watermark position: ')
        self.wm_pos_combobox = Combobox(self, values=POSITIONS, text='test', state='readonly', width=10)
        # Set index 0 as active combobox item
        self.wm_pos_combobox.current(0)
        self.watermark_button = Button(text="Select your watermark image", width=25, command=self.load_watermark_image)

    def setup_widgets_layout(self):
        self.top_label.grid(row=0, column=0, columnspan=3)
        self.watermark_button.grid(row=1, columnspan=3, pady=10)
        self.files_list.grid(row=2, column=0, columnspan=3)
        self.browse_button.grid(row=3, column=0, pady=10, sticky=W)
        self.select_all_button.grid(row=3, column=1)
        self.start_button.grid(row=3, column=2, sticky=E)
        self.wm_pos_label.grid(row=4, column=1, sticky=E)
        self.wm_pos_combobox.grid(row=4, column=2, sticky=E)

    def on_closing(self):
        """
        When clicking on closing button make sure the user is willing to close the app.
        """
        # If user press 'OK' exit app
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def load_watermark_image(self):
        """
        Allow the user to select the image to apply as watermark.
        """
        file = filedialog.askopenfilename(initialdir="/",
                                          filetypes=[("Image files", FORMATS)])

        # If any file has been selected
        if file:
            # Create a Watermark object and display a messagebox
            self.wm = Watermark(file).image
            messagebox.showinfo(title='Information', message='Watermark file successfully loaded.')

    def add_image(self):
        """
        Allow the user to select and add images to watermark to the listbox.
        """

        # If watermark file has not been chosen yet
        if not hasattr(self, 'wm'):
            messagebox.showinfo(title='Information', message='Please load your watermark file first.')
            return

        # Open a file dialog window to select multiple image files
        filenames = filedialog.askopenfilenames(initialdir="/",
                                                filetypes=[("Image files", FORMATS)])

        # If any file has been selected
        if filenames:
            for filename in filenames:
                # Add the file absolut path to listbox
                self.files_list.insert(END, filename)
                # Create an Img object and add it to all_images list
                img = Img(filename, self.wm)
                self.all_images.append(img)

    def run_watermarking(self):
        """
        Perform the watermarking process on selected images.
        """
        # If no image to deal with show a messagebox
        if not self.all_images:
            messagebox.showinfo(title='Information', message='Please add at least one image')
            return

        # Loop through all Img objects and apply watermark using the specified position from the combobox
        for image in self.all_images:
            image.add_watermark(position=self.get_specified_watermark_pos())

        # Clear the images listbox and all Img objects stored in all_images
        # Then show a message when process is completed
        self.delete_all()
        messagebox.showinfo(title='Success', message='Watermarking process completed!')

    def delete_all(self):
        """
        Clear the images listbox and all Img objects stored in all_images.
        """

        # If listbox is already empty show a messagebox
        if self.files_list.size() == 0:
            messagebox.showinfo(title='Information', message='The list is already empty.')
            return

        self.files_list.delete('0', 'end')
        self.all_images.clear()

    def get_specified_watermark_pos(self):
        """
        Get the current 'Watermark position' string value from the combobox.
            :returns: A lower-case position (string) to determine the watermark position in the final image.
        """
        return self.wm_pos_combobox.get().lower()


if __name__ == '__main__':
    window = MainWindow()
    window.mainloop()
