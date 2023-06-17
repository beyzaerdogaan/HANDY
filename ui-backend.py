from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QComboBox
import subprocess
import sys


import res_rc
from database_config import fetch_dictionaries, connect_to_database, insert_dictionary, delete_first_row, \
    configuration

# Load the UI file created with Qt Designer
ui_file = "handy.ui"
Ui_MainWindow, _ = uic.loadUiType(ui_file)


class MyForm(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyForm, self).__init__()
        self.setupUi(self)

        # Connect the button click event to the handler
        self.btn_start.clicked.connect(self.btn_start_clicked)

        # Disable two elements in the QComboBox
        # self.cmbx_wolf_right.model().item(2).setEnabled(False)
        cmbxs = []
        cmbxs.append(self.cmbx_wolf_right)
        cmbxs.append(self.cmbx_metal_right)
        cmbxs.append(self.cmbx_gun_finger_right)
        cmbxs.append(self.cmbx_scissors_right)
        cmbxs.append(self.cmbx_scout_right)
        cmbxs.append(self.cmbx_thumbs_up_right)
        cmbxs.append(self.cmbx_wolf_left)
        cmbxs.append(self.cmbx_gun_finger_left)
        cmbxs.append(self.cmbx_scissors_left)
        cmbxs.append(self.cmbx_scout_left)
        cmbxs.append(self.cmbx_thumbs_up_left)
        cmbxs.append(self.cmbx_pointing_left)
        self.config_cmbx(cmbxs)

        # Connect a signal to handle the selection change
        for cmbx in cmbxs:
            cmbx.currentIndexChanged.connect(lambda index, cmbxs=cmbxs: self.handle_selection_change(index, cmbxs))
        # self.cmbx_wolf_right.currentIndexChanged.connect(self.handle_selection_change)

    def btn_start_clicked(self):
        # Run the second file using subprocess
        subprocess.Popen([sys.executable, 'C:/Users/byzrd/PycharmProjects/handy-ui/handy-ui/handy.py'])

    def handle_selection_change(self, index, cmbxs):
        sender = self.sender()  # Get the sender of the signal
        print(cmbxs)

        if isinstance(sender, QComboBox):
            selected_item = sender.currentText()
            print(f"{sender.objectName()} - Selected index: {index}")
            print(f"{sender.objectName()} - Selected item: {selected_item}")

            connection = connect_to_database("handy_schema")
            functions_dict = fetch_dictionaries(connection)

            move = sender.objectName().replace("cmbx_", "")
            move_and_hand = move.rsplit("_", 1)
            movement = move_and_hand[1] + "_" + move_and_hand[0]

            action = ""
            for k, v in functions_dict.items():
                if v == movement:
                    action = k

            if selected_item == "":
                functions_dict[action] = selected_item
                for cmbx in cmbxs:
                    cmbx.model().item(cmbx.findText(action)).setEnabled(True)
                    cmbx.update()
            else:
                functions_dict[selected_item] = movement
                for cmbx in cmbxs:
                    if cmbx.objectName() != sender.objectName():
                        cmbx.model().item(cmbx.findText(action)).setEnabled(True)
                        cmbx.model().item(cmbx.findText(selected_item)).setEnabled(False)
                        cmbx.update()
                    sender.update()

            delete_first_row(connection)
            insert_dictionary(connection, functions_dict)

    def config_cmbx(self, cmbxs):
        connection = connect_to_database("handy_schema")
        functions_dict = fetch_dictionaries(connection)
        for k, v in functions_dict.items():
            if v == "right_wolf":
                self.cmbx_wolf_right.setCurrentIndex(self.cmbx_wolf_right.findText(k))
            elif v == "right_metal":
                self.cmbx_metal_right.setCurrentIndex(self.cmbx_metal_right.findText(k))
            elif v == "right_gun_finger":
                self.cmbx_gun_finger_right.setCurrentIndex(self.cmbx_gun_finger_right.findText(k))
            elif v == "right_scissors":
                self.cmbx_scissors_right.setCurrentIndex(self.cmbx_scissors_right.findText(k))
            elif v == "right_scout":
                self.cmbx_scout_right.setCurrentIndex(self.cmbx_scout_right.findText(k))
            elif v == "right_thumbs_up":
                self.cmbx_thumbs_up_right.setCurrentIndex(self.cmbx_thumbs_up_right.findText(k))
            elif v == "left_wolf":
                self.cmbx_wolf_left.setCurrentIndex(self.cmbx_wolf_left.findText(k))
            elif v == "left_gun_finger":
                self.cmbx_gun_finger_left.setCurrentIndex(self.cmbx_gun_finger_left.findText(k))
            elif v == "left_scissors":
                self.cmbx_scissors_left.setCurrentIndex(self.cmbx_scissors_left.findText(k))
            elif v == "left_scout":
                self.cmbx_scout_left.setCurrentIndex(self.cmbx_scout_left.findText(k))
            elif v == "left_thumbs_up":
                self.cmbx_thumbs_up_left.setCurrentIndex(self.cmbx_thumbs_up_left.findText(k))
            elif v == "left_pointing":
                self.cmbx_pointing_left.setCurrentIndex(self.cmbx_pointing_left.findText(k))

            functions = [ k for (k,v) in functions_dict.items() if functions_dict.get(k) != ""]
            for i in functions:
                for cmbx in cmbxs:
                    cmbx.model().item(cmbx.findText(i)).setEnabled(False)
            for cmbx in cmbxs:
                cmbx.model().item(cmbx.currentIndex()).setEnabled(True)


if __name__ == '__main__':
    configuration()
    app = QtWidgets.QApplication([])
    form = MyForm()
    form.show()
    app.exec()
    sys.exit(app.exec_())
