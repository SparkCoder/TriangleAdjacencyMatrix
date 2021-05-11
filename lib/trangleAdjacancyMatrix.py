import matplotlib.pyplot as plt
import numpy as np

from PIL import Image, ImageDraw, ImageFont

import threading
import os


class TriangleAdjacencyMatrix:
    def __init__(self, **kwargs):
        self.width = self.__set_kwarg('width', kwargs, 1024)
        self.border = self.__set_kwarg('border', kwargs, 50)

        self.line_color = self.__set_kwarg('line_color', kwargs, '#020202')
        self.thickness = self.__set_kwarg('thickness', kwargs, 30)
        self.font = self.__set_kwarg('font', kwargs, ImageFont.load_default())
        self.icons = self.__set_kwarg(
            'icons', kwargs, [Image.new('RGBA', (512, 512), (255, 0, 0, 255))] * 4)

        self.items = self.__set_kwarg('items', kwargs, ['item 1, item 2'])

        n_items = len(self.items)
        self.matrix = self.__set_kwarg(
            'matrix', kwargs, np.array([[0] * n_items] * n_items))

    def __set_kwarg(_, arg, kwargs, default=None):
        if arg in kwargs:
            return kwargs[arg]
        return default

    def generate(self):
        width = self.width - (self.border * 2)
        height = self.width - (self.border * 2)

        gen = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        img = Image.new("RGBA", (self.width, self.width), (0, 0, 0, 0))
        canvas = ImageDraw.Draw(gen)

        n_items = len(self.items)
        label_width = min(10 * self.font.size, width / 2)

        cell_size = height / n_items
        half_cell_size = cell_size / 2
        half_height = height / 2

        # Grid
        for row in range(n_items):
            y_start = (cell_size * row)
            x_end = half_height - (y_start / 2)
            y_end = half_height + (y_start / 2)
            canvas.line([
                (label_width,  y_start),
                (label_width + x_end, y_end)
            ], fill=self.line_color, width=self.thickness)
            canvas.line([
                (label_width,  height - y_start),
                (label_width + x_end, height - y_end)
            ], fill=self.line_color, width=self.thickness)

            if row < n_items - 1:
                for col in range(n_items - row - 1):
                    sec = (cell_size * col)
                    x_pos = (half_cell_size * 0.5) + (sec / 2)
                    y_pos = (half_cell_size * 1.5) + \
                        (sec / 2) + (cell_size * row)

                    x_index = col + row + 1
                    y_index = row

                    icon = self.icons[self.matrix[y_index, x_index]]
                    icon = icon.resize((int(half_cell_size), int(half_cell_size)),
                                       resample=Image.ANTIALIAS)
                    gen.paste(
                        icon, (int(label_width + x_pos), int(y_pos)), icon)

        # Label lines
        for row in range(n_items + 1):
            y_start = (cell_size * row) + (self.thickness * 0.5 if row ==
                                           0 else (self.thickness * (-0.5) if row == n_items else 0))
            canvas.line([
                (0,  y_start),
                (label_width, y_start)
            ], fill=self.line_color, width=self.thickness)

        # Labels
        for row in range(n_items):
            y_start = (cell_size * row)
            canvas.text((0, y_start - (self.font.size / 2) + half_cell_size),
                        self.items[row], font=self.font, align="left", fill=self.line_color)

        gen = gen.resize(gen.size, Image.ANTIALIAS)
        img.paste(gen, (self.border, self.border))
        img = img.resize(img.size, Image.ANTIALIAS)

        return img


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))

    width = 2048
    thickness = 30
    font = ImageFont.truetype(os.path.join(
        dir_path, 'ui', 'fonts', 'Poppins-Bold.ttf'), 80)
    line_color = '#020202'
    items = [
        'Parking',
        'Entry gate',
        'lobby & reception',
        'Admin. office',
        'R&D block',
        'Multi-purpose hall',
        'Gallery block',
        'Library',
        'Conference hall',
        'Amphitheatre',
        'Meeting area'
    ]

    tam = TriangleAdjacencyMatrix(
        width=width, thickness=thickness, font=font, line_color=line_color, items=items)
    img = tam.generate()

    plt.imshow(np.asarray(img))
    plt.show()
