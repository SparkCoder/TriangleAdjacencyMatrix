from PIL import ImageFont
from PIL import ImageQt
from PIL import Image

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLabel, QListWidgetItem
from PySide2.QtCore import QFile, QObject
from PySide2.QtCore import Qt as Qt
from PySide2.QtGui import QIcon, QPixmap

from lib.labelListItem import LabelListItem

from lib.trangleAdjacancyMatrix import TriangleAdjacencyMatrix

import numpy as np

import sys
import os

# import resources
from lib.ui import res_rc

# Globals
app_root = os.path.dirname(os.path.realpath(__file__))


class App(QObject):
    __instance = None

    def __init__(self, ui_file_name, title, parent=None):
        super(App, self).__init__(parent)

        # Singleton
        if App.__instance is None:
            App.__instance = self
        elif App.__instance != self:
            raise Exception('Cannot spawn multiple App windows!')

        # Setup
        self.current_marker = -1
        self.kinds = [
            QIcon(':/icons/icons/adjacent.png'),
            QIcon(':/icons/icons/not_adjacent.png'),
            QIcon(':/icons/icons/not_related.png'),
            QIcon(':/icons/icons/related_not_adjacent.png'),
        ]
        self.labels = [
            'item 1',
            'item 2',
            'item 3'
        ]
        self.__generate_matrix(rewamp=True)
        self.__generate_compute()
        self.__load_ui(ui_file_name, title)

        self.__update_matrix()

        self.window.labels.clear()
        for label in self.labels:
            self.__add_label(label, list_update=False)

        # Events
        self.window.addLabelBtn.clicked.connect(self.add_label_event)

        self.window.adjacentBtn.clicked.connect(
            lambda: self.set_current_marker_event(0))
        self.window.notAdjacentBtn.clicked.connect(
            lambda: self.set_current_marker_event(1))
        self.window.notRelatedBtn.clicked.connect(
            lambda: self.set_current_marker_event(2))
        self.window.relatedNotAdjacentBtn.clicked.connect(
            lambda: self.set_current_marker_event(3))

    def set_current_marker_event(self, index):
        self.current_marker = index

    def set_marker_event(self, row, col):
        if 0 <= self.current_marker and self.current_marker <= 3:
            self.matrix[row, col] = self.current_marker
            self.matrix[col, row] = self.current_marker
            self.__update_matrix()

    def add_label_event(self):
        # Add label and restructure matrix
        self.__add_label('item ' + str(len(self.labels) + 1))
        self.__generate_matrix()
        self.__update_matrix()

    def __generate_compute(self):
        width = 1024
        thickness = 30
        font = ImageFont.truetype(os.path.join(
            app_root, 'lib', 'ui', 'fonts', 'Poppins-Bold.ttf'), 80)
        line_color = '#020202'
        icons_path = os.path.join(app_root, 'lib', 'ui', 'icons')
        icons = [
            Image.open(os.path.join(icons_path, 'adjacent.png')),
            Image.open(os.path.join(icons_path, 'not_adjacent.png')),
            Image.open(os.path.join(icons_path, 'not_related.png')),
            Image.open(os.path.join(icons_path, 'related_not_adjacent.png'))
        ]
        self.tam = TriangleAdjacencyMatrix(
            width=width, thickness=thickness, font=font, line_color=line_color, icons=icons)

    def __compute_image(self):
        self.tam.matrix = self.matrix
        self.tam.items = self.labels

        img = self.tam.generate()

        h = self.window.generated.height()
        print(img.size)
        # img.resize((img.size[0] * (h // img.size[1]), h),
        #           resample=Image.ANTIALIAS)

        image = ImageQt.ImageQt(img)
        pixmap = QPixmap()
        pixmap.convertFromImage(image)

        self.window.generated.setPixmap(pixmap.copy())
        self.window.generated.show()

    def __add_label(self, label, list_update=True):
        # Update label list
        if list_update:
            self.labels.append(label)

        # Add label entry
        item = QListWidgetItem(self.window.labels)
        self.window.labels.addItem(item)

        # Add label widget
        row = LabelListItem(label)
        row.item = item
        row.change_callback = self.change_label_event
        row.delete_callback = self.delete_label_event
        self.window.labels.setItemWidget(item, row)

    def delete_label_event(self, item):
        self.__delete_label(item)
        self.__generate_matrix()
        self.__update_matrix()

    def __delete_label(self, item):
        index = self.window.labels.row(item)
        self.labels.pop(index)
        self.window.labels.takeItem(index)

    def change_label_event(self, item, name):
        self.__change_label(item, name)
        self.__update_matrix()

    def __change_label(self, item, name):
        index = self.window.labels.row(item)
        self.labels[index] = name
        self.window.labels.itemWidget(item).setText(name)

    def __clearLayout(_, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def __generate_matrix(self, rewamp=False):
        label_count = len(self.labels)
        matrix = np.array([
            [0] * label_count
        ] * label_count)

        i = 0
        for row in range(label_count):
            for col in range(row):
                matrix[row, col] = i
                i = (i + 1) % 4

        if rewamp:
            self.matrix = matrix
        else:
            for row in range(min(len(self.matrix), label_count)):
                for col in range(min(len(row), label_count)):
                    self.matrix[row, col] = matrix[row, col]

    def __update_matrix(self):
        label_count = len(self.labels)
        self.__clearLayout(self.window.matrix)
        self.window.matrix.cellRect(label_count, label_count)
        self.window.matrix.setAlignment(Qt.AlignVCenter)

        self.__compute_image()

        for col in range(label_count):
            label = QLabel(self.labels[col])
            label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
            self.window.matrix.addWidget(label, 0, col + 1)

        for row in range(label_count):
            label = QLabel(self.labels[row])
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.window.matrix.addWidget(label, row + 1, 0)

            for col in range(row):
                self.window.matrix.addWidget(
                    self.__generate_matrix_button(self.matrix[row, col], row, col), row + 1, col + 1)

            for col in range(row, label_count):
                self.window.matrix.addWidget(self.__generate_matrix_button(
                    self.matrix[row, col], row, col, disabled=True), row + 1, col + 1)

    def __generate_matrix_button(self, kind, row, col, disabled=False):
        button = QPushButton()
        button.setIcon(self.kinds[kind])
        button.setDisabled(disabled)
        button.clicked.connect(lambda: self.set_marker_event(row, col))
        return button

    def __load_ui(self, ui_file_name, title):
        loader = QUiLoader()
        ui_file = QFile(ui_file_name)

        if not ui_file.open(QFile.ReadOnly):
            raise Exception(
                f"Cannot open {ui_file_name}: {ui_file.errorString()}")

        self.window = loader.load(ui_file)
        self.window.setWindowTitle(title)
        ui_file.close()

        self.window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    AppView = App(os.path.join(app_root, 'lib', 'ui', 'main.ui'),
                  'Triangle Adjacency Matrix')
    sys.exit(app.exec_())
