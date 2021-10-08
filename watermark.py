from PIL import Image


class Watermark:
    def __init__(self, path):
        self.image = Image.open(path)
        self.width, self.height = self.image.size
        self.convert_to_rgba()

    # This is needed to keep opacity and paste the watermark in the base image or PIL might raise an exception
    # ValueError: bad transparency mask
    def convert_to_rgba(self):
        """
        Convert the current image to RGBA mode.
        """
        if self.image.mode != "RGBA":
            self.image = self.image.convert("RGBA")
