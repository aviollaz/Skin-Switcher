import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from shutil import copyfile

with open("info.txt", "r") as file:
    line = file.readline()
    last_id = int(line.split("=")[1])

current_skin = -1
osu_path = ""
multiSkin_path = ""

class SkinSwitcher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Skin Switcher')
        self.setGeometry(100, 100, 400, 400)  # Set window size
        self.setStyleSheet("background-color: #FFCCFF;")  # Set background color to white

        layout = QVBoxLayout()

        # Button to choose directory
        self.choose_dir_button = QPushButton('Choose osu! directory')
        self.choose_dir_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.choose_dir_button)

        # Button to add skin
        self.add_skin_button = QPushButton('Add a skin')
        self.add_skin_button.clicked.connect(self.add_skin)
        layout.addWidget(self.add_skin_button)

        self.setLayout(layout)

    def choose_directory(self):
        global multiSkin_path
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if directory:
            print(f'Selected directory: {directory}')
            multiSkin_path = f'{directory}/Skins/skinSwitcher'
    
    def add_skin(self):
        global last_id

        # create multiSkin folder if it does not exist
        if not os.path.exists(multiSkin_path):
            os.makedirs(multiSkin_path)
        
        # fetch last skin id and update it
        skin_id = last_id + 1
        with open("info.txt", "w") as file:
            file.write(f'last_id={skin_id}')

        # create specific skin folder inside multiSkin
        new_skin_path = f'{multiSkin_path}/skin_{skin_id}'
        os.makedirs(new_skin_path)
        
        directory = QFileDialog.getExistingDirectory(self, 'Select skin folder')
        for file in os.listdir(directory):
            source_path = f'{directory}/{file}'
            destination_path = os.path.join(new_skin_path, f'{file}#{skin_id}')
            copyfile(source_path, destination_path)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    skin_switcher_app = SkinSwitcher()
    skin_switcher_app.show()
    sys.exit(app.exec())