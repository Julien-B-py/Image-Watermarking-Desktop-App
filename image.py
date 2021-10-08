import os

from PIL import Image


class Img:

    def __init__(self, path, watermark):
        self.watermark = watermark
        self.wm_width, self.wm_height = watermark.width, watermark.height

        self.image = Image.open(path)
        self.width, self.height = self.image.size
        self.image_path = path
        self.image_parent_folder = os.path.dirname(self.image_path)
        self.image_filename = os.path.basename(self.image_path)
        self.wm_position = {
            'default': (self.width - self.wm_width, self.height - self.wm_height),
            'top-left': (0, 0),
            'top-right': (self.width - self.wm_width, 0),
            'bottom-left': (0, self.height - self.wm_height),
            'center': ((self.width - self.wm_width) // 2, (self.height - self.wm_height) // 2),
        }

    def add_watermark(self, position=None):
        """
        Apply the selected watermark to our image.
            :param position: A position (string) to determine the watermark position in the final image. Default
                positioning is 'bottom-right'. You can also select 'top-left', 'top-right', 'bottom-left' or 'center'.
        """

        # Pastes watermark in the image.
        if not position:
            # Default position: bottom-right
            self.image.paste(im=self.watermark,
                             box=self.wm_position['default'],
                             mask=self.watermark)
        else:
            # Specific positioning
            self.image.paste(im=self.watermark,
                             box=self.wm_position.get(position, self.wm_position['default']),
                             mask=self.watermark)

        # Split the base filename from the file extension to add a suffix
        new_filename = self.image_filename.split('.')[0] + '_wm'
        file_extension = self.image_filename.split('.')[-1]
        # Create new filename with '_wm' suffix before file extension
        output_filename = new_filename + '.' + file_extension
        output_image_path = os.path.join(self.image_parent_folder, output_filename)
        # Save image
        self.image.save(output_image_path, quality=95)


if __name__ == '__main__':
    my_img = Img('test.jpg')
    my_img.add_watermark(position='center')
