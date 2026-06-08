__author__ = 'Janko Slavic'

import sys

from PyQt6 import QtWidgets
from PyQt6 import QtGui

import time


class MainWindow(QtWidgets.QMainWindow):
    """ Inherited main window
    """

    def __init__(self):
        """ Constructor of the MainWindow object
        """
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle('Main window')
        self.setGeometry(0, 0, 1600, 1400)
        #self.showMaximized()
        self.init_status_bar()
        self.init_central_widget()
        self.init_actions()
        self.init_menus()
#        self.phase = 0
        # we will need this for the animation

    def init_status_bar(self):
        """ Function to create Status Bar
        """
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.showMessage('Ready', 4000)
        self.setStatusBar(self.status_bar)

    def init_central_widget(self):
        """ Content of the central window
        """
        #first we create the central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        #then we make a vertical layout and assign it to central_widget
        v_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(v_layout)

        #now we add a text input field and a widget for buttons into v_layout
        self.function_text = QtWidgets.QTextEdit()
        self.buttons_widget = QtWidgets.QWidget()
        v_layout.addWidget(self.function_text)
        v_layout.addWidget(self.buttons_widget)

        #we will place the buttons in a horizontal layout
        h_layout = QtWidgets.QHBoxLayout()
        self.buttons_widget.setLayout(h_layout)

        #we define the input field
        self.function_text.setFontPointSize(20)
        self.function_text.setText('np.sin')
        self.function_text.setMaximumHeight(50)

        #we define two buttons
        self.submit_btn = QtWidgets.QPushButton('Show')
        self.submit_btn.pressed.connect(self.refresh_figure)
        self.animate_btn = QtWidgets.QPushButton('Animate')
        self.animate_btn.pressed.connect(self.animate_figure)
        self.animate_btn.setCheckable(True)

        #we now add both buttons to the horizontal layout
        h_layout.addStretch() # adjusts so there is free space on the left
        h_layout.addWidget(self.submit_btn)
        h_layout.addWidget(self.animate_btn)
        h_layout.addStretch() # for free space on the right
        #self.get_figure()

        #v_layout.addWidget(self.canvas)
        #v_layout.addWidget(self.canvas_toolbar)



    def init_menus(self):
        """ Set up the menus
        """
        self.file_menu = self.menuBar().addMenu('&File')
        self.help_menu = self.menuBar().addMenu('&Help')

        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.reset_action)
        self.help_menu.addAction(self.help_action)

    def file_show_help(self):
        #for debugging use this
        # QtGui.QMessageBox.about(self,
        QtWidgets.QMessageBox.about(self,
                                'Display of a pop-up window with text.',
                                'Python and Qt :)\nEnter a numpy function')

    def clear_input(self):
        self.function_text.setText('')

    def reset_input(self):
        self.function_text.setText('np.sin')

    def init_actions(self):
        """ Set up the actions for the menus
        """
        self.new_file_action = QtGui.QAction('&New',
                                             self, shortcut=QtGui.QKeySequence.StandardKey.New,
                                             statusTip="New display",
                                             triggered=self.clear_input)
        self.reset_action = QtGui.QAction('&Reset',
                                          self,
                                          statusTip="Reset",
                                          triggered=self.reset_input)
        self.help_action = QtGui.QAction(  # QtGui.QIcon('new.png') # this is how we could include an icon
                                           '&Help',
                                           self,
                                           triggered=self.file_show_help)

    def get_figure(self):
        pass

    def animate_figure(self):
        pass

    def refresh_figure(self):
        #instead of displaying a figure, here we demonstrate the use of a selection dialog
        function_list = ['sin', 'cos', 'tan', 'exp']
        text, ok = QtWidgets.QInputDialog.getItem(self, 'Selection dialog example', 'Select:', function_list)
        self.function_text.setText('np.' + text)

    def show_progress(self):
        """ Show progress

        """
        while self.progress_bar.value() < 100:
            self.progress_bar.setValue(self.progress_bar.value() + 2)
            time.sleep(.05)
        self.status_label.setText('Ready')

    def mouseDoubleClickEvent(self, event):
        """ We override the inherited event in the QtGui.QMainWindow object
            (double-click e.g. on the progress bar)
        """
        self.close()

if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        app.exec()
        sys.exit(0)
    except SystemExit:
        print('Closing window.')
    except:
        print(sys.exc_info())
