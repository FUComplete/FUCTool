# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(644, 590)
        MainWindow.setMinimumSize(QtCore.QSize(644, 590))
        MainWindow.setMaximumSize(QtCore.QSize(644, 590))
        MainWindow.setWindowTitle("FUComplete Tool")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 9, 645, 581))
        self.tabWidget.setObjectName("tabWidget")
        self.patch_tab = QtWidgets.QWidget()
        self.patch_tab.setObjectName("patch_tab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.patch_tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 641, 551))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.patcher_verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.patcher_verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.patcher_verticalLayout.setObjectName("patcher_verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setText("Select ISO file:")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.iso_path = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.iso_path.setEnabled(False)
        self.iso_path.setText("")
        self.iso_path.setObjectName("iso_path")
        self.horizontalLayout.addWidget(self.iso_path)
        self.iso_button = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.iso_button.setText("Select")
        self.iso_button.setObjectName("iso_button")
        self.horizontalLayout.addWidget(self.iso_button)
        self.patcher_verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox_2 = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.groupBox_2.setTitle("Options:")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.keep_databin = QtWidgets.QCheckBox(self.groupBox_2)
        self.keep_databin.setText("Extract patched DATA.BIN after patching (for modders).")
        self.keep_databin.setObjectName("keep_databin")
        self.verticalLayout_8.addWidget(self.keep_databin)
        self.psp_go_mem = QtWidgets.QCheckBox(self.groupBox_2)
        self.psp_go_mem.setText("PSP Go internal storage remapping (PSP Go only).")
        self.psp_go_mem.setObjectName("psp_go_mem")
        self.verticalLayout_8.addWidget(self.psp_go_mem)
        self.horizontalLayout_10.addLayout(self.verticalLayout_8)
        self.patcher_verticalLayout.addWidget(self.groupBox_2)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setText("Output:")
        self.label_4.setObjectName("label_4")
        self.patcher_verticalLayout.addWidget(self.label_4)
        self.patch_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.patch_button.setEnabled(False)
        self.patch_button.setText("Patch ISO")
        self.patch_button.setObjectName("patch_button")
        self.patcher_verticalLayout.addWidget(self.patch_button)
        self.tabWidget.addTab(self.patch_tab, "Patcher")
        self.config_tab = QtWidgets.QWidget()
        self.config_tab.setObjectName("config_tab")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.config_tab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 641, 551))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.config_verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.config_verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.config_verticalLayout.setObjectName("config_verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setText("Select CONFIG.BIN file:")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.config_bin_path = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.config_bin_path.setEnabled(False)
        self.config_bin_path.setText("")
        self.config_bin_path.setObjectName("config_bin_path")
        self.horizontalLayout_2.addWidget(self.config_bin_path)
        self.config_bin_button = QtWidgets.QToolButton(self.verticalLayoutWidget_2)
        self.config_bin_button.setText("Select")
        self.config_bin_button.setObjectName("config_bin_button")
        self.horizontalLayout_2.addWidget(self.config_bin_button)
        self.config_verticalLayout.addLayout(self.horizontalLayout_2)
        self.config_list = QtWidgets.QListWidget(self.verticalLayoutWidget_2)
        self.config_list.setEnabled(False)
        self.config_list.setFocusPolicy(QtCore.Qt.NoFocus)
        self.config_list.setStyleSheet("QListWidget::item { border-bottom: 1px solid lightgray; }")
        self.config_list.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.config_list.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.config_list.setObjectName("config_list")
        self.config_verticalLayout.addWidget(self.config_list)
        self.config_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.config_button.setEnabled(False)
        self.config_button.setText("Save")
        self.config_button.setObjectName("config_button")
        self.config_verticalLayout.addWidget(self.config_button)
        self.tabWidget.addTab(self.config_tab, "Configuration")
        self.replacer_tab = QtWidgets.QWidget()
        self.replacer_tab.setObjectName("replacer_tab")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.replacer_tab)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 641, 551))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_5.setText("Select folder:")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.replace_path = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.replace_path.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.replace_path.sizePolicy().hasHeightForWidth())
        self.replace_path.setSizePolicy(sizePolicy)
        self.replace_path.setText("")
        self.replace_path.setObjectName("replace_path")
        self.horizontalLayout_3.addWidget(self.replace_path)
        self.replace_folder_button = QtWidgets.QToolButton(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.replace_folder_button.sizePolicy().hasHeightForWidth())
        self.replace_folder_button.setSizePolicy(sizePolicy)
        self.replace_folder_button.setText("Select")
        self.replace_folder_button.setObjectName("replace_folder_button")
        self.horizontalLayout_3.addWidget(self.replace_folder_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.replace_status = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.replace_status.setText("")
        self.replace_status.setObjectName("replace_status")
        self.horizontalLayout_6.addWidget(self.replace_status)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.refresh_replace_button = QtWidgets.QToolButton(self.verticalLayoutWidget_3)
        self.refresh_replace_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_replace_button.sizePolicy().hasHeightForWidth())
        self.refresh_replace_button.setSizePolicy(sizePolicy)
        self.refresh_replace_button.setText("Rescan folder")
        self.refresh_replace_button.setObjectName("refresh_replace_button")
        self.horizontalLayout_6.addWidget(self.refresh_replace_button)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.replace_list = QtWidgets.QTableWidget(self.verticalLayoutWidget_3)
        self.replace_list.setEnabled(False)
        self.replace_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.replace_list.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.replace_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.replace_list.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.replace_list.setObjectName("replace_list")
        self.replace_list.setColumnCount(2)
        self.replace_list.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setText("id")
        self.replace_list.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("path")
        self.replace_list.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.replace_list)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.dump_databin_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.dump_databin_button.setText("Dump DATA.BIN")
        self.dump_databin_button.setObjectName("dump_databin_button")
        self.horizontalLayout_4.addWidget(self.dump_databin_button)
        self.nativepsp_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.nativepsp_button.setEnabled(False)
        self.nativepsp_button.setText("Generate NATIVEPSP folder")
        self.nativepsp_button.setObjectName("nativepsp_button")
        self.horizontalLayout_4.addWidget(self.nativepsp_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.tabWidget.addTab(self.replacer_tab, "File Replacer")
        self.quests_tab = QtWidgets.QWidget()
        self.quests_tab.setObjectName("quests_tab")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.quests_tab)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 641, 551))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_6.setText("Select save folder:")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.save_path = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.save_path.setEnabled(False)
        self.save_path.setText("")
        self.save_path.setObjectName("save_path")
        self.horizontalLayout_5.addWidget(self.save_path)
        self.save_folder_button = QtWidgets.QToolButton(self.verticalLayoutWidget_4)
        self.save_folder_button.setText("Select")
        self.save_folder_button.setObjectName("save_folder_button")
        self.horizontalLayout_5.addWidget(self.save_folder_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.folder_count = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.folder_count.setText("Decrypted quests in folder (0):")
        self.folder_count.setAlignment(QtCore.Qt.AlignCenter)
        self.folder_count.setObjectName("folder_count")
        self.horizontalLayout_8.addWidget(self.folder_count)
        self.quests_rescan = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quests_rescan.sizePolicy().hasHeightForWidth())
        self.quests_rescan.setSizePolicy(sizePolicy)
        self.quests_rescan.setText("Rescan folder")
        self.quests_rescan.setObjectName("quests_rescan")
        self.horizontalLayout_8.addWidget(self.quests_rescan)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.quests_folder_table = QtWidgets.QTableWidget(self.verticalLayoutWidget_4)
        self.quests_folder_table.setEnabled(True)
        self.quests_folder_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.quests_folder_table.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.quests_folder_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.quests_folder_table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.quests_folder_table.setObjectName("quests_folder_table")
        self.quests_folder_table.setColumnCount(2)
        self.quests_folder_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setText("qid")
        self.quests_folder_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Name")
        self.quests_folder_table.setHorizontalHeaderItem(1, item)
        self.verticalLayout_4.addWidget(self.quests_folder_table)
        self.horizontalLayout_7.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.quests_right = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.quests_right.setEnabled(False)
        self.quests_right.setText("--->")
        self.quests_right.setObjectName("quests_right")
        self.verticalLayout_3.addWidget(self.quests_right)
        self.quests_left = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.quests_left.setEnabled(False)
        self.quests_left.setText("<---")
        self.quests_left.setObjectName("quests_left")
        self.verticalLayout_3.addWidget(self.quests_left)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.save_count = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.save_count.setText("Quests in save (0/18):")
        self.save_count.setAlignment(QtCore.Qt.AlignCenter)
        self.save_count.setObjectName("save_count")
        self.horizontalLayout_9.addWidget(self.save_count)
        self.quests_remove = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.quests_remove.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quests_remove.sizePolicy().hasHeightForWidth())
        self.quests_remove.setSizePolicy(sizePolicy)
        self.quests_remove.setText("Remove")
        self.quests_remove.setObjectName("quests_remove")
        self.horizontalLayout_9.addWidget(self.quests_remove)
        self.verticalLayout_6.addLayout(self.horizontalLayout_9)
        self.quests_save_table = QtWidgets.QTableWidget(self.verticalLayoutWidget_4)
        self.quests_save_table.setEnabled(False)
        self.quests_save_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.quests_save_table.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.quests_save_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.quests_save_table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.quests_save_table.setRowCount(18)
        self.quests_save_table.setObjectName("quests_save_table")
        self.quests_save_table.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        item.setText("qid")
        self.quests_save_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Name")
        self.quests_save_table.setHorizontalHeaderItem(1, item)
        self.verticalLayout_6.addWidget(self.quests_save_table)
        self.horizontalLayout_7.addLayout(self.verticalLayout_6)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.quests_save_button = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.quests_save_button.setEnabled(False)
        self.quests_save_button.setText("Save ")
        self.quests_save_button.setObjectName("quests_save_button")
        self.verticalLayout_2.addWidget(self.quests_save_button)
        self.tabWidget.addTab(self.quests_tab, "Custom Quests")
        self.about_tab = QtWidgets.QWidget()
        self.about_tab.setObjectName("about_tab")
        self.verticalLayoutWidget_8 = QtWidgets.QWidget(self.about_tab)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(0, 0, 641, 541))
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_7.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.about_title = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.about_title.sizePolicy().hasHeightForWidth())
        self.about_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.about_title.setFont(font)
        self.about_title.setText("<html><head/><body><p>FUComplete Tool</p></body></html>")
        self.about_title.setTextFormat(QtCore.Qt.RichText)
        self.about_title.setAlignment(QtCore.Qt.AlignCenter)
        self.about_title.setObjectName("about_title")
        self.verticalLayout_7.addWidget(self.about_title)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setText("<html><head/><body><p align=\"center\"><a href=\"https://github.com/FUComplete/FUCTool/issues/new\"><span style=\" text-decoration: underline; color:#2980b9;\">Report issues</span></a> | <a href=\"https://github.com/FUComplete/FUCTool\"><span style=\" text-decoration: underline; color:#2980b9;\">Repository</span></a><br/></p><p>Tool to install and manage various settings and options of the <a href=\"https://github.com/FUComplete\"><span style=\" text-decoration: underline; color:#2980b9;\">FUComplete</span></a> patch.</p><p><br/></p></body></html>")
        self.label_8.setOpenExternalLinks(True)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_7.addWidget(self.label_8)
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.groupBox.setFont(font)
        self.groupBox.setTitle("Libraries/tools used:")
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setText("<html>\n"
"<head />\n"
"<body>\n"
"<ul>\n"
"<li><a href=\"https://gitlab.com/svanheulen/mhff\" style=\"text-decoration: underline; color:#2980b9;\">mhff</a></li>\n"
"<li>mhef (<a href=\"https://gitlab.com/svanheulen/mhef\" style=\"text-decoration: underline; color:#2980b9;\">original</a>, <a href=\"https://github.com/IncognitoMan/mhef\" style=\"text-decoration: underline; color:#2980b9;\">fork</a>)</li>\n"
"<li><a href=\"https://github.com/jmacd/xdelta\" style=\"text-decoration: underline; color:#2980b9;\">xdelta3</a></li>\n"
"<li><a href=\"https://www.romhacking.net/utilities/891/\" style=\"text-decoration: underline; color:#2980b9;\">UMD-Replace</a></li>\n"
"<li><a href=\"https://github.com/BrianBTB/SED-PC\" style=\"text-decoration: underline; color:#2980b9;\">SED-PC</a></li>\n"
"<li><a href=\"https://github.com/scott-griffiths/bitstring\" style=\"text-decoration: underline; color:#2980b9;\">bitstring</a></li>\n"
"<li><a href=\"https://github.com/clalancette/pycdlib\" style=\"text-decoration: underline; color:#2980b9;\">pycdlib</a></li>\n"
"</ul>  \n"
"</body>\n"
"</html>")
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_7.setOpenExternalLinks(True)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_5.addWidget(self.label_7)
        self.verticalLayout_7.addWidget(self.groupBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem1)
        self.tabWidget.addTab(self.about_tab, "About")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass
import resources_rc
