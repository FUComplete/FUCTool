#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import shutil
import sys
from datetime import datetime
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


class ConfigWidget(QtWidgets.QWidget):
    def __init__(self, desc, options, parent=None):
        super(ConfigWidget, self).__init__(parent)
        self.options = options

        label = QtWidgets.QLabel(desc)
        label.setOpenExternalLinks(True)
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
        outfolder = Path(self.filepath).parent.joinpath("data_root")

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


class ISOHashThread(QtCore.QThread):
    endSignal = QtCore.pyqtSignal(str)

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def run(self):
        iso_hash = utils.get_iso_hash(self.filepath)
        self.endSignal.emit(iso_hash)


class CopyISOThread(QtCore.QThread):
    endSignal = QtCore.pyqtSignal(str)

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def run(self):
        utils.create_temp_folder()
        tmp_iso = Path(utils.temp_folder, self.filepath.name)
        shutil.copy2(self.filepath, tmp_iso)

        self.endSignal.emit(str(tmp_iso))


class ExtractDATABINThread(QtCore.QThread):
    endSignal = QtCore.pyqtSignal(str)

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def run(self):
        utils.create_temp_folder()
        data_bin_path = utils.extract_data_bin(self.filepath)
        self.endSignal.emit(data_bin_path)


class DecryptDATABINThread(QtCore.QThread):
    endSignal = QtCore.pyqtSignal(str)

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def run(self):
        utils.create_temp_folder()
        data_dec_path = Path(utils.temp_folder, "DATA.BIN.DEC")
        utils.decrypt_data_bin(self.filepath, data_dec_path)

        self.endSignal.emit(str(data_dec_path))


