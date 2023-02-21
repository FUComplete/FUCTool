#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import shutil
import sys
from pathlib import Path

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import utils
from qt_ui import Ui_MainWindow


class QTextEditLogger(logging.Handler, QtCore.QObject):
    appendPlainText = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.appendPlainText.connect(self.widget.appendPlainText)

    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText.emit(msg)


class OptionalWidget(QtWidgets.QWidget):
    def __init__(self, label, filename, parent=None):
        super(OptionalWidget, self).__init__(parent)
        self.filename = filename

        label = QtWidgets.QLabel(label)
        self.checkbox = QtWidgets.QCheckBox()

        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # self.checkbox.setSizePolicy(sizePolicy)
        label.setWordWrap(True)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.checkbox)

        self.mouseReleaseEvent = lambda _: self.checkbox.click()
        self.setLayout(layout)


class ConfigWidget(QtWidgets.QWidget):
    def __init__(self, desc, options, parent=None):
        super(ConfigWidget, self).__init__(parent)
        self.options = options

        label = QtWidgets.QLabel(desc)
        self.combobox = QtWidgets.QComboBox()

        for op in self.options["values"]:
            self.combobox.addItem(op["label"])

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.combobox.setSizePolicy(sizePolicy)
        label.setWordWrap(True)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.combobox)

        self.setLayout(layout)


class DumpDataBINThread(QtCore.QThread):
    endSignal = QtCore.pyqtSignal(str)
    statusSignal = QtCore.pyqtSignal(int)

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def run(self):
        # bin_dec = Path(self.filepath).stem + ".BIN.DEC"
        # utils.decrypt_data_bin(self.filepath, bin_dec)
        # self.statusSignal.emit(1)

        outfolder = Path(self.filepath).parent.joinpath("DATA.BIN_dump")

        # Check if folder exists already, can cause issues later
        if outfolder.exists():
            shutil.rmtree(outfolder)

        os.makedirs(outfolder, exist_ok=True)

        try:
            utils.dump_data_bin(self.filepath, outfolder)
            self.statusSignal.emit(1)
        except (MemoryError, OverflowError):
            self.statusSignal.emit(-1)
            return

        utils.rename_dump_files(outfolder)
        self.endSignal.emit(str(outfolder.absolute()))


