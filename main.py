import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from shutil import copytree
import keyboard

last_id = -1
current_skin = -1
osu_path = ""
multi_skin_path = ""

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
        global multi_skin_path
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if directory:
            print(f'Selected directory: {directory}')
            multi_skin_path = f'{directory}/Skins/skinSwitcher'
    

    def add_skin(self):
        # create multi_skin folder if it does not exist
        if not os.path.exists(multi_skin_path):
            os.makedirs(multi_skin_path)
        
        # fetch last skin id and update it
        skin_id = self.update_last_id(multi_skin_path)

        # copy all of the skin files into multi_skin
        original_skin_directory = QFileDialog.getExistingDirectory(self, 'Select skin folder')

        self.copy_skin_files(original_skin_directory, skin_id)

    
    def copy_skin_files(self, directory, skin_id):
        source_path = directory
        destination_path = f'{multi_skin_path}/skin_{skin_id}' 

        # used copytree() instead of copyfile() because the latter breaks when copying directories
        copytree(source_path, destination_path)


    def update_last_id(self, multi_skin_path):
        # List all directories in the specified path
        folders = [folder for folder in os.listdir(multi_skin_path) if os.path.isdir(os.path.join(multi_skin_path, folder))]

        # Extract numbers from folder names and find the highest one
        last_id = max((int(folder.split('_')[-1]) for folder in folders if folder.startswith('skin_')), default=-1) + 1

        return last_id

if __name__ == '__main__':
    app = QApplication(sys.argv)
    skin_switcher_app = SkinSwitcher()
    skin_switcher_app.show()
    sys.exit(app.exec())