class DecryptSaveThread(QtCore.QThread):
    endSignal = QtCore.pyqtSignal(bytes)

    def __init__(self, filepath, save_region):
        super().__init__()
        self.filepath = filepath
        self.save_region = save_region

    def run(self):
        dec = utils.decrypt_save(self.filepath, self.save_region)
        self.endSignal.emit(dec)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(f"FUComplete Tool [{utils.VERSION}]")

        self.iso_hash_thread = None
        self.copy_iso_thread = None
        self.extract_databin_thread = None
        self.decrypt_databin_thread = None
        self.dump_thread = None
        self.decrypt_save_thread = None

        self.process1 = None  # UMD-Replace.exe
        self.process2 = None  # xdelta3.exe
        self.process3 = None  # SED-PC.exe

        self.iso_hash = None
        self.current_iso_path = None

        self.folder_quests = []
        self.save_quests = []

        self.save = None
        self.save_key = None
        self.save_region = None

        self.config = utils.config

        # Cleanup
        if utils.temp_folder.exists():
            shutil.rmtree(utils.temp_folder)

        logTextBox = QTextEditLogger(self)
        logTextBox.setFormatter(logging.Formatter('%(levelname)s | %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().setLevel(logging.INFO)
        self.patcher_verticalLayout.insertWidget(3, logTextBox.widget)

        # Patcher tab
        self.psp_go_mem.clicked.connect(self.psp_go_check)

        self.patch_button.clicked.connect(self.patch_iso)
        self.iso_button.clicked.connect(self.select_iso)

        # Config Tab
        self.config_options = []
        for itm in self.config["CONFIG.BIN"]:
            item = QtWidgets.QListWidgetItem(self.config_list)
            item_widget = ConfigWidget(itm["description"], itm["options"])
            item.setSizeHint(item_widget.sizeHint())
            self.config_list.addItem(item)
            self.config_list.setItemWidget(item, item_widget)
            self.config_options.append(item_widget)

        self.config_list.verticalScrollBar().setSingleStep(10)

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
        self.quests_save_button.clicked.connect(self.encrypt_and_save)

        # About tab
        self.about_title.setText(f"FUComplete Tool {utils.VERSION}")

    def generic_dialog(self, text, title="Info", mode=0):
        if mode == 0:
            QtWidgets.QMessageBox.information(self, title, text)
        if mode == 1:
            QtWidgets.QMessageBox.critical(self, title, text)

    def log_stderr(self, data):
        stderr = bytes(data).decode("utf8")
        logging.error(stderr)

    def process1_stderr(self):
        data = self.process1.readAllStandardError()
        self.log_stderr(data)

    def process2_stderr(self):
        data = self.process2.readAllStandardError()
        self.log_stderr(data)

    def process3_stderr(self):
        data = self.process3.readAllStandardError()
        self.log_stderr(data)

    def psp_go_check(self):
        if self.psp_go_mem.isChecked():
            result = QtWidgets.QMessageBox.question(self, 'PSP Go internal storage remapping',
                                                    "This is ONLY needed if you're installing the game on a PSP Go's internal storage.\n\nDO NOT enable if you're installing the game to a memory stick or a different model PSP/Vita.\n\nAre you sure you want to enable this?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.No)

            if result == QtWidgets.QMessageBox.No:
                self.psp_go_mem.setChecked(False)

    def select_iso(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                            "Select MHFU ISO file", "", "ISO Files (*.iso)",
                                                            options=options)
        if fileName:
            self.iso_path.setText(fileName)
            logging.info("Checking ISO...")

            self.iso_hash_thread = ISOHashThread(fileName)
            self.iso_hash_thread.start()

            self.iso_hash_thread.endSignal.connect(self.iso_hash_finished)

    def iso_hash_finished(self, iso_hash):
        self.iso_hash = iso_hash
        self.iso_hash_thread.exit()

        if self.iso_hash in [utils.UMD_MD5HASH, utils.PSN_MD5HASH]:
            logging.info("Valid ISO file.")
            self.patch_button.setEnabled(True)
        else:
            logging.error(f"Invalid ISO, your dump should match one of the following md5 hashes:")
            logging.error(f"UMD: {utils.UMD_MD5HASH}")
            logging.error(f"PSN: {utils.PSN_MD5HASH}")

    def patch_compat(self, iso_path):
        exe_path = Path(utils.bin_path, "xdelta3.exe")
        patch_path = Path(utils.current_path, "res", "patches", "compat.xdelta")
        utils.create_temp_folder()
        niso_path = Path(utils.temp_folder, iso_path.stem + "_compat.iso")
        self.current_iso_path = niso_path

        logging.info("UMD ISO found, applying compat patch...")
        self.process2 = QtCore.QProcess()
        self.process2.readyReadStandardError.connect(self.process2_stderr)
        self.process2.finished.connect(self.patch_compat_finished)
        self.process2.start(str(exe_path), ["-d", "-s", str(iso_path), str(patch_path), str(niso_path)])

    def patch_compat_finished(self):
        logging.info("Compat patching done.")
        self.process2 = None

        self.extract_databin()

    def copy_iso(self, iso_path):
        logging.info("Copying ISO...")
        self.copy_iso_thread = CopyISOThread(iso_path)
        self.copy_iso_thread.start()

        self.copy_iso_thread.endSignal.connect(self.copy_iso_finished)

    def copy_iso_finished(self, tmp_iso):
        self.copy_iso_thread.exit()

        self.current_iso_path = tmp_iso
        self.extract_databin()

    def extract_databin(self):
        logging.info("Extracting DATA.BIN...")
        self.extract_databin_thread = ExtractDATABINThread(self.current_iso_path)
        self.extract_databin_thread.start()

        self.extract_databin_thread.endSignal.connect(self.extract_databin_finished)

    def extract_databin_finished(self, databin_path):
        self.extract_databin_thread.exit()
        self.decrypt_databin(databin_path)

    def decrypt_databin(self, databin_path):
        logging.info("Decrypting DATA.BIN (this may take a few minutes)...")
        self.decrypt_databin_thread = DecryptDATABINThread(databin_path)
        self.decrypt_databin_thread.start()

        self.decrypt_databin_thread.endSignal.connect(self.decrypt_databin_finished)

    def decrypt_databin_finished(self):
        self.decrypt_databin_thread.exit()

        old_data_path = Path(utils.temp_folder, "DATA.BIN")
        os.remove(old_data_path)

        self.replace_databin()

    def replace_databin(self):
        exe_path = Path(utils.bin_path, "UMD-replace.exe")
        databin_path = Path(utils.temp_folder, "DATA.BIN.DEC")

        logging.info("Replacing DATA.BIN...")
        self.process1 = QtCore.QProcess()
        self.process1.readyReadStandardError.connect(self.process1_stderr)
        self.process1.finished.connect(self.replace_databin_finished)
        self.process1.start(str(exe_path), [str(self.current_iso_path), "/PSP_GAME/USRDIR/DATA.BIN", str(databin_path)])

    def replace_databin_finished(self):
        self.process1 = None

        old_data_path = Path(utils.temp_folder, "DATA.BIN.DEC")
        if self.keep_databin.isChecked():
            ndatabin = Path(self.iso_path.text()).parent.joinpath("DATA.BIN")
            shutil.move(old_data_path, ndatabin)
            logging.info(f"DATA.BIN moved to: {ndatabin}")
        else:
            os.remove(old_data_path)

        self.patch_fuc()

    def patch_fuc(self):
        exe_path = Path(utils.bin_path, "xdelta3.exe")
        patch_path = Path(utils.current_path, "res", "patches", "FUC.xdelta")
        iso_path = Path(self.iso_path.text())
        niso_path = Path(iso_path.parent, iso_path.stem + "_FUC.iso")

        logging.info("Patching ISO...")
        self.process2 = QtCore.QProcess()
        self.process2.readyReadStandardError.connect(self.process2_stderr)
        self.process2.finished.connect(self.patch_fuc_finished)
        self.process2.start(str(exe_path), ["-d", "-s", str(self.current_iso_path), str(patch_path), str(niso_path)])

    def patch_fuc_finished(self):
        self.process2 = None

        iso_path = Path(self.iso_path.text())

        if self.psp_go_mem.isChecked():
            self.patch_psp_go(iso_path)
        else:
            self.cleanup()

    def patch_psp_go(self, iso_path):
        exe_path = Path(utils.bin_path, "xdelta3.exe")
        patch_path = Path(utils.current_path, "res", "patches", "EF0.xdelta")
        utils.create_temp_folder()
        niso_path = Path(utils.temp_folder, iso_path.stem + "_ef0.iso")
        self.current_iso_path = niso_path

        logging.info("Applying PSP Go internal storage patch...")
        self.process2 = QtCore.QProcess()
        self.process2.readyReadStandardError.connect(self.process2_stderr)
        self.process2.finished.connect(self.patch_psp_go_finished)
        self.process2.start(str(exe_path), ["-d", "-s", str(iso_path), str(patch_path), str(niso_path)])

    def patch_psp_go_finished(self):
        logging.info("PSP Go internal storage patching done.")
        self.process2 = None

        self.cleanup()

    def cleanup(self):
        iso_path = Path(self.iso_path.text())
        niso_path = Path(iso_path.parent, iso_path.stem + "_FUC.iso")

        if utils.temp_folder.exists():
            shutil.rmtree(utils.temp_folder)

        logging.info("Checking patched ISO...")
        self.iso_hash_thread = ISOHashThread(niso_path)
        self.iso_hash_thread.start()

        self.iso_hash_thread.endSignal.connect(self.iso_hash_finished2)

    def iso_hash_finished2(self, iso_hash):
        self.iso_hash = iso_hash
        self.iso_hash_thread.exit()

        if self.iso_hash in self.config["iso_checksum"]:
            iso_path = Path(self.iso_path.text())
            niso_path = Path(iso_path.parent, iso_path.stem + "_FUC.iso")
            logging.info(f"Patching done, patched ISO is located at: {niso_path}")
        else:
            logging.error(f"Patched ISO doesn't match the checksum, try again.")

        self.patch_button.setEnabled(True)
        self.iso_button.setEnabled(True)
        self.keep_databin.setEnabled(True)
        self.psp_go_mem.setEnabled(True)
        self.patch_button.setText("Patch ISO")

    def patch_iso(self):
        self.patch_button.setEnabled(False)
        self.iso_button.setEnabled(False)
        self.keep_databin.setEnabled(False)
        self.psp_go_mem.setEnabled(False)
        self.patch_button.setText("Patching...")

        iso_path = Path(self.iso_path.text())

        if self.iso_hash == utils.UMD_MD5HASH:
            self.patch_compat(iso_path)
        else:
            self.copy_iso(iso_path)

    def select_config_bin(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select CONFIG.BIN file", "",
                                                            "CONFIG.BIN (CONFIG.BIN)", options=options)
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
            self.generic_dialog("ERROR: No files found in folder.", mode=1, title="Error")
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
        inpath = Path(self.replace_path.text())
        outpath = Path(inpath).parent.absolute().joinpath('NATIVEPSP')
        utils.generate_filebin(inpath, outpath)

        self.generic_dialog(f"NATIVEPSP folder successfully generated at: {outpath}")

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

            self.dump_thread.endSignal.connect(self.dump_finished)
            self.dump_thread.statusSignal.connect(self.dump_status)

    def dump_status(self, code):
        if code == -1:
            self.dump_databin_button.setText("Dump DATA.BIN")
            self.dump_databin_button.setEnabled(True)
            self.generic_dialog(f"DATA.BIN is not decrypted.", mode=1, title="Error")
            self.dump_thread.exit()
        if code == 1:
            self.dump_databin_button.setText("Renaming...")

    def dump_finished(self, filepath):
        self.dump_databin_button.setEnabled(True)
        self.dump_databin_button.setText("Dump DATA.BIN")

        self.generic_dialog(f"DATA.BIN dumped to {filepath}")
        self.dump_thread.exit()

    def scan_quests_folder(self):
        self.quests_save_table.clearSelection()
        self.folder_quests = utils.get_quests_in_folder()
        qsize = len(self.folder_quests)

        self.quests_folder_table.setRowCount(qsize)
        self.folder_count.setText(f"Decrypted quests in folder ({qsize}):")

        for i, q in enumerate(self.folder_quests):
            qid = QtWidgets.QTableWidgetItem(q["qid"])
            name = QtWidgets.QTableWidgetItem(q["name"])
            self.quests_folder_table.setItem(i, 0, qid)
            self.quests_folder_table.setItem(i, 1, name)

    def scan_quests_save(self):
        self.quests_save_table.clearContents()
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

            self.read_save(savepath)

            self.quests_right.setEnabled(True)
            self.quests_left.setEnabled(True)
            self.quests_remove.setEnabled(True)
            self.quests_save_table.setEnabled(True)
            self.quests_save_button.setEnabled(True)

    def read_save(self, path):
        if "ULES01213" in path.parent.name:
            self.save_key = "FU.bin"
            self.save_region = 1
        if "ULUS10391" in path.parent.name:
            self.save_key = "FU.bin"
            self.save_region = 2
        if "ULJM05500" in path.parent.name:
            self.save_key = "P2G.bin"
            self.save_region = 3

        param = Path(path.parent, "PARAM.SFO")
        if (self.save_key is None) or (not path.exists()) or (not param.exists()):
            self.generic_dialog("Select the PSP save folder with the MHP2NDG.BIN and PARAM.SFO files.",
                                mode=1, title="Error")
            return

        self.save_folder_button.setEnabled(False)
        self.save_folder_button.setText("Decrypting...")
        self.decrypt_save_thread = DecryptSaveThread(path, self.save_region)
        self.decrypt_save_thread.start()

        self.decrypt_save_thread.endSignal.connect(self.decrypt_save_finished)

    def decrypt_save_finished(self, dec):
        self.save = bytearray(dec)
        self.save_quests = utils.get_quests_in_save(dec)
        self.scan_quests_save()

        self.save_folder_button.setEnabled(True)
        self.save_folder_button.setText("Select")

    def copy_to_save(self):
        selection = self.quests_folder_table.selectionModel().selectedRows()

        if len(self.save_quests) + len(selection) > 18:
            self.generic_dialog("Not enough slots to add selected quests to save.", mode=1, title="Error")
        else:
            for s in selection:
                qfile = self.folder_quests[s.row()]
                self.save_quests.append(qfile)

            self.quests_folder_table.clearSelection()
            self.scan_quests_save()

    def copy_from_save(self):
        selection = self.quests_save_table.selectionModel().selectedRows()

        for s in selection:
            qfile = self.save_quests[s.row()]
            self.folder_quests.append(qfile)

            fname = "m" + qfile["qid"] + ".mib.dec"
            qfolder = Path(utils.current_path, "quests")
            fpath = Path(qfolder, fname)

            if not qfolder.exists():
                os.makedirs(qfolder)

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

    def encrypt_and_save(self):
        self.quests_save_button.setText("Encrypting...")
        self.quests_save_button.setEnabled(False)

        empty = 18 - len(self.save_quests)
        empty_quests = [{"bytes": bytearray(), "qid": "", "name": ""} for _ in range(empty)]

        nquests = self.save_quests + empty_quests
        nsave = utils.add_quests_to_save(self.save, nquests)
        nsave = utils.encrypt_save(nsave, self.save_region)

        utils.create_temp_folder()
        og_save = Path(self.save_path.text(), "MHP2NDG.BIN")
        tmp_save = Path(utils.temp_folder, "MHP2NDG.BIN.TEMP")
        backup_save = Path(og_save.parent, "MHP2NDG.BIN.BAK")

        param_in = Path(og_save.parent, "PARAM.SFO")

        with open(tmp_save, "wb") as f:
            f.write(nsave)

        shutil.copy2(og_save, backup_save)

        keypath = Path(utils.resources_path, "keys", self.save_key)
        exe_path = Path(utils.bin_path, "SED-PC.exe")

        self.process3 = QtCore.QProcess()
        self.process3.readyReadStandardError.connect(self.process3_stderr)
        self.process3.finished.connect(self.encrypt_finished)
        self.process3.start(str(exe_path), ["-e", str(tmp_save), str(param_in), str(og_save), str(keypath)])

    def encrypt_finished(self):
        self.process3 = None

        tmp_save = Path(utils.temp_folder, "MHP2NDG.BIN.TEMP")
        os.remove(tmp_save)

        self.generic_dialog(f"Save changed succesfully.")
        self.quests_save_button.setText("Save")
        self.quests_save_button.setEnabled(True)

#
# def exception_hook(exc_type, exc_value, exc_traceback):
#     logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
#     sys.exit()
#
#
# def set_up_logger():
#     date_time_obj = datetime.now()
#     timestamp_str = date_time_obj.strftime("%d-%b-%Y_%H_%M_%S")
#     filename = '{}.log'.format(timestamp_str)
#     logging.basicConfig(filename=filename)
#     sys.excepthook = exception_hook


if __name__ == "__main__":
    # set_up_logger()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.setStyle("Fusion")
    window.show()
    app.exec_()