class QuestsReadThread(QtCore.QThread):
    endSignal = QtCore.pyqtSignal(str)

    def __init__(self, folderpath):
        super().__init__()
        self.folderpath = folderpath



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.dump_thread = None

        self.process1 = None  # UMD-Replace.exe
        self.process2 = None  # xdelta3.exe
        self.process3 = None  # psp-save.exe

        self.folder_quests = []
        self.save_quests = []

        self.save = None
        self.save_key = None
        # self.decpath = None

        config = utils.config

        # Cleanup
        if utils.temp_folder.exists():
            shutil.rmtree(utils.temp_folder)

        # Patcher Tab
        logTextBox = QTextEditLogger(self)
        logTextBox.setFormatter(logging.Formatter('%(levelname)s | %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().setLevel(logging.INFO)
        self.patcher_verticalLayout.insertWidget(4, logTextBox.widget)

        self.optional_patches = []
        for itm in config["optional"]:
            item = QtWidgets.QListWidgetItem(self.optional_list)
            item_widget = OptionalWidget(itm["label"], itm["file"])
            item.setSizeHint(item_widget.sizeHint())
            self.optional_list.addItem(item)
            self.optional_list.setItemWidget(item, item_widget)
            self.optional_patches.append(item_widget)

        self.patch_button.clicked.connect(self.patch_iso)
        self.iso_button.clicked.connect(self.select_iso)

        # Config Tab
        self.config_options = []
        for itm in config["config.bin"]:
            item = QtWidgets.QListWidgetItem(self.config_list)
            item_widget = ConfigWidget(itm["description"], itm["options"])
            item.setSizeHint(item_widget.sizeHint())
            self.config_list.addItem(item)
            self.config_list.setItemWidget(item, item_widget)
            self.config_options.append(item_widget)

        self.config_button.clicked.connect(self.save_config)
        self.config_bin_button.clicked.connect(self.select_config_bin)

        # Replacer Tab
        header = self.replace_list.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.replace_folder_button.clicked.connect(self.select_replace_folder)
        self.refresh_replace_button.clicked.connect(self.refresh_list_clicked)
        self.nativepsp_button.clicked.connect(self.generate_nativepsp_folder)
        self.dump_databin_button.clicked.connect(self.dump_databin)

        # Quests Tab
        self.quests_folder_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.quests_folder_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.quests_save_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.quests_save_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.scan_quests_folder()

        self.save_folder_button.clicked.connect(self.select_save_folder)
        self.quests_rescan.clicked.connect(self.scan_quests_folder)
        self.quests_right.clicked.connect(self.copy_to_save)
        self.quests_left.clicked.connect(self.copy_from_save)
        self.quests_remove.clicked.connect(self.remove_from_save)

    def generic_dialog(self, text, title="Info", mode=0):
        if mode == 0:
            QtWidgets.QMessageBox.information(self, title, text)
        if mode == 1:
            QtWidgets.QMessageBox.critical(self, title, text)

    def select_iso(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select MHFU ISO file", "", "ISO Files (*.iso)",
                                                            options=options)
        if fileName:
            self.iso_path.setText(fileName)
            self.optional_list.setEnabled(True)
            self.patch_button.setEnabled(True)

    def patch_iso(self):
        print(self.iso_path.text())

        for itm in self.optional_patches:
            print(itm.filename, itm.checkbox.isChecked())

        # patcher.LOGGER = logging.getLogger()
        # patcher.replace_data_bin("", "")

    def select_config_bin(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select config.bin file", "",
                                                            "config.bin (config.bin)", options=options)
        if fileName:
            for i, conf in enumerate(utils.read_configs(fileName)):
                self.config_options[i].combobox.setCurrentIndex(conf)

            self.config_bin_path.setText(fileName)
            self.config_list.setEnabled(True)
            self.config_button.setEnabled(True)

    def save_config(self):
        cpath = self.config_bin_path.text()
        config_bin = utils.read_file_bytes(cpath)

        for itm in self.config_options:
            offset = itm.options["offset"]
            data = itm.options["values"][itm.combobox.currentIndex()]["data"]
            config_bin = utils.write_config(config_bin, offset, data)

        utils.write_file_bytes(cpath, config_bin)
        self.generic_dialog("Configuration saved successfully.")

    def refresh_replace_list(self, folderName):
        files = utils.read_replace_folder(folderName)

        if not files:
            self.generic_dialog("ERROR: No data folder found.", mode=1, title="Error")
            return

        lenght = len(files)
        self.replace_list.setRowCount(lenght)
        self.replace_status.setText(f"{lenght} file(s) found.")

        for i, f in enumerate(files):
            idx = QtWidgets.QTableWidgetItem(f["id"])
            path = QtWidgets.QTableWidgetItem(f["path"])
            self.replace_list.setItem(i, 0, idx)
            self.replace_list.setItem(i, 1, path)

        self.replace_list.resizeRowsToContents()

    def refresh_list_clicked(self):
        path = self.replace_path.text()
        self.refresh_replace_list(path)

    def select_replace_folder(self):
        options = QtWidgets.QFileDialog.Options(QtWidgets.QFileDialog.ShowDirsOnly)
        folderName = QtWidgets.QFileDialog.getExistingDirectory(self, "Select mods folder", options=options)
        if folderName:
            self.refresh_replace_list(folderName)

            self.replace_path.setText(folderName)
            self.replace_list.setEnabled(True)
            self.refresh_replace_button.setEnabled(True)
            self.nativepsp_button.setEnabled(True)

    def generate_nativepsp_folder(self):
        inpath = self.replace_path.text()
        outpath = Path(inpath).parent.absolute().joinpath('nativePSP')
        utils.generate_filebin(inpath, outpath)

        self.generic_dialog(f"nativePSP folder successfully generated at: {outpath}")

    def dump_databin(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select DATA.BIN file", "",
                                                            "DATA.BIN (DATA.BIN DATA.BIN.DEC)",
                                                            options=options)
        if fileName:
            self.dump_databin_button.setEnabled(False)
            self.dump_databin_button.setText("Dumping...")

            self.dump_thread = DumpDataBINThread(fileName)
            self.dump_thread.start()

            self.dump_thread.endSignal.connect(self.dump_end)
            self.dump_thread.statusSignal.connect(self.dump_status)

    def dump_status(self, code):
        if code == -1:
            self.dump_databin_button.setText("Dump DATA.BIN")
            self.dump_databin_button.setEnabled(True)
            self.generic_dialog(f"DATA.BIN is not decrypted.", mode=1, title="Error")
            self.dump_thread.exit()
        if code == 1:
            self.dump_databin_button.setText("Renaming...")

    def dump_end(self, filepath):
        self.dump_databin_button.setEnabled(True)
        self.dump_databin_button.setText("Dump DATA.BIN")

        self.generic_dialog(f"DATA.BIN dumped to {filepath}")
        self.dump_thread.exit()

    def scan_quests_folder(self):
        self.quests_save_table.clearSelection()
        self.folder_quests = utils.get_quests_in_folder()
        qsize = len(self.folder_quests)

        self.quests_folder_table.setRowCount(qsize)
        self.folder_count.setText(f"Quests in folder ({qsize}):")

        for i, q in enumerate(self.folder_quests):
            qid = QtWidgets.QTableWidgetItem(q["qid"])
            name = QtWidgets.QTableWidgetItem(q["name"])
            self.quests_folder_table.setItem(i, 0, qid)
            self.quests_folder_table.setItem(i, 1, name)

    def scan_quests_save(self):
        qsize = len(self.save_quests)
        self.save_count.setText(f"Quests in save ({qsize}/18):")

        for i, q in enumerate(self.save_quests):
            qid = QtWidgets.QTableWidgetItem(q["qid"])
            name = QtWidgets.QTableWidgetItem(q["name"])
            self.quests_save_table.setItem(i, 0, qid)
            self.quests_save_table.setItem(i, 1, name)

    def select_save_folder(self):
        options = QtWidgets.QFileDialog.Options(QtWidgets.QFileDialog.ShowDirsOnly)
        folderName = QtWidgets.QFileDialog.getExistingDirectory(self, "Select PSP save folder", options=options)
        if folderName:
            savepath = Path(folderName).joinpath("MHP2NDG.BIN")
            self.save_path.setText(folderName)

            # TODO: move to QuestsReadThread
            self.read_save(savepath)

            self.quests_right.setEnabled(True)
            self.quests_left.setEnabled(True)
            self.quests_remove.setEnabled(True)
            self.quests_save_table.setEnabled(True)
            self.quests_save_button.setEnabled(True)

    def read_save(self, path):
        mode = None
        if "ULES01213" in path.parent.name:
            self.save_key = "FU.bin"
            mode = 1
        if "ULUS10391" in path.parent.name:
            self.save_key = "FU.bin"
            mode = 2
        if "ULJM05500" in path.parent.name:
            self.save_key = "P2G.bin"
            mode = 3

        param = Path(path.parent, "PARAM.SFO")
        if (self.save_key is None) or (not path.exists()) or (not param.exists()):
            self.generic_dialog("Select the PSP save folder with the MHP2NDG.BIN and PARAM.SFO files.",
                                mode=1, title="Error")
            return

        shutil.copy2(path, Path(path.parent, path.stem + ".BIN.BAK"))  # Backup save just in case

        dec = utils.decrypt_save(path, mode)
        self.save = dec
        self.save_quests = utils.get_quests_in_save(dec)
        self.scan_quests_save()

    # def decrypt_finished(self):
    #     self.process3 = None
    #
    #     self.save_folder_button.setText("Select")
    #     self.save = utils.read_file_bytes(self.decpath)
    #
    #     self.quests_right.setEnabled(True)
    #     self.quests_left.setEnabled(True)
    #     self.quests_save_table.setEnabled(True)

    def copy_to_save(self):
        selection = self.quests_folder_table.selectionModel().selectedRows()

        # TODO: Check if it's an arena quest and not add it (and show a dialog)
        if len(self.save_quests)+len(selection) > 18:
            self.generic_dialog("Not enough slots to add selected quests to save.", mode=1, title="Error")
        else:
            for s in selection:
                # TODO: encrypt when writting save
                # enc = utils.encrypt_quest(qfile)

                qfile = self.folder_quests[s.row()]
                self.save_quests.append(qfile)

            self.quests_folder_table.clearSelection()
            self.scan_quests_save()

    def copy_from_save(self):
        selection = self.quests_save_table.selectionModel().selectedRows()

        for s in selection:
            qfile = self.save_quests[s.row()]
            self.folder_quests.append(qfile)

            fname = "m"+qfile["qid"]+".mib.dec"
            fpath = Path(utils.current_path, "quests", fname)

            if fpath.exists():
                dlg = QtWidgets.QMessageBox()
                dlg.setWindowTitle("Question")
                dlg.setText(f"{fname} already exists, overwrite?")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Question)
                dlg.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

                if dlg.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                    with open(fpath, "wb") as f:
                        f.write(qfile["bytes"])
            else:
                with open(fpath, "wb") as f:
                    f.write(qfile["bytes"])

        self.scan_quests_folder()

    def remove_from_save(self):
        selection = self.quests_save_table.selectionModel().selectedRows()

        removed = []
        for s in selection:
            removed.append(s.row())

        nlist = []
        for i in range(len(self.save_quests)):
            if i not in removed:
                nlist.append(self.save_quests[i])

        self.save_quests = nlist
        self.quests_save_table.clearContents()
        self.scan_quests_save()

    def write_save(self, path):
        # keypath = Path("res", self.save_key)
        # utils.create_temp_folder()
        # decpath = Path(utils.temp_folder, path.stem + ".BIN.DEC")
        # exe_path = Path(utils.current_path, "bin", "psp-save-w32.exe")

        self.save_folder_button.setText("Decrypting...")
        self.process3 = QtCore.QProcess()
        self.process3.finished.connect(self.decrypt_finished)
        self.process3.start(str(exe_path), ["-d", str(keypath), "5", str(path), str(decpath)])

    def encrypt_and_save(self):
        keypath = Path("res", self.save_key)
        exe_path = Path(utils.current_path, "bin", "psp-save-w32.exe")

        self.quests_save_button.setText("Encrypting...")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.setStyle("Fusion")
    window.show()
    app.exec_()
