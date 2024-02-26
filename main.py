import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QInputDialog
from shutil import copytree, move
import keyboard

last_id = -1
current_skin_id = -1
osu_path = ""
multi_skin_path = ""
skin_id_of_keybind = {}

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
        global multi_skin_path
        # create multi_skin folder if it does not exist
        if not os.path.exists(multi_skin_path):
            os.makedirs(multi_skin_path)
        
        # fetch last skin id and update it
        skin_id = self.update_last_id(multi_skin_path)

        # copy all of the skin files into multi_skin
        original_skin_directory = QFileDialog.getExistingDirectory(self, 'Select skin folder')

        self.copy_skin_files(original_skin_directory, skin_id)

        keybinds = ['ctrl+5', 'ctrl+6', 'ctrl+7', 'ctrl+8', 'ctrl+9', 'ctrl+0']
        keybind, ok = QInputDialog.getItem(self, 'choose keybind', 'select a keybind for this skin', keybinds, 0, True)
        if ok:
            self.handle_key_map(keybind, skin_id)
            
    
    # saves the skins id for that specific keybind
    def handle_key_map(self, keybind, skin_id):
        skin_id_of_keybind[keybind] = skin_id


    def detect_input(self, event):
        global current_skin_id
        if event.event_type == keyboard.KEY_DOWN:
            if keyboard.is_pressed('ctrl') and event.name in ['5', '6', '7', '8', '9', '0']:
                current_skin_id = self.switch_skin(current_skin_id, skin_id_of_keybind[f'ctrl+{event.name}'])
                print(f'pressed ctrl+{event.name}, switching skin')


    def switch_skin(self, current_skin_id, new_skin_id):
        global multi_skin_path
        # Return current skin files into its folder
        files = os.listdir(multi_skin_path)

        for file in files:
            if not file.startswith("skin_"):
                source_path = os.path.join(multi_skin_path, file)
                destination_path = os.path.join(f'{multi_skin_path}/skin_{current_skin_id}', file)
                move(source_path, destination_path)
        
        # Move the new skin files into the multi skin folder
        new_files = os.listdir(f'{multi_skin_path}/skin_{new_skin_id}')
        
        for file in new_files:
            source_path = os.path.join(f'{multi_skin_path}/skin_{new_skin_id}', file)
            destination_path = multi_skin_path
            move(source_path, destination_path)

        # Update the skin id     
        current_skin_id = new_skin_id
        return current_skin_id


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
    keyboard.hook(skin_switcher_app.detect_input)
    sys.exit(app.exec())
    