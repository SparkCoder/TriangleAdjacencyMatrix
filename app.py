from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton
from PySide2.QtCore import QFile, QObject
from PySide2.QtGui import QIcon

import numpy as np

import sys
import os

# import resources
import lib.ui.res_rc

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
        self.__generate_matrix()

        self.__load_ui(ui_file_name, title)

        # Events
         

        self.__update_matrix()

    def __clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def __generate_matrix(self):
        label_count = len(self.labels)
        self.matrix = np.array([
            [0] * label_count
        ] * label_count)

        i = 0
        for row in range(label_count):
            for col in range(row + 1):
                self.matrix[row, col] = i
                i = (i + 1) % 4

    def __update_matrix(self):
        label_count = len(self.labels)
        self.__clearLayout(self.window.matrix)
        self.window.matrix.cellRect(label_count, label_count)

        for row in range(label_count):
            for col in range(row + 1):
                self.window.matrix.addWidget(
                    self.__generate_matrix_button(self.matrix[row, col]), row, col)
            for col in range(row + 1, label_count):
                self.window.matrix.addWidget(self.__generate_matrix_button(
                    self.matrix[row, col], disabled=True), row, col)

    def __generate_matrix_button(self, kind, disabled=False):
        button = QPushButton()
        button.setIcon(self.kinds[kind])
        button.setDisabled(disabled)
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
