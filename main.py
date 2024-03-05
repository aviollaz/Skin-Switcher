import sys
import os
import shutil
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QInputDialog, QDialog, QLabel, QLineEdit
from shutil import copytree, move
import keyboard
import pyautogui
from functools import partial

username = os.getlogin()

class DirectoryDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Select osu! Directory')
        self.osu_path = f'C:\\Users\\{username}\\AppData\\Local\\osu!'
        self.initUI()
        

    def initUI(self):
        layout = QVBoxLayout()

        instruction_label =  QLabel('you probably don\'t have to change this unless you didn\'t install osu! in the default location')
        layout.addWidget(instruction_label)

        # Create a QLineEdit widget for the default path
        self.path_line_edit = QLineEdit(self.osu_path)
        layout.addWidget(self.path_line_edit)

        # Create a QPushButton widget for browsing the directory
        browse_button = QPushButton('Browse')
        browse_button.clicked.connect(self.browse_directory)
        layout.addWidget(browse_button)

        self.setLayout(layout)

    def browse_directory(self):
        # Open a file dialog for the user to select a directory
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory', self.osu_path)
        if directory:
            self.path_line_edit.setText(directory)
            self.osu_path = directory




class SkinSwitcher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.last_id = -1
        self.current_skin_id = -1
        self.multi_skin_path = ""
        self.skin_id_of_keybind = {}

    def initUI(self):
        self.setWindowTitle('Skin Switcher')
        self.setGeometry(100, 100, 430, 500)  # Set window size
        self.setStyleSheet("background-color: #FFCCFF;")  # Set background color to white

        layout = QVBoxLayout()

        # Button to choose directory
        self.choose_dir_button = QPushButton('Choose osu! directory')
        self.choose_dir_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.choose_dir_button)

        # skin lot #1
        self.add_skin_5 = QPushButton('slot 1')
        self.add_skin_5.clicked.connect(partial(self.add_skin, 5))
        self.add_skin_5.setFixedSize(50,50)
        layout.addWidget(self.add_skin_5)

        # skin lot #2
        self.add_skin_6 = QPushButton('slot 2')
        self.add_skin_6.clicked.connect(partial(self.add_skin, 6))
        self.add_skin_6.setFixedSize(50,50)
        layout.addWidget(self.add_skin_6)

        # reset button
        self.reset_button = QPushButton("reset skins")
        self.reset_button.clicked.connect(self.reset_ss)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)


    def choose_directory(self):
        dialog = DirectoryDialog(self)
        dialog.exec()
        directory = dialog.osu_path
        self.multi_skin_path = f'{directory}/Skins/skinSwitcher'

    def add_skin(self, slot):
        # create multi_skin folder if it does not exist
        if not os.path.exists(self.multi_skin_path):
            os.makedirs(self.multi_skin_path)

        # copy all of the skin files into multi_skin
        original_skin_directory = QFileDialog.getExistingDirectory(self, 'Select skin folder')

        self.copy_skin_files(original_skin_directory, slot)

    

    def detect_input(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            if keyboard.is_pressed('ctrl') and event.name in ['5', '6', '7', '8', '9', '0']:
                self.switch_skin(event.name)
                pyautogui.keyDown('ctrl')
                pyautogui.keyDown('shift')
                pyautogui.keyDown('alt')
                pyautogui.keyDown('s')

                # Release all keys
                pyautogui.keyUp('s')
                pyautogui.keyUp('alt')
                pyautogui.keyUp('shift')
                pyautogui.keyUp('ctrl')
                print(f'pressed ctrl+{event.name}, switching skin')


    def switch_skin(self, new_skin_id):
        self.current_skin_id = self.fetch_current_skin()

        # Return current skin files into its folder
        files = os.listdir(self.multi_skin_path)

        for file in files:
            if not file.startswith("skin_"):
                source_path = os.path.join(self.multi_skin_path, file)
                destination_path = os.path.join(f'{self.multi_skin_path}/skin_{self.current_skin_id}', file)
                move(source_path, destination_path)
        
        # Move the new skin files into the multi skin folder
        new_files = os.listdir(f'{self.multi_skin_path}/skin_{new_skin_id}')
        
        for file in new_files:
            source_path = os.path.join(f'{self.multi_skin_path}/skin_{new_skin_id}', file)
            destination_path = self.multi_skin_path
            move(source_path, destination_path)

        with open("info.txt", "w") as file:
            file.write(f"current_skin={new_skin_id}")
            file.close()


    def copy_skin_files(self, directory, slot):
        source_path = directory
        destination_path = f'{self.multi_skin_path}/skin_{slot}' 

        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)

        # used copytree() instead of copyfile() because the latter breaks when copying directories
        copytree(source_path, destination_path)


    def fetch_current_skin(self):
        if os.path.exists("info.txt"):
            with open("info.txt", "r") as file:
                try:
                    self.current_skin_id = int(file.readline().split("=")[1])
                except:
                    print("invalid skin id")
        else:
            with open("info.txt", "w") as file:
                file.write('current_skin=-1')
        return self.current_skin_id
    
    def reset_ss(self):
        shutil.rmtree(self.multi_skin_path)

        with open("info.txt", "w") as file:
            file.write("current_skin=-1")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    skin_switcher_app = SkinSwitcher()
    skin_switcher_app.show()
    keyboard.hook(skin_switcher_app.detect_input)
    sys.exit(app.exec())
    