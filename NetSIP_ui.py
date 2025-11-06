import PyQt6.QtCore as QtCore
import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtGui as QtGui

try:
    from . import tab1_modifier
except:
    import tab1_modifier

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NetSIP")

        # Create layout for the tabs
        self.tab_layout = QtWidgets.QVBoxLayout()
        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_layout.addWidget(self.tab_widget)        

        # Get the widget for tab1
        tab1 = tab1_modifier.tab1_modifier(self)
        self.tab_widget.addTab(tab1, "SIP Modifier")      

        # Add the widget as the central widget
        self.setCentralWidget(self.tab_widget)


        # set the default window size
        self.resize(1080, 720)
        # Add an icon for the program
        try:
            self.setWindowIcon(QtGui.QIcon("images/netspi.png"))
        except:
            pass
        
        # Show the UI window
        self.show()


    def clicked(self, checked):
        pass

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def contextMenuEvent(self, e):
        context = QtWidgets.QMenu(self)
        context.exec(e.globalPos())


class Color(QtWidgets.QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(color))
        self.setPalette(palette)
        

if(__name__ == "__main__"):
    app = QtWidgets.QApplication([])
    app.setStyle("Fusion")

    window = MainWindow()

    app.exec()

def launch():
    app = QtWidgets.QApplication([])
    app.setStyle("Fusion")

    window = MainWindow()

    app.exec()
