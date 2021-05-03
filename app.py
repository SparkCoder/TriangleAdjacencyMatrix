from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QObject

import sys
import os

import res_rc

# Globals
app_root = os.path.dirname(os.path.realpath(__file__))


class App(QObject):

    def __init__(self, ui_file_name, title, parent=None):
        super(App, self).__init__(parent)

        loader = QUiLoader()
        ui_file = QFile(ui_file_name)

        if not ui_file.open(QFile.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)

        self.window = loader.load(ui_file)
        self.window.setWindowTitle(title)
        ui_file.close()

        self.window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    App = App(os.path.join(app_root, 'main.ui'), 'Triangle Adjacency Matrix')
    sys.exit(app.exec_())
