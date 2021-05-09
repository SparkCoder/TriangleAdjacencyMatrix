from PySide2.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide2.QtCore import Qt as Qt

from .editableLabel import EditableLabel


class LabelListItem(QWidget):
    def __init__(self, name, parent=None):
        super(LabelListItem, self).__init__(parent)

        self.item = None
        self.change_callback = None
        self.delete_callback = None

        self.label = EditableLabel(name)
        self.label.on_change_callback = self.__change_event

        self.button = QPushButton("DELETE")
        self.button.clicked.connect(self.__delete_event)

        self.row = QHBoxLayout(self)
        self.row.addWidget(self.label, 1)
        self.row.addWidget(self.button, 1)
        self.row.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.row)

    def __change_event(self, name):
        if self.change_callback is not None and self.item is not None:
            self.change_callback(self.item, name)

    def __delete_event(self):
        if self.delete_callback is not None and self.item is not None:
            self.delete_callback(self.item)

    def setText(self, name):
        self.label.setText(name)
