import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                             QVBoxLayout)

SWITCH_RATIO = 15

VERTICAL = [False for _i in range(500)]
HORIZONTAL = [True for _i in range(500)]


class Switch:
    def __init__(self, x, y, active=False, widget=None, array=None, id=0):
        self.x = x
        self.y = y
        self.object = QGraphicsRectItem(0, 0, SWITCH_RATIO, SWITCH_RATIO, self.trigger)
        self.active = active
        if active:
            self.object.setBrush(QBrush(Qt.cyan))
        else:
            self.object.setBrush(QBrush(Qt.darkCyan))
        self.object.setPos(x, y)
        self.widget = widget
        self.array = array
        self.id = id

    def draw(self, scene):
        scene.addItem(self.object)

    def trigger(self):
        self.active = not self.active
        self.array[self.id] = self.active
        self.widget.draw_graphics()


class SwitchGroup:
    def __init__(self, widget=None, array=None):
        self.objects = []
        self.widget = widget
        self.array = array

    def add(self, x, y, state):
        self.objects.append(Switch(x, y, active=state, widget=self.widget, id=len(self.objects), array=self.array))

    def extrapolate_from(self, x1, y1, x2, y2):
        state_list = self.array
        for i in range(((x2-x1) // SWITCH_RATIO//2)+1):
            for j in range(((y2 - y1) // SWITCH_RATIO//2)+1):
                self.add(x1+i*SWITCH_RATIO*2, y1+j*SWITCH_RATIO*2, state_list[max([i, j])])

    def draw(self, scene):
        for item in self.objects:
            item.draw(scene)


class QGraphicsRectItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, w, h, pressAction=None):
        super(QGraphicsRectItem, self).__init__(x, y, w, h)
        self.pressAction = pressAction

    def mousePressEvent(self, event):
        QtWidgets.QGraphicsRectItem.mousePressEvent(self, event)
        self.pressAction.__call__()


class QWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    def resizeEvent(self, event):
        QtWidgets.QWidget.resizeEvent(self, event)
        self.draw_graphics()

    def draw_graphics(self):
        self.scene.clear()
        width = self.view.size().width()
        height = self.view.size().height()
        self.scene.setBackgroundBrush(Qt.GlobalColor.white)
        rect = QGraphicsRectItem(0, 0, SWITCH_RATIO, SWITCH_RATIO, p)
        rect.setBrush(QBrush(Qt.lightGray))
        self.scene.addLine(SWITCH_RATIO, SWITCH_RATIO, width-5, SWITCH_RATIO)
        self.scene.addLine(SWITCH_RATIO, SWITCH_RATIO, SWITCH_RATIO, height-5)
        self.scene.addItem(rect)

        a = SwitchGroup(widget=self, array=VERTICAL)
        b = SwitchGroup(widget=self, array=HORIZONTAL)
        a.extrapolate_from(0, SWITCH_RATIO * 2, 0, 2000)
        b.extrapolate_from(SWITCH_RATIO*2, 0, 2000, 0)

        a.draw(self.scene)
        b.draw(self.scene)


def p():
    print("aboba")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    window.resize(500, 500)
    window.setMinimumSize(QtCore.QSize(500, 500))
    # window.setMaximumSize(QtCore.QSize(500, 500))

    frame = QtWidgets.QFrame(window)
    frame.setGeometry(QtCore.QRect(5, 440, 491, 50))
    frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
    frame.setFrameShadow(QtWidgets.QFrame.Raised)

    color_button = QtWidgets.QPushButton(frame)
    color_button.setText("Color palette...")
    mode_button = QtWidgets.QPushButton(frame)
    mode_button.setText("Mode")
    random_button = QtWidgets.QPushButton(frame)
    random_button.setText("Randomize!")
    label = QtWidgets.QLabel(frame)
    label.setText("Line-on probability:")
    doubleSpinBox = QtWidgets.QDoubleSpinBox(frame)
    doubleSpinBox.setMaximum(1.0)
    doubleSpinBox.setSingleStep(0.1)

    horizontal_layout = QtWidgets.QHBoxLayout(frame)
    horizontal_layout.addWidget(color_button)
    horizontal_layout.addWidget(mode_button)
    horizontal_layout.addWidget(random_button)
    horizontal_layout.addWidget(label)
    horizontal_layout.addWidget(doubleSpinBox)

    window.draw_graphics()

    verticalLayout = QVBoxLayout(window)
    verticalLayout.addWidget(window.view)
    verticalLayout.addWidget(frame)

    window.show()
    window.view.show()
    window.setWindowTitle("Hitomezashi Visualization Tool")
    app.exec()
