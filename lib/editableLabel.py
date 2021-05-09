from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout


class EditableLabel(QWidget):
    def __init__(self, name, parent=None):
        super(EditableLabel, self).__init__(parent)

        self.on_change_callback = None

        self.label = QLabel(name)

        self.edit = QLineEdit()
        self.edit.setHidden(True)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

        self.__return_pressed = False

        # Events
        self.label.mousePressEvent = self.__edit_event
        self.edit.focusOutEvent = self.__edit_end_event
        self.edit.returnPressed.connect(self.__edit_end_event)

    def __edit_event(self, e):
        self.label.setHidden(True)
        self.edit.setHidden(False)
        self.edit.setText(self.label.text())
        self.edit.setFocus()

    def __edit_end_event(self, e=None):
        if e is None:
            self.__return_pressed = True
        elif self.__return_pressed:
            self.__return_pressed = False
            return
        self.label.setHidden(False)
        self.edit.setHidden(True)
        self.label.setText(self.edit.text())
        if self.on_change_callback is not None:
            self.on_change_callback(self.label.text())

    def setText(self, text):
        self.label.setText(text)
