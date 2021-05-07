from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QListWidgetItem
from PySide2.QtCore import QFile, QObject
from PySide2.QtCore import Qt as Qt
from PySide2.QtGui import QIcon

import numpy as np

import sys
import os

# import resources
from lib.ui import res_rc

# Globals
app_root = os.path.dirname(os.path.realpath(__file__))


class LabelListItem(QWidget):
    def __init__(self, name, parent=None):
        super(LabelListItem, self).__init__(parent)

        self.label = QLabel(name)
        self.button = QPushButton("DELETE")

        self.row = QHBoxLayout(self)

        self.row.addWidget(self.label)
        self.row.addWidget(self.button)

        self.row.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.row)


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

        self.__update_matrix()

        self.window.labels.clear()
        for label in self.labels:
            self.__add_label(label, list_update=False)

        # Events
        self.window.addLabelBtn.clicked.connect(self.add_label_event)

    def add_label_event(self):
        self.__add_label('item ' + str(len(self.labels) + 1))
        self.__generate_matrix()
        self.__update_matrix()

    def __add_label(self, label, list_update=True):
        if list_update:
            self.labels.append(label)
        row = LabelListItem(label)
        item = QListWidgetItem(self.window.labels)
        self.window.labels.addItem(item)
        self.window.labels.setItemWidget(item, row)

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
        self.window.matrix.setAlignment(Qt.AlignVCenter)

        for col in range(label_count):
            label = QLabel(self.labels[col])
            label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
            self.window.matrix.addWidget(label, 0, col + 1)

        for row in range(label_count):
            label = QLabel(self.labels[row])
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.window.matrix.addWidget(label, row + 1, 0)

            for col in range(row + 1):
                self.window.matrix.addWidget(
                    self.__generate_matrix_button(self.matrix[row, col]), row + 1, col + 1)

            for col in range(row + 1, label_count):
                self.window.matrix.addWidget(self.__generate_matrix_button(
                    self.matrix[row, col], disabled=True), row + 1, col + 1)

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
