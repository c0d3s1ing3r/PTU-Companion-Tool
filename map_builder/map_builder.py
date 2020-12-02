"""
Effectively an image placement drawer to facillitate map drawing
Because you want to be able to easily open and close these things, files are zipped together 
and saved using a custom extension
Assets stolen from DPP
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PIL import Image
import glob

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PokeD&D Map Editor'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initPillow()
        self.initUI()
        
    def initPillow(self):
        self.initTextures()
        self.initDestinations()

    def initTextures(self):
        textureFiles = []
        self.textures = {} # textures is a simple map of the filename to the image
        textureFiles = map(Image.open, glob.glob('./rsrc/textures/*.png'))
        for png in textureFiles: # this masks off the path and extension from the key
            self.textures[str.replace(str.replace(png.filename, './rsrc/textures\\', ''), '.png', '')] = png

    def initDestinations(self):
        destinationFiles = []
        self.destinations = {} # destinations is a simple map of the filename to the image
        destinationFiles = map(Image.open, glob.glob('./rsrc/destinations/*.png'))
        for png in destinationFiles:
            self.destinations[str.replace(str.replace(png.filename, './rsrc/destinations\\', ''), '.png', '')] = png

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('./rsrc/window_icon.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.addTools()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.show()
    
    def addTools(self):
        self.horizontalGroupBox = QGroupBox('Tools')
        layout = QGridLayout()

        self.textureCombo = QComboBox()
        self.textureCombo.addItem("Select a texture")
        self.textureCombo.addItems(list(self.textures))
        

        self.destinationCombo = QComboBox()
        self.destinationCombo.addItem("Select a destination")
        self.destinationCombo.addItems(list(self.destinations))

        layout.addWidget(QLabel('Set Texture:'),0,0)
        layout.addWidget(self.textureCombo,0,1)
        layout.addWidget(QLabel('Set Destination:'),1,0)
        layout.addWidget(self.destinationCombo,1,1)

        layout.addWidget(QPushButton('7'),2,0)
        layout.addWidget(QPushButton('8'),2,1)
        
        self.horizontalGroupBox.setLayout(layout)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())