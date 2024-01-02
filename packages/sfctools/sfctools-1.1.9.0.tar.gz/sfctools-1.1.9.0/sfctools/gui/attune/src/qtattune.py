from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QAbstractItemView, QListWidgetItem, QSplashScreen, QShortcut
from PyQt5.QtGui import QDesktopServices, QPixmap
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import QPalette, QColor, QFont

import traceback 


import difflib
import sys
import os
import yaml
import shutil
import time
import sympy
import re as regex
from re import sub
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from graphviz import Source
from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from sympy import simplify, init_printing, printing
import pandas as pd
import pyperclip
from collections import defaultdict
import subprocess

# sub-modules
from .pandasmodel import PandasModel
from .mamba_interpreter2 import convert_code
from .mainloop_editor import MainLoopEditor
from .output_display import OutputDisplay
from . import resources

from .draw_widget import MyDrawWidget, Box
from .agent_editor import CodeEditor
from .yaml_editor import SettingsEditor
from .theme_manager import ThemeManager

from . import resources
from .mamba_interpreter2 import convert_code
from .mainloop_editor import MainLoopEditor
from .output_display import OutputDisplay
# from .qt_material import apply_stylesheet


def camel(s):
  # ensures correct agent naming
  #s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  # s = sub(r"(_|-)+", " ", s).lower().replace(" ", "")
  if len(s) > 0:
    return ''.join([s[0].capitalize(), s[1:]])
  else:
    return s

def convert_bool(s):
            if s == "False":
                return False
            elif s == "True":
                return True

            return None


class SearchDialog(QtWidgets.QDialog):
    instance = None

    def __init__(self,parent=None):
        super(SearchDialog, self).__init__(parent)

        # print("init search dialog")
        self.__class__.instance = self

        path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(path,'search_dialog.ui'), self)

        self.pushButton.pressed.connect(self.start_search)
        # self.parent = parent

    def start_search(self):
        search_name = self.lineEdit.text()
        print("search for", search_name)

        # search agent

        for box in self.parent().drawcanvas.boxes:
            if box.name == search_name:

                self.parent().data_select_where(search_name)
                
                self.parent().drawcanvas.highlighted = box
                self.parent().update()
                break

    def CloseEvent(self, event):
        # print("close search dialg.")
        self.__class__.instance = None
        super().CloseEvent()


class MatrixViewer(QtWidgets.QDialog):
    instance = None

    def __init__(self,model,parent=None):
        super(MatrixViewer, self).__init__(parent)  # Call the inherited classes __init__ method

        self.__class__.instance = self

        path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(path,'matrix_viewer.ui'), self)

        self.set_model(model)
        # self.setStyleSheet(parent.theme_manager.get_stylesheet("main"))
        # self.setStyleSheet(parent.theme_manager.get_background_style())


    def set_model(self,model):
        print("SET MODEL", model)
        self.pandas_model = model
        self.tableView.setModel(model)

    def get_data(self):
        return self.pandas_model.get_rawdata()


class CashFlowViewer(QtWidgets.QDialog):
    instances = {}

    def closeEvent(self, event):
        del self.__class__.instances[self.name]
        event.accept() # let the window close

    def __init__(self,parent=None,name="Unknown"):

        self.name = name

        super(CashFlowViewer, self).__init__(parent)  # Call the inherited classes __init__ method
        path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(path,'income_viewer.ui'), self)
        self.setWindowTitle("Cash Flow Statement of %s" % name)

        self.__class__.instances[name] = self


    def set_model(self,model):
        print("SET MODEL", model)
        self.pandas_model = model
        self.tableView.setModel(model)

    def get_data(self):
        return self.pandas_model.get_rawdata()


class IncomeViewer(QtWidgets.QDialog):
    instances = {}

    def closeEvent(self, event):
        del self.__class__.instances[self.name]
        event.accept() # let the window close

    def __init__(self,parent=None,name="Unknown"):

        super(IncomeViewer, self).__init__(parent)  # Call the inherited classes __init__ method
        path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(path,'income_viewer.ui'), self)
        self.setWindowTitle("Income Sheet of %s" % name)

        self.name = name
        self.__class__.instances[name] = self

    def set_model(self,model):
        print("SET MODEL", model)
        self.pandas_model = model
        self.tableView.setModel(model)

    def get_data(self):
        return self.pandas_model.get_rawdata()



# Step 1: Create a worker
class StatusLED(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self,rb):
        super().__init__()
        self.rb = rb

        # self.rb = rb
        self.i = 0
        self.j = 0
        self.on = False
        # print("WORKER CREATED")

    def run(self):
        """Long-running task."""
        while(True):
            time.sleep(.1)

            if self.on:
                self.i += 1

                state = self.rb.isChecked()
                # self.rb.setChecked(not state)

                if self.i == 5:
                    self.i = 0
                    self.switch_state()
            else:
                pass
                # self.rb.setChecked(False)

            #print("state",self.i)

    def switch_state(self):
        self.on = not self.on
        # print("switch", self.on)

        #if not self.on:
        #    self.rb.setChecked(False)

class TransactionDesigner(QtWidgets.QMainWindow):
    def __init__(self):
        super(TransactionDesigner, self).__init__() # Call the inherited classes __init__ method
        print("load...")
        path = os.path.dirname(os.path.abspath(__file__))
        loadpath = os.path.join(path,"transaction_designer_mainwindow.ui")
        content = []
        success = False

        self.test_mode = False # used for testing

        # remove font-size to fix bug in qt designer
        with open(loadpath,"r") as file:
            for line in file.readlines():
                if "<pointsize>-1</pointsize>" not in line:
                    content.append(line)

            success = True

        if success:
            with open(loadpath,"w") as file:
                file.write("".join(content))



        # uic.loadUi('transaction_designer.ui', self) # Load the .ui file
        uic.loadUi(loadpath, self) # Load the .ui file
        print("done.")

        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint)
        # self.setFixedSize(self.size());
        self.flipped = False

        my_widget = MyDrawWidget(self.frame,self)
        # my_widget.move(-5,-55) #(80,160)

        # self.label_17.setVisible(False) # logo

        self.code_data = {}

        # logger for changes in transactions
        self.made_changes = False

        self.arrangeButton_7.pressed.connect(lambda: self.notify_tooltip(self.arrangeButton_7))
        self.arrangeButton_8.pressed.connect(lambda: self.notify_tooltip(self.arrangeButton_8))
        self.arrangeButton_9.pressed.connect(lambda: self.notify_tooltip(self.arrangeButton_9))
        self.arrangeButton_3.pressed.connect(lambda: self.notify_tooltip(self.arrangeButton_3))
        self.arrangeButton_4.pressed.connect(lambda: self.notify_tooltip(self.arrangeButton_4))
        self.arrangeButton_5.pressed.connect(lambda: self.notify_tooltip(self.arrangeButton_5))
        self.arrangeButton_6.pressed.connect(lambda: self.notify_tooltip(self.arrangeButton_6))
        # self.arrangeButton_2.pressed.connect(lambda: self.notify_tooltip(self.arrangeButton_2))



        self.actionGenerate_BalanceSheet_Matrix.triggered.connect(lambda: self.gen_balance_matrix(detailed=False))
        self.actionGenerate_Balance_Matrix_Detailed.triggered.connect(lambda: self.gen_balance_matrix(detailed=True))

        
        self.agent1Edit.textEdited.connect(self.change_alert)
        self.agent2Edit.textEdited.connect(self.change_alert)
        self.AssetListLeft.textChanged.connect(self.change_alert)
        self.LiabilityListLeft.textChanged.connect(self.change_alert)
        self.EquityListLeft.textChanged.connect(self.change_alert)
        self.AssetListRight.textChanged.connect(self.change_alert)
        self.LiabilityListRight.textChanged.connect(self.change_alert)
        self.EquityListRight.textChanged.connect(self.change_alert)
        self.editSubject.textEdited.connect(self.change_alert)
        self.editShortname.textEdited.connect(self.change_alert)
        self.editQuantity.textEdited.connect(self.change_alert)
        self.editDescription.textEdited.connect(self.change_alert)

        self.comboIncomeLeft.currentIndexChanged.connect(self.change_alert)
        self.comboCashLeft.currentIndexChanged.connect(self.change_alert)
        self.comboIncomeRight.currentIndexChanged.connect(self.change_alert)
        self.comboCashRight.currentIndexChanged.connect(self.change_alert)
        self.registerFlowBox.currentIndexChanged.connect(self.change_alert)
        self.registerFlowBox.currentIndexChanged.connect(lambda: print("REGISTER FLOW", self.registerFlowBox.currentText()))
        self.comboIncomeLeft.currentIndexChanged.connect(lambda: print("REGISTER FLOW", self.registerFlowBox.currentText()))

        self.editType.currentIndexChanged.connect(self.change_alert)
        self.comboUnidir.currentIndexChanged.connect(self.change_alert)

        self.editAddArgs.textEdited.connect(self.change_alert)
        self.editAddCode.textChanged.connect(self.change_alert)

        self.spinBoxFontSize.valueChanged.connect(lambda: self.drawcanvas.update())
        self.spinBoxFontSize_2.valueChanged.connect(lambda: self.drawcanvas.update())

        self.FilterlineEdit.textChanged.connect(self.update_table)

        self.checkBox.stateChanged.connect(lambda: self.drawcanvas.update())
        self.checkBox_2.stateChanged.connect(lambda: self.drawcanvas.update())
        self.checkBox_3.stateChanged.connect(lambda: self.drawcanvas.update())
        self.checkBox_4.stateChanged.connect(lambda: self.drawcanvas.update())
        self.checkBox_5.stateChanged.connect(lambda: self.drawcanvas.update())
        self.checkBox_6.stateChanged.connect(lambda: self.drawcanvas.update())
        self.checkBox_7.stateChanged.connect(lambda: self.drawcanvas.update())
        self.checkBox_8.stateChanged.connect(lambda: self.drawcanvas.update())
        self.checkBox_9.stateChanged.connect(lambda: self.drawcanvas.update())

        self.checkBox_raster.stateChanged.connect(lambda: self.drawcanvas.update_raster())

        # status LED
        self.thread = QThread()

        self.worker = StatusLED(self.radioButton)
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

        self.theme_manager = ThemeManager(self)
        self.setStyleSheet(self.theme_manager.get_stylesheet("main"))

        self.actionChristmas.triggered.connect(self.theme_manager.activate_christmas_mode)
        

        self.current_file = None

        # --
        self.drawcanvas = my_widget
        self.drawcanvas.mode = "drag"

        self.backup_str = ""
        # self.setMouseTracking(True)
        # self.nextButton.pressed.connect(self.goto_next)
        self.browseButton.triggered.connect(self.browse)
        # self.saveButton.triggered.connect(self.save)
        self.saveAsButton.triggered.connect(self.save_dlg)
        self.saveBuildButton.triggered.connect(self.save_and_build)
        # self.FlipHeightButton.pressed.connect(self.flip_height)
        self.actionFlip_View.triggered.connect(self.flip_height)
        self.actionRestore_Original_Size.triggered.connect(self.restore_original_size)

        self.actionShow_Output_Log.triggered.connect(self.show_output_display)

        # self.showgraphButton.triggered.connect(self.show_graph)
        self.genMatButton.triggered.connect(self.try_gen_matrix)
        # self.genCodeButton.triggered.connect(self.gen_code)
        # self.genTexButton.pressed.connect(self.gen_tex_description)
        self.genICSButton.triggered.connect(self.gen_tex_ics)

        self.graphshowincome.pressed.connect(self.gen_ics_single)
        self.genCFSButton.pressed.connect(self.gen_cashflow_single)

        self.editMainLoopButton.triggered.connect(self.edit_mainloop)

        self.buildProjectButton.triggered.connect(lambda: self.build_project(overwrite=True))
        self.runButton.triggered.connect(self.run_project)

        self.shortcut = QShortcut(QKeySequence("Ctrl+S"),self)
        self.shortcut.activated.connect(self.save_and_build)

        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"),self)
        self.shortcut_search.activated.connect(self.search_dlg)

        self.actionAbout.triggered.connect(lambda: self.notify("This sfctols-attune, developed at German Aerospace Center, Institute of Networked Energy Systems (DLR-VE).\nMIT license.\nThanks for using! Please report bugs to thomas.baldauf@dlr.de",title="About this software"))
        self.actionFlowMatrix_to_Excel_file.triggered.connect(lambda: self.gen_matrix(mode="excel"))

        self.actionSwitch_Dark_Bright_Mode.triggered.connect(self.switch_theme)

        self.transactionView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.transactionView.doubleClicked.connect(self.data_select)
        self.transactionView.setColumnWidth(0, 120)

        self.arrangeButton.pressed.connect(self.arrange_pretty)
        self.removeButton.pressed.connect(self.remove_item)

        self.bc1.pressed.connect(lambda: self.change_color(1))
        self.bc2.pressed.connect(lambda: self.change_color(2))
        self.bc3.pressed.connect(lambda: self.change_color(3))
        self.bc4.pressed.connect(lambda: self.change_color(4))
        self.bc5.pressed.connect(lambda: self.change_color(5))
        self.bc6.pressed.connect(lambda: self.change_color(6))
        self.bc7.pressed.connect(lambda: self.change_color(7))
        self.bc8.pressed.connect(lambda: self.change_color(8))

        self.btn_csave.pressed.connect(lambda: self.theme_manager.save_colors())
        self.btn_cload.pressed.connect(lambda: self.theme_manager.load_colors())
        self.btn_crestore.pressed.connect(lambda: self.theme_manager.restore())
        self.mainloop_str = ""
        self.settings_str = """
metainfo:
	author: your name here
	date: 2070
	info: example settings

hyperparams:
       - name: example
         value: 42.0
         description: an example parameter
"""
        self.editSettingsButton.triggered.connect(self.edit_settings)
        self.addButton.pressed.connect(self.add_new) # add an agent
        self.addButton2.pressed.connect(self.add_helper) # add a helper agent (no transactions)
        self.graphDeleteButton.pressed.connect(self.remove_helper)
        #self.saveButton.pressed.connect(self.save)
        # self.graphSelectButton.pressed.connect(self.change_graphmode_select)
        # self.graphDragButton.pressed.connect(self.change_graphmode_drag)
        self.graphEditButton.pressed.connect(self.edit_graph_agent)
        #for widget in [self.AssetListLeft, self.AssetListRight,
        #               self.LiabilityListLeft, self.LiabilityListRight,
        #               self.EquityListLeft, self.EquityListRight]:
        #    widget.textChanged.connect(self.update_data)
        self.actionSwap_Line_Interpolation.triggered.connect(self.drawcanvas.swap_interpol_style)
        self.actionExport_Graph_to_PDF.triggered.connect(self.drawcanvas.export_pdf)

        self.udpateButton.pressed.connect(self.update_data)

        self.filename = None    # current .yaml file
        self.entry_data = [] # store current entries
        self.selection_idx = None

        #self.matrixView = MatrixViewer(self)
        self.moveUpBtn.pressed.connect(self.move_up)
        self.moveDnBtn.pressed.connect(self.move_down)

        self.filterCombo.itemSelectionChanged.connect(lambda: self.drawcanvas.update())
        self.clearFilterButton.pressed.connect(self.clear_filter)

        # mainloop editor is always running to check for file changes
        self.mainloop_editor = MainLoopEditor(self,self.mainloop_str)
        self.mainloop_editor.show()
        self.mainloop_editor.hide()

        # settings editor is always running to check for file changes
        self.settings_editor = SettingsEditor(self, self.settings_str)
        self.settings_editor.show()
        self.settings_editor.hide()

        # theme manager setup
        # theme manager has 'dark' and 'bright' mode
        self.theme_manager.theme = "dark"
        self.switch_theme()
        self.theme_manager.restore()
        self.switch_theme()
        self.switch_theme()


    def search_dlg(self):
        """
        search for an agent
        """

        if SearchDialog.instance is None:
            new_dlg = SearchDialog(self)
            
        else:
            new_dlg = SearchDialog.instance

        new_dlg.show()
        # self.notify("Test Search", title="Search Agent")

    def change_color(self,which):
        color = QColorDialog.getColor()

        if color.isValid():
            print("CHANGE COLOR", which, color.name())

            btn_table = {
                1: self.bc1,
                2: self.bc2,
                3: self.bc3,
                4: self.bc4,
                5: self.bc5,
                6: self.bc6,
                7: self.bc7,
                8: self.bc8,
            }

            btn_table[which].setStyleSheet("background-color: rgb(%s,%s,%s);"%(color.red(),color.green(),color.blue()))
            self.theme_manager.colors[self.theme_manager.theme][which-1] = color


    def clear_filter(self):
        self.filterCombo.clearSelection()

    def gen_balance_matrix(self,detailed=True):
        # generates a balance sheet matrix for all agents
        # :param: detailed: show large matrix or aggregate individual rows?

        try:
            combined_balance =  defaultdict(lambda: {"Item":[],"Assets":[],"Liabilities": []})


            for filedata in self.entry_data:

                agent1 = filedata["agent1"].strip()
                agent2 = filedata["agent2"].strip()

                assets1 = filedata["a1"]
                liabs1 = filedata["l1"] #+ filedata["e1"] + "\n"

                assets2 = filedata["a2"]
                liabs2 = filedata["l2"] #+ filedata["e2"] + "\n"

                if detailed:
                    subject = " (%s)\n" % filedata["subject"]
                else:
                    subject = "\n"
                my_assets1 = []
                my_liabs1 = []
                my_assets2 = []
                my_liabs2 = []

                for i in assets1.split("\n"):
                    if i.strip().startswith("+"):
                        my_item = i.split("+")[1] + subject
                        sign = "+"
                    elif i.strip().startswith("-"):
                        my_item = i.split("-")[1] + subject
                        sign = "-"
                    else:
                        break
                    combined_balance[agent1]["Item"].append(my_item)
                    combined_balance[agent1]["Assets"].append(sign+filedata["quantity"]+"\n")
                    combined_balance[agent1]["Liabilities"].append("")

                for i in assets2.split("\n"):
                    if i.strip().startswith("+"):
                        my_item = i.split("+")[1] + subject
                        sign = "+"
                    elif i.strip().startswith("-"):
                        my_item = i.split("-")[1] + subject
                        sign = "-"
                    else:
                        break
                    combined_balance[agent2]["Item"].append(my_item)
                    combined_balance[agent2]["Assets"].append(sign+filedata["quantity"]+"\n")
                    combined_balance[agent2]["Liabilities"].append("")


                for j in liabs1.split("\n"):
                    if j.strip().startswith("+"):
                        my_item = j.split("+")[1] + subject
                        sign = "+"

                    elif j.strip().startswith("-"):
                        my_item = j.split("-")[1] + subject
                        sign = "-"
                    else:
                        break
                    combined_balance[agent1]["Item"].append(my_item)
                    combined_balance[agent1]["Liabilities"].append(sign+filedata["quantity"]+"\n")
                    combined_balance[agent1]["Assets"].append("")

                for j in liabs2.split("\n"):
                    if j.strip().startswith("+"):
                        my_item = j.split("+")[1] + subject
                        sign = "+"

                    elif j.strip().startswith("-"):
                        my_item = j.split("-")[1] + subject
                        sign = "-"
                    else:
                        break
                    combined_balance[agent2]["Item"].append(my_item)
                    combined_balance[agent2]["Liabilities"].append(sign+filedata["quantity"]+"\n")
                    combined_balance[agent2]["Assets"].append("")



            print(combined_balance)

            dfs = []
            for k,v in combined_balance.items():
                dv = pd.DataFrame(v)
                dv = dv.rename(columns={"Liabilities":"Liabilities (%s)"%k, "Assets": "Assets (%s)"%k})

                if not detailed:
                    aggregation_functions = {}
                    for col in dv.columns:
                        if col == "Item":
                            aggregation_functions[col] = "first"
                        else:
                            aggregation_functions[col] = "sum"
                    dv = dv.groupby(dv['Item']).aggregate(aggregation_functions)
                    dv = dv.drop(columns="Item")

                dfs.append(pd.DataFrame(dv))


            df = pd.concat(dfs,axis=1) #,keys =combined_balance.keys())
            print(df.to_string())
            df = df.replace(np.nan,"")



            model = PandasModel(df)
            mview = MatrixViewer(model,parent=self)

            # mview.webView.setHtml(df_html)
            if not self.test_mode:
                mview.show()

        except Exception as e:
            self.notify(title="Error",message="Error:" + str(e))


    def edit_mainloop(self):
        try:
            print("self.mainloop_str",self.mainloop_str)
            lines = self.mainloop_str

            my_edit = self.mainloop_editor # MainLoopEditor(parent=self, text=lines)
            my_edit.set_text(lines)
            my_edit.setStyleSheet(self.theme_manager.get_background_style())
            my_edit.setStyleSheet(self.theme_manager.get_stylesheet("main"))
            my_edit.start_watchdog(self.current_file)
            my_edit.show()

        except Exception as e:
            self.notify("Could not edit mainloop file. Have you saved the project yet?\n"  + str(e), title="Error")

    def restore_original_size(self):
        self.setFixedSize(1821,1010)
        self.setMaximumSize(40000,40000)

    def flip_height(self):
        if self.flipped:
            W = self.frameGeometry().width()
            H = self.frameGeometry().height()

            self.setMinimumSize(self.last_width,self.last_height)
            # self.setMaximumSize(self.last_width,self.last_height)
            self.setMaximumSize(40000,40000)
            # self.setMinimumSize(400,400)

            # W = self.frameGeometry().width()
            # self.FlipHeightButton.setGeometry(int(W)-81-25,5,81,21)

            self.flipped = False
        else:
            W = self.frameGeometry().width()
            H = self.frameGeometry().height()
            self.last_width = W
            self.last_height = H

            self.setFixedSize(800,70)

            #W = self.frameGeometry().width()
            #self.FlipHeightButton.setGeometry(int(W)-81-25,5,81,21)

            self.flipped = True


    def change_alert(self):
        self.made_changes = True
        # self.udpateButton.setText("Update Values *")

    def show_output_display(self):
        # shows the logger display for output quantities

        try:

            path = os.path.dirname(self.current_file)+"/output/"
            print("[DEBUG MESSAGE] open output display in path", path)

            output_display = OutputDisplay(self,path = path)
        except Exception as e:
            self.notify(str(e),title="Error")



    def save_and_build(self):

        # -- create new status signal

        self.worker.switch_state()
        # ---

        self.save()

        a = []
        for ce in CodeEditor.instances.values():
            names = ce.save_and_build()
            if names is not None:
                a.append(names)

        for ai in a:
            if ai[0] in CodeEditor.instances:
                CodeEditor.instances[ai[0]] = None
                del CodeEditor.instances[ai[0]]
            CodeEditor.instances[ai[1]] = ai[2]

        print("\nNEW INSTANCES\n", CodeEditor.instances)
        

        try:
            self.build_project(silent=True)
            self.statusBar().showMessage("Saved " + self.current_file)
            self.settings_editor.mtime = time.time()
            
        except Exception as e:
            # self.notify(str(e),title="Exception")
            print(str(e))



    def run_project(self):

        self.save_and_build()

        # self.show_output_display()

        self.setCursor(Qt.WaitCursor)

        try:
            # self.tabWidget.setCurrentIndex(1)

            #filename = os.path.dirname(self.current_file) + "/python_code/mainloop.py"
            filename = os.path.dirname(self.current_file) + "/runner.py"
            folder = os.path.dirname(self.current_file) + "/"

            if " " in filename or " " in folder:
                self.notify(title="Invalid file name", message="There are spaces in your folder or file name. This might cause problems.")

            print("lookup", filename, "in", folder)

            old_dir = os.getcwd()
            # print("old_dir",old_dir)

            os.chdir(folder)
            cmd = "conda activate attune /k python %s" % filename
            print("COMMAND", cmd)
            os.system("start cmd     %s" % cmd)

            os.chdir(old_dir)

        except Exception as e:

            self.notify(str(e),title="")
            self.setCursor(Qt.ArrowCursor)

        self.setCursor(Qt.ArrowCursor)

    def build_project(self,silent=False,overwrite=False):

        #folder = QFileDialog.getExistingDirectory (self, 'Build Project...', os.getcwd())

        if self.current_file is None:
            self.notify(message="Cannot build project. Please save to file first.",title="Error")
            return

        folder = os.path.dirname(self.current_file)
        print("build project in ", folder)

        try:
            os.mkdir(folder + "/mamba_code/")
        except:
            pass

        try:
            os.mkdir(folder + "/python_code/")
        except:
            pass

        try:
            os.mkdir(folder + "/output/")
        except:
            pass

        try:

            for agent, code in self.drawcanvas.code_data.items():
                if agent in CodeEditor.instances: # only convert edited code

                    # write mamba code for completeness
                    path = folder + "/mamba_code/%s.py" % agent # former .txt

                    print("path",path)

                    with open(path, "w") as file:
                        file.write(code)

                    # write python code
                    path = folder + "/python_code/%s.py" % agent.lower()

                    print("path",path)

                    with open(path, "w") as file:
                        new_code = convert_code(code.split("\n"))[0]
                        new_code = new_code.encode("utf-8").decode('cp1252')
                        file.write(new_code) # convert using the mamba interpreter

            # write settings file
            with open(folder + "/settings.yml","w") as file:
                file.write(self.settings_str)

            # write the runner file
            if self.mainloop_str == "" or overwrite:
                with open(folder+"/runner.py","w") as file:
                    file.write("from python_code.mainloop import run\n\nrun()\n")

            # write main simulation file
            with open(folder + "/python_code/mainloop.py","w") as file:
            #with open(folder + "./mainloop.py","w") as file:
                if self.mainloop_str == "" or overwrite:

                    if overwrite:
                        yes = self.ask_question('', "WARNING - You are about to create a fresh main script. This could potentially overwrite previous versions (if any).\nThis operation cannot be reverted. Continue?")
                        if not yes:
                            return

                    if overwrite and self.mainloop_str != "":
                        with open(folder + "/python_code/mainloop_backup.py","w") as backupfile:
                        #with open(folder + "./mainloop_backup.py","w") as backupfile:
                            backupfile.write(self.mainloop_str.replace("\t","    "))

                    simu_str = """
\"\"\"
This the main ABM Simulation file
Cretaed with the sfctools GUI

@author: <Your name>
@date: <Your date>
\"\"\"

from sfctools import Agent, World, Settings, Clock, FlowMatrix
"""
                    for agent in self.drawcanvas.code_data.keys():
                        simu_str += "from python_code.%s import %s\n" % (agent.lower(),agent.capitalize())

                    simu_str += """

def iter():
    \"\"\"
    this is one iteration
    \"\"\"

    # TODO modify iteration here
"""

                    for agent in self.drawcanvas.code_data.keys():
                        a = agent.capitalize()
                        simu_str += "\tfor a in World().get_agents_of_type('%s'):\n\t\tprint('Do something with' + str(a))\n\n" % (a)
                    simu_str += """\n
def run():
    \"\"\"
    this is the main simulation loop
    \"\"\"
"""


                    simu_str += """\n

    Settings().read(\"settings.yml\") # read settings file

    \"\"\"
    Simulation parameters
    \"\"\"

    # number of agents to be created
"""

                    for agent in self.drawcanvas.code_data.keys():
                        simu_str += "\tN_%s = 1\n" % agent.capitalize()
                    simu_str += """
    # TODO^ set the correct value

    # number of simulation steps
    T = 100

    # TODO^ set the correct values

    # create Agents:
"""
                    for agent in self.drawcanvas.code_data.keys():
                        a = agent.capitalize()
                        simu_str += "\t[%s() for i in range(N_%s)]\n" % (a,a)

                    simu_str += "\n"
                    simu_str += "\t# inter-link agents \n"

                    simu_str += "\tWorld().link()\n\n"

                    # for agent in self.drawcanvas.code_data.keys():
                    #    a = agent.capitalize()
                    #    simu_str += "\t[i.link() for i in %s_pile]\n" % (a)

                    simu_str += """
    for i in range(T):
        iter()

        # TODO write outputs here ...

        Clock().tick()

    print(FlowMatrix().to_string())
"""
                    self.mainloop_str = simu_str

                else:
                    simu_str = self.mainloop_str

                print("SIMU STR", simu_str)
                file.write(simu_str.replace("\t","    "))

                if not silent:
                    self.notify("Project files built!",title="Success")

                self.gen_code() # generate transactions.py

        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            self.notify("Could not build project.\n" + str(exception_object) + str(exception_traceback),title="Error on Project Build")

    def auto_backup(self):
        try:
            folder = self.current_file
            if folder is not None:
                self.saveas(folder[:-6] +"_autobackup.sfctl") # makes a backup file
            else:
                # self.notify("You are working on a blank project file. Please save your changes soon.", title="Warning")
                self.statusBar().showMessage("WARNING: You are working on a blank project file. Please save your changes soon.")
        except Exception as e:
            self.notify(str(e), title="Error on AutoBackup")

    def edit_settings(self):
        if self.settings_str =="" or self.settings_str is None:
            self.notify(message="Something went wrong. Have you built the project?",title="Error")
            return

        # my_edit = SettingsEditor(parent=self, text=self.settings_str)
        self.settings_editor.show()
        self.settings_editor.rebuild_table()

    def edit_graph_agent(self):
        self.drawcanvas.edit_agent()

    def change_graphmode_select(self):

        self.drawcanvas.mode = "select"

    def change_graphmode_drag(self):

        self.drawcanvas.mode = "drag"

    def arrange_pretty(self):
        self.update_table()
        self.drawcanvas.arrange_pretty()

    def update_graphics_data(self, box, conn):
        pass


    def switch_theme(self):


        # from qt_material import apply_stylesheet

        if self.theme_manager.theme == "dark":
            self.theme_manager.theme = "bright"

        elif self.theme_manager.theme == "bright":
            self.theme_manager.theme = "dark"


        self.setStyleSheet(self.theme_manager.get_stylesheet("main"))

        self.theme_manager.restore_buttons()

        self.tabWidget_2.setStyleSheet(self.theme_manager.get_background_style())
        self.dockWidget_3.setStyleSheet(self.theme_manager.get_background_style())
        self.dockWidget_4.setStyleSheet(self.theme_manager.get_background_style())
        self.dockWidget_5.setStyleSheet(self.theme_manager.get_background_style())

        self.widget.setStyleSheet(self.theme_manager.get_background_style())

        self.dockWidget_7.setStyleSheet(self.theme_manager.get_background_style())
        self.tabWidget.setStyleSheet(self.theme_manager.get_background_style())

        for ce in CodeEditor.instances.values():
            ce.setStyleSheet(self.theme_manager.get_background_style())

        self.agent1Edit.setStyleSheet(self.theme_manager.get_background_style())
        self.agent2Edit.setStyleSheet(self.theme_manager.get_background_style())

        try:

            if MainLoopEditor.instance is not None:
                inst = MainLoopEditor.instance
                inst.setStyleSheet(self.theme_manager.get_background_style())
                inst.setStyleSheet(self.theme_manager.get_stylesheet("main"))

        except:

            pass

        self.update_table()

        # self.transactionView.setStyleSheet(self.theme_manager.get_table_style())

    def ask_question(self,title,message):
        # ask a question yes / no
        msg = QMessageBox(QMessageBox.Question,
                title, message,buttons=QMessageBox.Yes | QMessageBox.No,
                parent=self)
        msg.setWindowTitle(title)
        msg.setStyleSheet(self.theme_manager.get_notification_style())
        msg.exec_()
        reply = msg.standardButton(msg.clickedButton())

        if reply == msg.Yes:
            return True
        else:
            return False

    def notify(self,message,title):
        #msg = QMessageBox(self)
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        #msg.setStyleSheet(self.stylesheet)
        # get background color from theme manager
        # get foreground color from theme manager
        style = self.theme_manager.get_notification_style()
        msg.setStyleSheet(style)
        msg.open()


    def cleanup_transaction_data(self,data):
        """
        cleans up transaction data from old file versions
        """
        try:
            print("old_data",data)
            # data = dict(data)
            new_data = {"agents":{},"transactions":[],"box_positions":{}, "label_positions":{},"theme":None, "options":None} # data.copy()
            # new_data["transactions"] = data["transactions"].copy()

            for k,v in data.items():

                if k == "options":
                    new_data["options"] = data[k]

                if k == "theme":
                    new_data["theme"] = data[k] # {"globaltheme": bright/dark, "colors": colors} # load the color theme

                if k == "agents":
                    for k2,v2 in data[k].items():

                        # 1. rename agent
                        print("RENAME AGENTS...")
                        new_code_lines = []

                        for line in v2.split("\n"):
                            if "AGENT" in line: #  and len(line) >= 9:
                                nline = line[:9] + camel(line[9]) + line[10:]
                                print("   renamed", line,nline)
                            
                            elif "CLASS" in line: #
                                nline =  line[:9] + camel(line[9]) + line[10:]
                                print("   renamed", line,nline)

                            else:
                                nline = line # "NOT FOUND" # line
                            # print("nline",nline,"old",v2)

                            new_code_lines.append(nline)
                            
                            pass

                        new_code = "\n".join(new_code_lines)

                        agent_name = camel(str(k2))
                        print("    agent name", str(k2), "->" , camel(str(k2)))


                        if str(k2) in data["box_positions"]: # try if agent is placed somewhere

                            new_data["agents"][agent_name] = new_code

                            # 2. assign new box position
                            print("ASSIGN NEW BOX POSITIONS...")

                            old_pos = data["box_positions"][str(k2)]
                            new_data["box_positions"][agent_name] = old_pos

                else:
                    new_data[k] = v

            print("RENAME TRANSACTIONS...")
            # 3. rename transactions
            try:
                for i,t in enumerate(list(data["transactions"])):
                    new_data["transactions"][i]["agent1"] = camel(data["transactions"][i]["agent1"]) #.capitalize()
                    new_data["transactions"][i]["agent2"] = camel(data["transactions"][i]["agent2"]) #.capitalize()
            except Exception as e:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                self.notify("Something wen wrong when inserting the transactions:\n" + str(e) + "\nLine:" + str(line_number),title="Error")

            return new_data
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno

            self.notify("Coult not optn the project file. Is it an old version?\n Error in Line %i: "%line_number + str(e),title="Error")

    def notify_tooltip(self,which):
        tt = which.toolTip ()
        self.notify(title="Tip",message=str(tt))


    def resizeEvent(self, event):
        print("resize")

        #self.drawcanvas.parent.resize_frame()
        QtWidgets.QMainWindow.resizeEvent(self, event)

        # resize transaction
        w = 741
        h = 191 + max(0,self.frameGeometry().height()-985)
        self.transactionView.parent = self.dockWidget_5
        # self.transactionView.setGeometry(30,65,w,h) # 30,670,w,h)

        #self.label_17.setGeometry(10,self.frameGeometry().height()-150,131,89) # logo
        #self.label_17.setVisible(False)

        self.radioButton.setGeometry(0,self.frameGeometry().height()-28,22,22)

    def browse(self):

        try:
            filename = QFileDialog.getOpenFileName(self, 'Open file',os.getcwd(), "attune Files (*.sfctl);;MAMBA Files (*.mamba);;Transaction Files (*.trans)")[0]
        except:
            self.notify("Seems as if the projects folder does not yet exist. please create it manually in the parent directory of src", title="Projects folder")


        # remove all tabs from tab widget
        for i in range(1,self.tabWidget.count()):
            tab = self.tabWidget.widget(1)
            self.tabWidget.removeTab(1)
            del tab

        CodeEditor.instances = {}

        filename_backup = self.filename
        current_file_backup = self.current_file

        self.filename = filename
        self.current_file = filename

        self.mainloop_editor.start_watchdog(self.current_file)
        self.settings_editor.start_watchdog(self.current_file)

        self.label_fname.setText(filename)

        try:
            print("FILENAME",filename)

            # load entries into the list
            with open(filename, 'r') as stream:

                try:
                    transaction_data = self.cleanup_transaction_data(yaml.safe_load(stream))
                except Exception as e:
                    self.notify("Error retreiving the transaction data from the source file. Aborting.\n"+str(e),title="Error")

                print("transaction_data",transaction_data)
                try:

                    # try to load notes
                    if "notes" in transaction_data:
                        self.notesEdit.setPlainText(transaction_data["notes"])

                    # try to load color theme
                    if transaction_data["theme"] is not None:
                        try:
                            theme_fname = transaction_data["theme"]["colors"]
                            gtheme = transaction_data["theme"]["globaltheme"]
                            if self.theme_manager.theme != gtheme:
                                self.switch_theme()
                            self.theme_manager.load_colors(theme_fname)

                        except:
                            self.statusBar().showMessage("Could not load color theme. Fallback to stanard theme")

                    # new format
                    self.entry_data = transaction_data["transactions"]
                    self.drawcanvas.clear(clearall=True)
                    # add the helper agents

                    # self.notify(str(transaction_data), title="Transaction Data")
                    
                    for k,v in transaction_data["agents"].items():
                        self.drawcanvas.add_agent(k) # .capitalize())
                        print("Add agent", k) #.capitalize())

                    # add the transactions (connectors and boxes)
                    self.update_table()

                    # load agent's codes

                    # first, compare if the code in the file tree (if any) corresponds to the code in the .sfctl file

                    # check if file tree is existent
                    my_agents = list(transaction_data["agents"].keys())

                    # get directory from filename
                    try:
                        print("CHECK DIRECTORY FOR UPDATES", filename)
                        filepath = os.path.dirname(os.path.abspath(filename))
                        mamba_path = filepath + "/mamba_code"
                        print("mamba path",mamba_path)

                        msg = "I have detected a deviation between the /mamba_code/ directory and the code stored in this file!"
                        msg += " Affected files:\n\n"

                        sub_names = next(os.walk(mamba_path), (None, None, []))[2]  # [] if no file
                        alt_transaction_data = {}
                        alt_diffs = {}

                        for fi in sub_names:

                            # check filename for agent
                            aname = camel(fi[:-4]) # .capitalize()

                            print("File ",aname)
                            if aname in my_agents:

                                # read this file
                                with open(mamba_path+"/" + fi,"r") as file:
                                    code = file.read()

                                    # print("dev mamba folder: ",code)
                                    # print("dev sfctl file:", transaction_data["agents"][aname])

                                    if code.strip() != transaction_data["agents"][aname].strip():

                                        print("DEVIATION detected in ",aname)


                                        alt_transaction_data[aname] = code

                                        diff =  [li for li in difflib.ndiff(code.strip(), transaction_data["agents"][aname].strip()) if li[0] != ' ']
                                        alt_diffs[aname] = str(diff)

                                        strdiff = str(diff).strip()

                                        if len(strdiff) > 40:
                                            strdiff = strdiff[:7] + "..."
                                        else:
                                            strdiff = strdiff

                                        msg += fi + ": " + strdiff + "\n"
                                        print(diff)
                                        print("\n")

                        msg += "\nDo you want to adapt the external changes?"
                        # self.notify(msg,title="Changes Detected")

                        if len(alt_transaction_data) > 0:

                            qm = QMessageBox(self)
                            qm.setWindowTitle("Caution")
                            # qm.setText(message)
                            style = self.theme_manager.get_notification_style()
                            qm.setStyleSheet(style)


                            ret = qm.question(self,'Caution', msg , qm.Yes | qm.No)

                            if ret == qm.Yes:
                                for k,v in alt_transaction_data.items():
                                    transaction_data["agents"][k] = alt_transaction_data[k]
                            else:
                                pass

                    except Exception as e:
                        print("SOMETHING WENT WRONG")
                        print(str(e))
                    
                    #
                    print("UPDATE DRAW CANVAS")
                    self.drawcanvas.code_data = transaction_data["agents"]
                    self.drawcanvas.box_position_data = transaction_data["box_positions"]
                    self.drawcanvas.label_position_data = transaction_data["label_positions"]

                    print("BOX POSITIONS...")
                    for k,v in self.drawcanvas.box_position_data.items():
                        print("(1)", k,v)
                        self.drawcanvas.old_positions[k] = (v["x"], v["y"])
                        # self.notify(str(v), title="test")
                    for k,v in self.drawcanvas.label_position_data.items():
                        print("(2)", k,v)
                        self.drawcanvas.old_positions[k] =  (v["x"], v["y"])
                        # self.notify(str(v), title="test")

                    print("CODE DATA",transaction_data["agents"])

                    # move the boxes to the saved positions
                    
                    self.drawcanvas.reposition() # transaction_data["box_positions"])

                    try:
                        self.drawcanvas.reposition_labels() # transaction_data["label_positions"])
                    except:
                        print("Could not load label positions. Resetting to zero.")



                    print("Settings", self.settings_str)
                    self.settings_str = transaction_data["settings"]

                    try:
                        self.mainloop_str = transaction_data["mainloop"]
                    except:
                        print("NO MAINLOOP FOND. SKIPPING")
                    
                    try:
                        self.statusBar().showMessage("Opened file " + filename)
                    except:
                        pass

                except Exception as e:

                    # old format as fallback
                    self.entry_data = transaction_data["transactions"]
                    self.drawcanvas.code_data = transaction_data["agents"]
                    self.update_table()
                    print("wARNING - FALLBACK TO OLD FILE FORMAT!")
                    print(str(e))

                # self.fileEdit.setText(filename)

        except Exception as e :

            # self.notify(message="Something went wrong when opening the file:\n %s"%str(e),title="Error")
            self.filename = filename_backup
            self.curent_file = current_file_backup
            if str(self.current_file) != "":
                self.statusBar().showMessage("Cancelled. Restored file '%s'" % str(self.current_file))

        # update transaction table
        self.update_table()

        # update theme
        self.theme_manager.restore()

        try:
            fname, file_extension = os.path.splitext(self.filename)
            self.theme_manager.load_colors(fname + ".sfctheme")

        except Exception as e:
            print("could not load theme: ", str(e))

        # update boxes
        for box in self.drawcanvas.boxes:
            box.edit_agent()

        # update display options
        try:
            if "options" in transaction_data:
                if transaction_data["options"] is not None:
                    self.set_options(transaction_data["options"])
        except Exception as e:
            print(str(e))


    def entry_to_vals(self, entry, agent, which):

        if not bool(regex.findall("([+-]+)", entry)):
            self.notify(message="Sign corrupted in entry %s (%s of %s)"%(entry,which,agent),title="Error")
            return None, None, None

        if regex.findall("([+-]+)", entry)[0] == "-":
            sign = "-"
        else:
            sign = "+"

        words = regex.findall("([\w\s><=]+)", entry)

        item = ""
        silent = False
        for word in words:
            if word != "s":
                item += word.strip() + " "
            elif word == "s":
                silent = True

        
        split_item = item.split(" ")
        item = split_item[0].strip()

        # third-party agent can be defined here as cross-reference
        ref_agent = None 
        direction = 0
        other = ""
        if len(split_item) > 2:
            ref_agent = split_item[1].strip()
            print("ref_agent", ref_agent)
            if ref_agent == "":
                ref_agent = None
            elif ref_agent.startswith(">"):
                # log the change on the other agent
                ref_agent = ref_agent[1:]
                direction = 1
            elif ref_agent.startswith("<"):
                # log the change on this agent 
                ref_agent = ref_agent[1:]
                direction = 0
            elif ref_agent.startswith("="): 
                # log the change in both directions
                ref_agent = ref_agent[1:]
                direction = 2
            other = split_item[2].strip()
        
        # self.notify("%s %s %s %s %s %s" % (sign, item, silent, ref_agent, direction, other), title="test")
        return sign, item, silent, ref_agent, direction, other
    

    def update_table(self):
        #self.selection_idx = None
        self.transactionView.setRowCount(0)

        # self.transactionView.model().setTorizontalHeaderItem( 0, QTableWidgetItem("Name"))
        # self.transactionView.model().setTorizontalHeaderItem( 1, QTableWidgetItem("Short Name"))
        # self.transactionView.model().setTorizontalHeaderItem( 2, QTableWidgetItem("Unidirectional"))
        # self.transactionView.model().setTorizontalHeaderItem( 3, QTableWidgetItem("Flow"))

        # insert new rows if needed
        row_count = self.transactionView.rowCount()

        if self.entry_data is None:
            self.notify("Data is empty or corrupted. Something went wrong", title="Fatal Error")
            return

        if row_count < len(self.entry_data):
            for i in range(len(self.entry_data)-row_count):
                self.transactionView.insertRow(row_count)
        
        self.drawcanvas.clear()
        self.filterCombo.clear()
        self.filter_entries = []

        print("-> ENTRY DATA", self.entry_data)

        
        try:
            print("   ... -> found transactions entry")
            for i, data in enumerate(self.entry_data):
                # exists1 = self.drawcanvas.check_exist(data["agent1"].capitalize())
                # exists2 = self.drawcanvas.check_exist(data["agent2"].capitalize())
                
                print("DATA", i, data)

                new_agent1 = camel(data["agent1"])
                new_agent2 = camel(data["agent2"])
                box1 = self.drawcanvas.add_agent(new_agent1) # .capitalize())
                box2 = self.drawcanvas.add_agent(new_agent2) #.capitalize())

                # correct number of connections for existing agents
                box1.n_connections = 0
                box2.n_connections = 0
            
            # update the data
            for i, data in enumerate(self.entry_data):
                print(data)

                self.transactionView.setItem(i, 0, QTableWidgetItem(data["subject"]))
                self.transactionView.setItem(i, 1, QTableWidgetItem(camel(data["agent1"]))) # .capitalize()))
                self.transactionView.setItem(i, 2, QTableWidgetItem(camel(data["agent2"]))) # .capitalize()))
                self.transactionView.setItem(i, 3, QTableWidgetItem(data["shortname"]))
                self.transactionView.setItem(i, 4, QTableWidgetItem(data["kind"]))
                self.transactionView.setItem(i, 5, QTableWidgetItem(str(data["uni-directional"])))
                self.transactionView.setItem(i, 6, QTableWidgetItem(str(data["quantity"])))
                # self.transactionView.selectionModel().selectedRows()

                box1 = self.drawcanvas.add_agent(camel(data["agent1"])) #.capitalize())
                box2 = self.drawcanvas.add_agent(camel(data["agent2"])) #.capitalize())

                my_items = []

                allentries = "\n".join([data["l1"], data["a1"], data["e1"], data["l2"], data["a2"], data["e2"]])
                for sub_item in allentries.split("\n"):
                    for sub_entry in sub_item.split("\n"):
                        entry = sub_entry.replace("-","").replace("+","").lstrip()
                        if entry !=  "":
                            my_items.append(entry)

                self.drawcanvas.add_connection(box1, box2, name=data["shortname"],subject=data["subject"],items=my_items)

                # reduce the filter values
                x = []
                for val in my_items + [data["agent1"], data["agent2"]]:
                    x.append(val.split(" ")[0].strip())
                my_items = list(set(x))

                # update the filter values 
                for entry in my_items:
                    if entry not in self.filter_entries:
                        if entry not in [data["agent1"], data["agent2"]]:
                            self.filter_entries.append(entry)

        except Exception as e:
            tb_str = tb_str = "".join(traceback.format_tb(e.__traceback__))
            self.notify(str(e)+"\n" + "\n" + str(tb_str), title="Error")

        try:
            # search for a match in the filter

            found_idxs = []
            search_str = self.FilterlineEdit.text()

            if search_str != "":
                try:
                    for i in range(self.transactionView.rowCount()):

                        for j in range(self.transactionView.columnCount()):

                            entry_str = self.transactionView.item(i,j).text()

                            if entry_str.find(search_str) > -1:

                                found_idxs.append(i)
                except Exception as e:
                    print("Exception:", str(e))

            for found_idx in found_idxs:
                # highlight occurances
                for j in range(self.transactionView.columnCount()):
                    try:

                        if self.theme_manager.theme == "bright":

                            # light mode
                            self.transactionView.item(found_idx, j).setBackground(QtGui.QColor(227, 166, 166))
                            self.transactionView.item(found_idx, j).setForeground(QtGui.QColor(180, 18, 18))

                        else:

                            # dark mode
                            self.transactionView.item(found_idx, j).setBackground(QtGui.QColor(120, 120, 120))
                            self.transactionView.item(found_idx, j).setForeground(QtGui.QColor(50, 50, 50))

                    except:
                        pass
                        # avoids None pointer when a transaction is deleted
        except:
            pass


        for entry in self.filter_entries:
            self.filterCombo.addItem(entry)

        self.drawcanvas.reposition()
        self.drawcanvas.reposition_labels()

        self.drawcanvas.update()
        self.made_changes = False




    def move_down(self):
        # move selected transaction up in table
        selected_rows = sorted(set(index.row() for index in
                          self.transactionView.selectedIndexes()))

        if len(selected_rows) == 0:
            print("no selected rows")
            return

        selection = selected_rows[0]

        number_of_items = self.transactionView.rowCount()
        number_of_columns = self.transactionView.columnCount()

        try:

            if selection < number_of_items-1:
                currentRow = self.transactionView.currentRow()

                for j in range(number_of_columns):
                    currentItem = self.transactionView.takeItem(currentRow,j)
                    switchItem = self.transactionView.takeItem(currentRow+1,j)

                    self.transactionView.setItem(currentRow + 1, j, currentItem)
                    self.transactionView.setItem(currentRow, j, switchItem)

                    switch_entry = self.entry_data[currentRow+1]
                    current_entry = self.entry_data[currentRow]

                    self.entry_data[currentRow] = switch_entry
                    self.entry_data[currentRow+1] = current_entry

                self.transactionView.clearSelection()
                self.transactionView.setCurrentCell(currentRow+1,0)

        except Exception as e:
            self.notify("error: "+str(e), title="Error")


    def move_up(self):
        # move selected transaction up in table
        selected_rows = sorted(set(index.row() for index in
                          self.transactionView.selectedIndexes()))

        if len(selected_rows) == 0:
            print("no selected rows")
            return

        selection = selected_rows[0]

        number_of_items = self.transactionView.rowCount()
        number_of_columns = self.transactionView.columnCount()

        try:

            if selection >= 1:
                currentRow = self.transactionView.currentRow()

                for j in range(number_of_columns):
                    currentItem = self.transactionView.takeItem(currentRow,j)
                    switchItem = self.transactionView.takeItem(currentRow-1,j)

                    self.transactionView.setItem(currentRow - 1, j, currentItem)
                    self.transactionView.setItem(currentRow, j, switchItem)

                    switch_entry = self.entry_data[currentRow-1]
                    current_entry = self.entry_data[currentRow]

                    self.entry_data[currentRow] = switch_entry
                    self.entry_data[currentRow-1] = current_entry

                self.transactionView.clearSelection()
                self.transactionView.setCurrentCell(currentRow-1,0)

        except Exception as e:
            self.notify("error: "+str(e), title="Error")

    def data_select(self):

        #selected_rows = self.transactionView.selectionModel().selectedRows()
        selected_rows = sorted(set(index.row() for index in
                          self.transactionView.selectedIndexes()))

        if len(selected_rows) == 0:
            print("no selected rows")
            return

        selection = selected_rows[0]

        self.row_select(selection)
        self.made_changes = False


    def data_select_where(self, expr):
        print("data select where",expr)

        for i in range(self.transactionView.rowCount()):
                my_entry = self.transactionView.item(i, 3).text()

                print("...",i,my_entry)
                if my_entry == expr or my_entry.lower() == expr.lower():

                    self.row_select(i)
                    return

    def row_select(self,selection):

        # color the selected row
        # gb(233, 234, 227);

        self.selection_idx = None

        if self.made_changes:
            yes = self.ask_question("Warning", "You are about to change to another transaction and withdraw the changes you made. Continue?")
            if not yes:
                return

        try:
            """
            if self.selection_idx is not None:
                for i in range(self.transactionView.columnCount()):
                    self.transactionView.item(self.selection_idx, i).setBackground(QtGui.QColor(233, 234, 227))
                    self.transactionView.scrollToItem(self.transactionView.item(selection, i))
            for i in range(self.transactionView.columnCount()):
                self.transactionView.item(selection, i).setBackground(QtGui.QColor(59, 59, 159))
                self.transactionView.scrollToItem(self.transactionView.item(selection, i))
            """
            self.transactionView.clearSelection()
            self.transactionView.setCurrentCell(selection,3)
        
        except:
            pass

        try:
            self.selection_idx = selection
            print("selection",selection)

            data = self.entry_data[selection]

            print("data", data)

            self.AssetListLeft.clear()
            self.LiabilityListLeft.clear()
            self.LiabilityListRight.clear()
            self.AssetListRight.clear()
            self.EquityListLeft.clear()
            self.EquityListRight.clear()

            self.AssetListLeft.setPlainText(data["a1"])
            self.AssetListRight.setPlainText(data["a2"])
            self.LiabilityListLeft.setPlainText(data["l1"])  # +data["e1"])
            self.LiabilityListRight.setPlainText(data["l2"]) # +data["e2"])
            self.EquityListLeft.setPlainText(data["e1"])
            self.EquityListRight.setPlainText(data["e2"])

            self.agent1Edit.setText(camel(data["agent1"])) #.capitalize())
            self.agent2Edit.setText(camel(data["agent2"])) # .capitalize())

            self.registerFlowBox.setCurrentIndex(self.registerFlowBox.findText(str(data["log transaction"])))

            cashflow1 = data["cashflow1"] or "None"
            cashflow2 = data["cashflow2"] or "None"
            self.comboCashLeft.setCurrentIndex(self.comboCashLeft.findText(str(cashflow1)))
            self.comboCashRight.setCurrentIndex(self.comboCashRight.findText(str(cashflow2)))

            trtype = data["kind"] or "KA->KA"
            self.editType.setCurrentIndex(self.editType.findText(str(trtype)))

            ics1 = data["income1"] or "None"
            ics2 = data["income2"] or "None"
            self.comboIncomeLeft.setCurrentIndex(self.comboIncomeLeft.findText(ics1))
            self.comboIncomeRight.setCurrentIndex(self.comboIncomeRight.findText(ics2))

            self.editQuantity.setText(data["quantity"])
            self.editSubject.setText(data["subject"])

            self.drawcanvas.highlight_connector(data["shortname"])

            if "description" in data:
                self.editDescription.setText(data["description"])
            else:
                self.editDescription.setText("")
            self.editShortname.setText(data["shortname"])


            if "add_args" in data:
                self.editAddArgs.setText(data["add_args"])
            else:
                self.editAddArgs.setText("")

            if "add_code" in data:
                self.editAddCode.setPlainText(data["add_code"])
            else:
                self.editAddCode.setPlainText("")
            
            unidir = str(data["uni-directional"]) or "None"
            self.comboUnidir.setCurrentIndex(self.comboUnidir.findText(unidir))

        except Exception as e:
            self.notify(str(e),title="Error")

        self.made_changes = False

    def update_data(self):
        if self.selection_idx is None:
            return

        self.entry_data[self.selection_idx]["a1"] = self.AssetListLeft.toPlainText()
        self.entry_data[self.selection_idx]["a2"] = self.AssetListRight.toPlainText()
        self.entry_data[self.selection_idx]["l1"] = self.LiabilityListLeft.toPlainText()
        self.entry_data[self.selection_idx]["l2"] = self.LiabilityListRight.toPlainText()
        self.entry_data[self.selection_idx]["e1"] = self.EquityListLeft.toPlainText()
        self.entry_data[self.selection_idx]["e2"] = self.EquityListRight.toPlainText()

        self.entry_data[self.selection_idx]["a1"]  = self.AssetListLeft.toPlainText()
        self.entry_data[self.selection_idx]["a2"] = self.AssetListRight.toPlainText()
        self.entry_data[self.selection_idx]["l1"]  = self.LiabilityListLeft.toPlainText()
        self.entry_data[self.selection_idx]["l2"]  = self.LiabilityListRight.toPlainText()
        self.entry_data[self.selection_idx]["e1"]  = self.EquityListLeft.toPlainText()
        self.entry_data[self.selection_idx]["e2"]  = self.EquityListRight.toPlainText()

        only_rename = True
        if self.entry_data[self.selection_idx]["agent1"]  != self.agent1Edit.text():
            only_rename = False
        if self.entry_data[self.selection_idx]["agent2"]  !=self.agent2Edit.text():
            only_rename = False


        if not self.drawcanvas.check_exist(self.agent1Edit.text()):
            if self.agent1Edit.text().strip() != "":
                yes = self.ask_question('',"The agent %s does not exist.\nDo you wish to continue and automatically create a new agent?"%self.agent1Edit.text())
                if not yes:
                    return

        if not self.drawcanvas.check_exist(self.agent2Edit.text()):
            if self.agent2Edit.text().strip() != "":
                yes = self.ask_question('',"The agent %s does not exist.\nDo you wish to continue and automatically create a new agent?"%self.agent2Edit.text())
                if not yes:
                    return

        self.entry_data[self.selection_idx]["agent1"]  = camel(self.agent1Edit.text()) #.capitalize() # upper because agents are always uppercase
        self.entry_data[self.selection_idx]["agent2"]  = camel(self.agent2Edit.text()) #.capitalize()

        self.agent1Edit.setText(camel(self.agent1Edit.text())) #.capitalize())
        self.agent2Edit.setText(camel(self.agent2Edit.text())) #.capitalize())

        self.entry_data[self.selection_idx]["uni-directional"] = \
            str(self.comboUnidir.currentText())

        self.entry_data[self.selection_idx]["log transaction"] =\
            str(self.registerFlowBox.currentText())

        self.entry_data[self.selection_idx]["cashflow1"] = \
            str(self.comboCashLeft.currentText())
        self.entry_data[self.selection_idx]["cashflow2"] = \
            str(self.comboCashRight.currentText())

        self.entry_data[self.selection_idx]["kind"] = \
            str(self.editType.currentText())

        self.entry_data[self.selection_idx]["income1"] = \
            str(self.comboIncomeLeft.currentText())
        self.entry_data[self.selection_idx]["income2"] = \
            str(self.comboIncomeRight.currentText())


        if only_rename:

            self.drawcanvas.rename_connection(self.entry_data[self.selection_idx]["shortname"] , str(self.editShortname.text()))

        else:
            self.drawcanvas.remove_connection(self.entry_data[self.selection_idx]["shortname"]) #, str(self.editSubject.text()))

            box1 = self.drawcanvas.add_agent(self.entry_data[self.selection_idx]["agent1"])
            box2 = self.drawcanvas.add_agent(self.entry_data[self.selection_idx]["agent2"])

            my_items = []
            data = self.entry_data[self.selection_idx]

            allentries = "\n".join([data["l1"], data["a1"], data["e1"], data["l2"], data["a2"], data["e2"]])
            for sub_item in allentries.split("\n"):
                for sub_entry in sub_item.split("\n"):
                    entry = sub_entry.replace("-","").replace("+","").strip()
                    if entry !=  "":
                        my_items.append(entry)


            self.drawcanvas.add_connection(box1,box2, str(self.editShortname.text()),subject=self.editSubject.text(),items=my_items)

        self.entry_data[self.selection_idx]["quantity"] = \
            str(self.editQuantity.text())

        self.entry_data[self.selection_idx]["subject"] = \
            str(self.editSubject.text())

        self.entry_data[self.selection_idx]["shortname"] = \
            str(self.editShortname.text())

        self.entry_data[self.selection_idx]["description"] = \
            str(self.editDescription.text())

        self.entry_data[self.selection_idx]["add_args"] = \
            str(self.editAddArgs.text())

        self.entry_data[self.selection_idx]["add_code"] = \
            str(self.editAddCode.toPlainText())



        self.update_table()

        print("data changed.")

        self.made_changes = False

        self.row_select(self.selection_idx)

        # self.udpateButton.setText("Update Values")

    def save(self):

        try:


            filename = self.current_file # statusBar().currentMessage()
            self.label_fname.setText(filename)

            if filename is not None:

                self.saveas(filename)

                # TODO maybe backup(?)
                # self.notify("File saved under %s" % filename,title="Ok")
                print("FILE SAVED!")
            else:
                self.save_dlg()

        except Exception as e:
            if filename != "":
                self.notify(str(e),title="Error")



    def save_dlg(self):
        try:

            filename = QFileDialog.getSaveFileName(self, 'Save file',
                                               os.getcwd(), "attune Files (*.sfctl)")[0]
            self.statusBar().showMessage("Saved file " + filename)

            current_file_backup = self.current_file

            if filename is not None and filename != "":
                self.label_fname.setText(filename)

                self.current_file = filename
                self.saveas(filename)

            # TODO maybe backup(?)

        except Exception as e:
            self.notify("Could not save project.",title="Error")
            self.current_file = current_file_backup


    def get_options(self):
        o1 = str(self.checkBox_2.isChecked())
        o2 = str(self.checkBox.isChecked())
        o3 = str(self.checkBox_4.isChecked())
        o4 = str(self.checkBox_5.isChecked())
        o5 = str(self.checkBox_3.isChecked())
        o6 = str(self.checkBox_6.isChecked())
        o7 = str(self.checkBox_8.isChecked())
        o8 = str(self.checkBox_9.isChecked())
        o9 = str(self.checkBox_raster.isChecked())

        return [o1,o2,o3,o4,o5,o6,o7,o8,o9]

    def set_options(self,new_options):
        # set display options
        if new_options is None:
            return

        o1,o2,o3,o4,o5,o6,o7,o8,o9 = new_options

        def str_to_bool(x):
            if x == "True":
                return True
            return False

        self.checkBox_2.setChecked(str_to_bool(o1))
        self.checkBox.setChecked(str_to_bool(o2))
        self.checkBox_4.setChecked(str_to_bool(o3))
        self.checkBox_5.setChecked(str_to_bool(o4))
        self.checkBox_3.setChecked(str_to_bool(o5))
        self.checkBox_6.setChecked(str_to_bool(o6))
        self.checkBox_8.setChecked(str_to_bool(o7))
        self.checkBox_9.setChecked(str_to_bool(o8))
        self.checkBox_raster.setChecked(str_to_bool(o9))


    def saveas(self, filename):
        
        ftheme = None
        
        try:
            ftheme = filename[:-5]+"sfctheme" # absolute file path
            folder,ftheme = os.path.split(ftheme) # convert to relative file path
            self.theme_manager.save_colors(ftheme)
        except:
            self.notify("Could not save color theme. proceeding without",title="Error")
        
        # drawcanvas code_data
        code_data = {}
        for k,v in self.drawcanvas.code_data.items():
            code_data[k] = str(v.encode("utf-8").decode('cp1252'))
            # fix some potential encoding errors
        
        try:
            print("FILENAME", filename)

            # load entries into the list
            with open(filename, 'w') as stream:

                data = {"transactions": self.entry_data,
                "agents": code_data,
                "box_positions": self.drawcanvas.box_positions(),
                "label_positions": self.drawcanvas.label_positions(),
                "settings": self.settings_str,
                "mainloop": self.mainloop_str,
                "theme": {"globaltheme": self.theme_manager.theme, "colors":ftheme},
                "notes": self.notesEdit.toPlainText(),
                "options": self.get_options(),
                }

                yaml.dump(data,stream)
        
        except Exception as e:
            self.notify(message=str(e), title="Error")


    def try_gen_matrix(self):
        try:
            self.gen_matrix()
        except Exception as e:
            self.notify("Error",str(e))

    def gen_matrix(self,mode="standard"):
        """
        generate flow matrix:

        :param mode: standard,excel,latex

        standard: shows matrix graphically
        excel: exports an excel file
        latex: not yet supported NOT AVAILABLE FOR NOW
        html: NOT AVAILABLE FOR NOW
        """

        flow_data = {}

        flow_data["CA"] = defaultdict(lambda: defaultdict(list))  # current account
        flow_data["KA"] = defaultdict(lambda: defaultdict(list))  # capital account

        # flow_data[KA or CA][subject][agent]
        if len(self.entry_data) == 0:
            self.notify(message="Cannot generate Matrix. Have you set up any transactions yet?",title="Error")
            return

        try:
            for filedata in self.entry_data:
                                """
                                evaluate transaction entries with the flow logger
                                """
                                subject = filedata["subject"].replace("_", " ").title()
                                kind = filedata["kind"]
                                log_flow = True
                                if filedata["log transaction"] == "False":
                                    log_flow= False
                                #   log_flow = bool(filedata["log transaction"])
                                print("LOG FLOW",log_flow,"raw",filedata["log transaction"])
                                quantity = filedata["quantity"]
                                agent1 = filedata["agent1"].replace("_", " ").title()
                                agent2 = filedata["agent2"].replace("_", " ").title()

                                # upper part of matrix
                                if log_flow:
                                    account_from = kind.split("->")[0]
                                    account_to = kind.split("->")[1]

                                    flow_data[account_from][subject][agent1].append("-" + str(quantity))
                                    flow_data[account_to][subject][agent2].append(str(quantity))

                                # lower part of matrix = changes in assets ans liabilities

                                a1 = filedata["a1"]  # + "\n"
                                e1 = filedata["e1"]  # + "\n"
                                l1 = filedata["l1"]  # + "\n"
                                a2 = filedata["a2"]  # + "\n"
                                e2 = filedata["e2"]  # + "\n"
                                l2 = filedata["l2"]  # + "\n"

                                # assets
                                for item_name in a1.split("\n"):  # + e1.split("\n"):
                                    if item_name != "":
                                        name = item_name[1:].lstrip().split(" ")[0].strip()
                                        sign = item_name[0]

                                        if sign == "+":
                                            flipped_sign = "-"
                                        else:
                                            flipped_sign = "+"

                                        if not "(s)" in name:
                                            flow_data["KA"]["Δ %s" % name][agent1].append(
                                                "(" + flipped_sign + quantity + ")")

                                for item_name in a2.split("\n"):  # + e2.split("\n"):
                                    if item_name != "":
                                        name = item_name[1:].lstrip().split(" ")[0].strip()
                                        sign = item_name[0]

                                        if sign == "+":
                                            flipped_sign = "-"
                                        else:
                                            flipped_sign = "+"

                                        if not "(s)" in name:
                                            flow_data["KA"]["Δ %s" % name][agent2].append(
                                                "(" + flipped_sign + quantity + ")")

                                # liabilities
                                for item_name in l1.split("\n"):
                                    if item_name != "":
                                        name = item_name[1:].lstrip().split(" ")[0].strip()
                                        sign = item_name[0]

                                        if not "(s)" in name:
                                            flow_data["KA"]["Δ %s" % name][agent1].append(
                                                "(" + sign + quantity + ")")

                                for item_name in l2.split("\n"):
                                    if item_name != "":
                                        name = item_name[1:].lstrip().split(" ")[0].strip()
                                        sign = item_name[0]

                                        if not "(s)" in name:
                                            flow_data["KA"]["Δ %s" % name][agent2].append(
                                                "(" + sign + quantity + ")")

            # print(flow_data)
            df_credit = pd.DataFrame(flow_data["CA"]).T
            df_capital = pd.DataFrame(flow_data["KA"]).T

            df_merge = pd.concat([df_credit, df_capital], axis=1, keys=['CA', 'KA']).swaplevel(0, 1,axis=1).sort_index(axis=1)


            # append new columns
            col_dict_ca = {}
            for col in df_credit.columns:
                col_dict_ca[col] = col + " (CA)"

            col_dict_ka = {}
            for col in df_capital.columns:
                col_dict_ka[col] = col + " (KA)"

            df_credit = df_credit.rename(columns = col_dict_ca)
            df_capital = df_capital.rename(columns=col_dict_ka)

            df_merge2 = pd.concat([df_credit, df_capital], axis=1)

            df_merge2 = df_merge2.reindex(sorted(df_merge2.columns), axis=1)
            df_merge2 = df_merge2.reindex(sorted(df_merge2.index), axis=0)

            df = df_merge.fillna(0.0).sort_index()


            def join_elements(my_item):
                if isinstance(my_item, list):
                    my_list = []
                    for subitem in my_item:
                        if subitem != "0":
                            my_list.append(subitem)

                    return "+".join(my_list)

                elif my_item == 0.0:
                    return "0"
                else:
                    return my_item

            df = df.applymap(join_elements)



            # sum over the columns

            def eval_sum(column):
                column = [str(c).replace("^", "**") for c in column]
                my_expr = "+".join(column)
                try:
                    return parse_expr(my_expr)
                except:
                    return my_expr



            df["Total"] = df.T.agg(eval_sum)  # df.T.sum()
            df.loc["Total"] = df.agg(eval_sum)
            print("TOTAL",df.loc["Total"])
            df_merge2["Total"] = df["Total"]

            # get the new columns

            # iterate through the columns
            print(df.columns)


            for column in df.columns:
                if column[0] != "Total":
                    print(column[0] + " "  + "(%s)" % column[1],df.loc["Total"][column])
                    df_merge2.loc["Total",column[0] + " "  + "(%s)" % column[1]] = df.loc["Total"][column]



            def simplify_expr(my_item):
                return simplify(my_item)

            df = df.applymap(simplify_expr)
            df_for_excel = df.copy()


            def abbreviate_zeros_latex(my_item):
                if my_item == "0" or my_item == 0:
                    return " .- "  # .- "
                else:
                    s = printing.latex(my_item, mode="inline") #  mode="inline")
                    print(s)
                    return s

            #df_backup = df.copy()
            df = df.applymap(abbreviate_zeros_latex)

            df_merge2 = df_merge2.replace(np.nan, '', regex=True)
            df_merge2 = df_merge2.replace("0", '', regex=True)
            df_merge2 = df_merge2.replace(0, '', regex=True)
            df_merge2 = df_merge2.replace(0.0, '', regex=True)

            # print(df.to_string())
            # df.iloc[0,0] = "$\\alpha$"

            pd.options.display.max_colwidth = None

            if mode == "html": # < NOT YET SUPPORTED

                df_html = """
        <html>
        <head>
        <title>Mathedemo</title>
        <script type="text/x-mathjax-config">
          MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
        </script>
        <script type="text/javascript"
          src="http://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
        </script>
        <link rel="stylesheet" href="mystyle.css">
        </head>

        <body>
        %s
        </body>
        </html>
        """%  df.to_html()

                pageSource = """
                             <html><head>
                             </head>
                             <body>
                             <p>asdf</p>
                             </body></html>
                             """

                # BLA

                # write page source to html
                if False:
                    # DEPRECIATED
                    path = os.path.dirname(os.path.abspath(__file__))
                    file = open(os.path.join(path,"files/mymatrix.html"),"w",encoding='utf-8')
                    file.write(df_html)
                    file.close()

            # QDesktopServices.openUrl(QUrl("./files/matrix.html"))

            if mode == "standard":
                model = PandasModel(df_merge2)
                mview = MatrixViewer(model,parent=self)

                # mview.webView.setHtml(df_html)
                if not self.test_mode:
                    mview.show()


            if mode == "latex": # < NOT YET SUPPORTED
                try:
                    self.convert_df_to_tex(df)
                except Exception as e:
                    self.notify(str(e),title="Error during Tex Conversion")

                # print("VIEW")
                # print(df_html)

            def convert_excel(my_item):
                if my_item == "0" or my_item == 0:
                    return " .- "  # .- "
                else:
                    s = pretty(my_item) # printing.latex(my_item) # ,mode="inline") #  mode="inline")
                    print(s)
                    return s

            if mode == "excel":
                try:
                    efilename = QFileDialog.getSaveFileName(self, 'Save file', os.getcwd(), "Excel Files (*.xlsx)")[0]

                    if efilename is not None and efilename != "":
                        df_for_excel = df_for_excel.applymap(convert_excel)
                        # path = os.path.dirname(os.path.abspath(__file__))
                        df_for_excel.to_excel(efilename) # "files/FlowMatrix_formatted.xlsx"))
                        # df_merge2.to_excel(os.path.join(path,efilename))    # "files/FlowMatrix.xlsx"))

                except Exception as e:
                    self.notify(str(e), title="Error during Excel conversion")

        except Exception as e:
            self.notify(str(e), title="Error during matrix generation")

    def remove_item(self):

        try:
            selected_rows = sorted(set(index.row() for index in
                                       self.transactionView.selectedIndexes()))

            if len(selected_rows) == 0:
                self.notify("no selected rows",title="Error")
                return

            selection = selected_rows[0]

            yes =  self.ask_question('',"Are you sure you want to remove the entry '%s'?"%self.entry_data[selection]["subject"])
            if yes:

                self.drawcanvas.remove_connection(self.entry_data[selection]["shortname"])

                self.transactionView.removeRow(selection)
                del self.entry_data[selection]

        except Exception as e:
            self.notify(str(e), title="Error")

        try:
            self.update_table()

        except Exception as e:
            self.notify(str(e), title="Error")


    def convert_df_to_tex(self,df):

        def wrapstring(s):
            # wraps string
            return textwrap.wrap(s, width=10)

        def abbreviate_zeros(my_item):
            if my_item == "0" or my_item == 0:
                return " .- "  # .- "
            else:
                my_item = str(my_item)
                max_len = 10
                if len(my_item) > max_len:
                    return my_item[:max_len] + "..."
                else:
                    return my_item

        df_backup = df.copy()

        df_latex = df.to_latex(longtable=False, escape=False).replace("Δ", "$\Delta$")

        df_latex = df_latex.replace("\\begin{tabular}", "\\begin{tabularx}{\\textwidth}")
        df_latex = df_latex.replace("\\end{tabular}", "\\end{tabularx}")
        df_latex = "\\begin{small}\n" + df_latex + "\n\end{small}"

        df_latex = df_latex.replace("\\left(", "(")
        df_latex = df_latex.replace("\\right)", ")")

        df_latex = df_latex.replace("{l", "{L{3cm}")

        df_latex = """
\\documentclass[a3paper,landscape]{article}
\\usepackage{booktabs}
\\usepackage{adjustbox}
\\usepackage[table]{xcolor}
\\usepackage{longtable}
\\usepackage{tabularx,ragged2e}
\\definecolor{Gray}{gray}{0.90}
\\definecolor{LightGray}{gray}{0.95}
\\definecolor{White}{rgb}{1,1,1}

\\newcolumntype{g}{>{\\columncolor{White}\\arraybackslash}L} %
\\newcolumntype{l}{>{\\columncolor{White}\\arraybackslash}p{3cm}} %centered "X" column
\\newcolumntype{L}[1]{>{\\raggedright\\arraybackslash}p{\\dimexpr#1-2\\tabcolsep-2\\arrayrulewidth+.21pt}}

\\usepackage[left=1cm,right=1.5cm]{geometry}

\\begin{document}\n""" + df_latex   + "\n\\end{document}"

        pyperclip.copy(df_latex)
        #self.notify(message="LaTeX code copied to clipboard. Have fun!", title="Have fun")
        self.statusBar().showMessage("LaTeX code copied to clipboard. Have fun!")


        # -------------
        if False: # DEPRICATED
            try:

                from pdflatex import PDFLaTeX
                path = os.path.dirname(os.path.abspath(__file__))
                my_file = os.path.join(path,"mymatrix")

                file = open(my_file, "w")
                file.write("""
        \\documentclass[a3paper,landscape]{article}
        \\usepackage{booktabs}
        \\usepackage{adjustbox}
        \\usepackage[table]{xcolor}
        \\usepackage{longtable}
        \\usepackage{tabularx,ragged2e}
        \\definecolor{Gray}{gray}{0.90}
        \\definecolor{LightGray}{gray}{0.95}
        \\definecolor{White}{rgb}{1,1,1}

        \\newcolumntype{g}{>{\\columncolor{White}\\arraybackslash}L} %
        \\newcolumntype{l}{>{\\columncolor{White}\\arraybackslash}p{3cm}} %centered "X" column
        \\newcolumntype{L}[1]{>{\\raggedright\\arraybackslash}p{\\dimexpr#1-2\\tabcolsep-2\\arrayrulewidth+.21pt}}

        \\usepackage[left=1cm,right=1.5cm]{geometry}

        \\begin{document}""")
                file.write(df_latex)
                file.write("""
        \\end{document}""")
                file.close()
                # pdfl = PDFLaTeX.from_texfile('my_texfile.tex')
                # pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
                # os.popen("pdflatex %s" % (os.getcwd()+"/my_texfile.tex"))
                import subprocess
                path = os.path.dirname(os.path.abspath(__file__))
                subprocess.run("pdflatex %s" % (os.path.join(path,"mymatrix.tex"))).check_returncode()

                #os.startfile(os.getcwd() + "\\mymatrix.pdf")
                try:
                    # shutil.rmtree(os.getcwd()+"\\files")
                    # os.mkdir(os.getcwd()+"\\files")

                    path = os.path.dirname(os.path.abspath(__file__))
                    shutil.move(path+"\\mymatrix.tex" , path+ "\\files\\mymatrix.tex")
                    shutil.move(path + "\\mymatrix.log", path + "\\files\\mymatrix.log")
                    shutil.move(path + "\\mymatrix.aux", path + "\\files\\\mymatrix.aux")
                    shutil.move(path + "\\mymatrix.pdf", path + "\\files\\mymatrix.pdf")
                    #shutil.copy(os.getcwd() + "\\files\\mymatrix.html",os.getcwd() + "\\files\\mymatrix.html")
                    #shutil.copy(os.getcwd() + "\\files\\mystyle.css", os.getcwd() + "\\files\\mystyle.css")
                except Exception as e:
                    self.notify(message=str(e),title="An Error occurred...(ID 1308)")

            except Exception as e:
                self.notify(message=str(e),title="An Error occurred...(ID 1311)")
            # -------------

            pd.options.display.max_colwidth = 2

            df_display = df_backup.applymap(abbreviate_zeros).to_string(line_width=None).replace("\_", "_")

            # self.parent.parentApp.getForm("AGGR_FLOW").data_box.values = df_display.split("\n")
            # self.parent.parentApp.switchForm("AGGR_FLOW")


    def gen_code(self,show_notification=False):

        code = ""
        code += "from sfctools import FlowMatrix \nimport numpy as np\n"
        code += "from sfctools import BalanceEntry,Accounts\n"
        code += "from sfctools import CashFlowEntry\n"
        code += "from sfctools import ICSEntry\n"
        code += "CA = Accounts.CA\nKA = Accounts.KA\n\n"

        subjects_count = defaultdict(lambda: 0.0)

        for filedata in self.entry_data:
            agent1 = filedata["agent1"]
            agent2 = filedata["agent2"]

            if agent1 == agent2:
                agent2 = "other_" + agent2

            a1 = filedata["a1"]  # + "\n"
            e1 = filedata["e1"]  # + "\n"
            l1 = filedata["l1"]  # + "\n"
            a2 = filedata["a2"]  # + "\n"
            e2 = filedata["e2"]  # + "\n"
            l2 = filedata["l2"]  # + "\n"

            flow_check = True
            print("FLOW CHECK", filedata["shortname"],filedata["log transaction"])
            if isinstance(filedata["log transaction"],str) and filedata["log transaction"].strip() == "True":
                # bool(filedata["log transaction"])
                flow_check = True
                print(flow_check)
            elif isinstance(filedata["log transaction"],str) and filedata["log transaction"].strip() == "False":
                # bool(filedata["log transaction"])
                flow_check = False
                print(flow_check)
            else:
                flow_check = filedata["log transaction"]
                print(flow_check)
            #print("FLOW CHECK", filename, flow_check)
            print("type", type(flow_check))

            kind = filedata["kind"]

            #subject =  filedata["subject"].replace(" ","_") + "_" + filedata["shortname".replace(" ","_")].lower()
            subject =  filedata["shortname".replace(" ","_")].replace("(","_").replace(")","").lower()
            subject_str =  filedata["subject".replace(" ","_")].lower().capitalize().replace("_", " ")

            subjects_count[subject] += 1
            if subjects_count[subject] > 1: # suffix for same names
                subject += "_%i" % int(subjects_count[subject])


            try:
                quantity = filedata["quantity"]
            except:
                quantity = "q"

            commands = []

            if "uni-directional" in filedata:
                unidir = filedata["uni-directional"]

                commands.append("cond = (isinstance(%s,float) or isinstance(%s,int))" % (quantity, quantity))
                commands.append("if cond: assert not np.isnan(%s)" % quantity)
                # ^ will also pass for np.float64
                commands.append("if cond: assert %s < +np.inf" % (quantity))
                commands.append("if cond: assert %s > -np.inf" % (quantity))

                #print("uni-directional",unidir)
                if str(unidir) == "True": # do not do bool(unidir)
                    #namaaa = filedata["shortname"]
                    #self.notify( (namaaa+ str(unidir)+ "="+(str(bool(unidir)))),title="check")
                    commands.append("if cond: assert %s >= 0, 'have to pass positive quantity: unidirectional transaction'" % quantity)

            commands = commands + ["%s.balance_sheet.disengage()" % agent1]
            if True: # agent1 != agent2:
                commands+= ["%s.balance_sheet.disengage()" % agent2]

            crossrefs = []
            def add_crossref(agent, sign, item, item2, silent, ref_agent, direction, other):
                be_dict = {"E":"BalanceEntry.EQUITY" , "A": "BalanceEntry.ASSETS", "L": "BalanceEntry.LIABILITIES"}
                
                # self.notify("crossref %s %s %s %s %s %s %s %s" % (agent, sign, item, item2, silent, ref_agent, direction, other),title="test")
                if direction == 0: # log for this agent 
                    be = be_dict[item2]
                    # item, agent, ref_agent, q, be = cr
                    crossrefs.append((item,agent,ref_agent,sign + quantity,be, direction))
                
                elif direction == 1: # log for other agent 
                    if other in be_dict:
                        be = be_dict[other]
                    else:
                        raise TypeError("Could not identify entry %s, should be A, L or E" % other)
                        
                    # item, agent, ref_agent, q, be = cr
                    crossrefs.append((item,ref_agent,agent,sign + quantity,be, direction))
                
                elif direction == 2: # log both 
                    #self.notify("direction 2", title="2")
                    
                    be = be_dict[item2]
                    crossrefs.append((item,agent,ref_agent,sign + quantity,be, direction))
                    #self.notify(str((item,agent,ref_agent,sign + quantity,be)), title="2")
                    
                    if other in be_dict:
                        be = be_dict[other]
                    else:
                        raise TypeError("Could not identify entry %s, should be A, L or E" % other)
                    crossrefs.append((item,ref_agent,agent,sign + quantity,be, direction))
                    #self.notify(str((item,ref_agent,agent,sign + quantity,be)), title="2")
                    
                else:
                    raise TypeError("Cannot interpret direction %s" % direction)

            ref_agents = []
            ref_items = []

            for entry in e1.split("\n"):
                if entry != "" and entry != "\n":
                    sign, item, silent, ref_agent, direction, other = self.entry_to_vals(entry, agent1, "Equity")
                    if sign is not None:
                        commands.append("%s.balance_sheet.change_item('%s', %s, %s, suppress_stock=%s)" % (
                        agent1, item, "BalanceEntry.EQUITY", sign + quantity, silent))
                        ref_items.append(item)
                    if ref_agent is not None:
                        add_crossref(agent1, sign, item, "E", silent, ref_agent, direction, other)
                        ref_agents.append(ref_agent)
                    
            for entry in a1.split("\n"):
                if entry != "" and entry != "\n":
                    sign, item, silent, ref_agent, direction, other  = self.entry_to_vals(entry, agent1, "Assets")
                    if sign is not None:
                        commands.append("%s.balance_sheet.change_item('%s', %s, %s, suppress_stock=%s)" % (
                        agent1, item, "BalanceEntry.ASSETS", sign + quantity, silent))
                        ref_items.append(item)
                    if ref_agent is not None:
                        add_crossref(agent1, sign, item, "A", silent, ref_agent, direction, other)
                        ref_agents.append(ref_agent)
                    
            for entry in l1.split("\n"):
                if entry != "" and entry != "\n":
                    sign, item, silent, ref_agent, direction, other = self.entry_to_vals(entry, agent1, "Liabilities")
                    if sign is not None:
                        commands.append("%s.balance_sheet.change_item('%s', %s, %s, suppress_stock=%s)" % (
                        agent1, item, "BalanceEntry.LIABILITIES", sign + quantity, silent))
                        ref_items.append(item)
                    if ref_agent is not None:
                        add_crossref(agent1, sign, item, "L", silent, ref_agent, direction, other)
                        ref_agents.append(ref_agent)
                    
            for entry in e2.split("\n"):
                if entry != "" and entry != "\n":
                    sign, item, silent, ref_agent,direction, other  = self.entry_to_vals(entry, agent2, "Equity")
                    if sign is not None:
                        commands.append("%s.balance_sheet.change_item('%s', %s, %s, suppress_stock=%s)" % (
                        agent2, item, "BalanceEntry.EQUITY", sign + quantity, silent))
                        ref_items.append(item)
                    if ref_agent is not None:
                        add_crossref(agent2, sign, item, "E", silent, ref_agent, direction, other)
                        ref_agents.append(ref_agent)
            
            for entry in a2.split("\n"):
                if entry != "" and entry != "\n":
                    sign, item, silent, ref_agent, direction, other  = self.entry_to_vals(entry, agent2, "Assets")
                    if sign is not None:
                        commands.append("%s.balance_sheet.change_item('%s', %s, %s, suppress_stock=%s)" % (
                        agent2, item, "BalanceEntry.ASSETS", sign + quantity, silent))
                        ref_items.append(item)
                    if ref_agent is not None:
                        add_crossref(agent2, sign, item, "A", silent, ref_agent, direction, other)
                        ref_agents.append(ref_agent)
                    
            for entry in l2.split("\n"):
                if entry != "" and entry != "\n":
                    sign, item, silent, ref_agent, direction, other = self.entry_to_vals(entry, agent2, "Liabilities")
                    if sign is not None:
                        commands.append("%s.balance_sheet.change_item('%s', %s, %s, suppress_stock=%s)" % (
                        agent2, item, "BalanceEntry.LIABILITIES", sign + quantity, silent))
                        ref_items.append(item)
                    if ref_agent is not None:
                        add_crossref(agent2, sign, item, "L", silent, ref_agent, direction, other)
                        ref_agents.append(ref_agent)


            commands.append("%s.balance_sheet.engage()" % agent1)
            if True: # agent1!=agent2:
                commands.append("%s.balance_sheet.engage()" % agent2)

            add_flow = flow_check
            if add_flow:
                print(subject_str,"flow check",flow_check)

                kind_enum = "(%s,%s)" % (kind.split("->")[0].strip(),kind.split("->")[1].strip())

                commands.append("FlowMatrix().log_flow(%s, %s, %s, %s, subject='%s')" % (kind_enum, quantity, agent1, agent2, subject_str))

            # cross references 
            # self.notify("\n".join([str(ik) for ik in crossrefs]),title="ok")

            for cr in crossrefs:
                item, agent, ref_agent, q, be, direction = cr
                commands.append("%s.balance_sheet.add_changelog(%s, '%s', %s, %s)" % (agent,ref_agent, item, be, q))


            # income statment
            my_income_dict = { # #translates string into ICSEntry (for better efficiency)
                "Revenue": "ICSEntry.REVENUES",
                "Non-Op. Income": "ICSEntry.NOI",
                "Expense": "ICSEntry.EXPENSES",
                "Tax": "ICSEntry.TAXES",
                "Interest": "ICSEntry.INTEREST",
                "Gain": "ICSEntry.GAINS",
                "Nontax.Profit": "ICSEntry.NONTAX_PROFITS",
                "Nontax. Profit": "ICSEntry.NONTAX_PROFITS", # quick and dirty bugfix
                "Nontax. Loss":  "ICSEntry.NONTAX_LOSSES",
                "Loss":  "ICSEntry.LOSSES"
            }

            # income statement entries
            loss_entries = ["ICSEntry.EXPENSES", "ICSEntry.LOSSES", "ICSEntry.NONTAX_LOSSES"]
            
            if "income1" in filedata:
                if str(filedata["income1"]) != 'None':
                    if my_income_dict[filedata["income1"]] in loss_entries:
                        commands.append("%s.income_statement.new_entry(%s,'%s',%s)" % (agent1,my_income_dict[filedata["income1"]],subject,quantity))
                    else:
                        commands.append("%s.income_statement.new_entry(%s,'%s',-%s)" % (agent1,my_income_dict[filedata["income1"]],subject,quantity))

            if "income2" in filedata:
                if str(filedata["income2"]) != 'None':
                    if my_income_dict[filedata["income2"]] == "ICSEntry.INTEREST" or my_income_dict[filedata["income2"]] == "ICSEntry.TAXES":
                        # received interest and taxes: flip sign for ICSEntry
                        commands.append("%s.income_statement.new_entry(%s,'%s',-%s)" % (agent2, my_income_dict[filedata["income2"]], subject, quantity))
                    else:
                        commands.append("%s.income_statement.new_entry(%s,'%s',%s)" % (agent2, my_income_dict[filedata["income2"]], subject, quantity))

            # cash flow statement
            if "cashflow1" in filedata:
                if str(filedata["cashflow1"]) != 'None':
                    commands.append("%s.cash_flow_statement.new_entry(%s,'%s',-%s)" % (agent1,"CashFlowEntry." + filedata["cashflow1"].upper(),subject,quantity))

            if "cashflow2" in filedata:
                if str(filedata["cashflow2"]) != 'None':
                    commands.append("%s.cash_flow_statement.new_entry(%s,'%s',%s)" % (agent2,"CashFlowEntry." + filedata["cashflow2"].upper(),subject,quantity))
            
            # print("----")
            # print("ref agents", ref_agents)
            # print("agent1, agent2", agent1, agent2)

            ref_agents = list(set(ref_agents)) 
            
            str_refa = ""
            if agent1 in ref_agents:
                ref_agents.remove(agent1)
                # print("found", agent1)
            if agent2 in ref_agents:
                ref_agents.remove(agent2)
                # print("found", agent2)
            
            ref_agents = list(set(ref_agents)) # remove double entries
            # print("---> ", ref_agents)
            # print("----\n\n")

            if len(ref_agents) > 0:
                str_refa = "," + ",".join(ref_agents)

            if "add_args" in filedata:
                add_args = filedata["add_args"].strip()
                if add_args != "":
                    str_refa += "," + add_args
            
            # check consistency
            # ref_items.append(item)
            done = []
            changelog_checks =  ""
            for item in ref_items:
                for agent in ref_agents:
                    if (agent,item) not in done:
                        done.append((agent,item))
                        changelog_checks += "    %s.balance_sheet.check_consistency_changelog('%s')\n" % (agent, item) 
                    if (agent1,item) not in done:
                        done.append((agent1,item))
                        changelog_checks += "    %s.balance_sheet.check_consistency_changelog('%s')\n" % (agent1, item) 
                    if (agent2,item) not in done:
                        done.append((agent2,item))
                        changelog_checks += "    %s.balance_sheet.check_consistency_changelog('%s')\n" % (agent2, item) 
            
            method = "def %s(%s, %s, %s %s):\n" % (subject, agent1, agent2, quantity, str_refa)
            
            method += "\n"  # + changelog_checks

            if "description" in filedata: # add the description in the docstring of the function definition
                method += "    #" + filedata["description"] + "\n"

            for command in commands:
                method += "    " + command + "\n"

            # additional code 
            if "add_code" in filedata:
                add_code = filedata["add_code"].split("\n")
            
                for command in add_code:
                    method +=  "    " + command + "\n"               

            method += changelog_checks
            method += "\n\n"
            
            code += method

        folder = os.path.dirname(self.current_file) # statusBar().currentMessage())
        fname =  folder + "/python_code/transactions.py"

        with open(fname,"w",encoding="utf-8") as file:
            file.write(code)

        if show_notification:
            self.notify(message="Code exported to %s" % (fname),title="Success")


    def gen_ics_single(self):
        if self.drawcanvas.highlighted is None:
            self.notify(title="No agent selected", message="No agent selected. Please select one first.")
            return
        if self.drawcanvas.highlighted.ishelper:
            self.notify(title="No agent selected", message="No valid box selected. Please select an agent.")
            return
        my_agent = self.drawcanvas.highlighted.name

        combined_income =  {"Subject":[],"Short Name": [],"Quantity":[], "Type":[], "Ranking":[]} # ranking will be removed later
        """
        "Gains": [], "Losses": [], "Revenues": [], "Taxes": [], "Expenses": [],
         "Nontaxable Losses": [], "Nontaxable Profits": [],
                               "Non-Operational Income": [],
                                               "Interest Payments": []
                                               }
        """
        k = 0
        try:
            for filedata in self.entry_data:
                agent1 = filedata["agent1"].strip()
                agent2 = filedata["agent2"].strip()

                print("agent1",agent1,"agent2",agent2)
                if agent1 == my_agent:
                    ref_agent = "agent1"
                    ref_income = "income1"

                elif agent2 == my_agent:
                    ref_agent = "agent2"
                    ref_income = "income2"
                else:
                    pass

                #assets1 = filedata["a1"] + "\n"
                #liabs1 = filedata["l1"] + "\n" + filedata["e1"] + "\n"

                #assets2 = filedata["a2"] + "\n"
                #liabs2 = filedata["l2"] + "\n" + filedata["e2"] + "\n"

                if (agent1 == my_agent or agent2 == my_agent) and str(filedata[ref_income]) != 'None':
                    mydict = {"Gain": "Gains",
                              "Loss": "Losses",
                              "Expense": "Expenses",
                              "Revenue": "Revenues",
                              "Tax": "Taxes",
                              "Nontax. Profit": "Nontaxable Profits",
                              "Nontax. Loss": "Nontaxable Losses",
                              "Non-Op. Income": "Non-Operational Income",
                              "Interest": "Interest Payments"}

                    try:
                        if agent1 == my_agent:
                            sign = "-"
                        if agent2 == my_agent:
                            sign = "+"

                        q = sympy.latex(sympy.simplify(sign + filedata["quantity"]), mode="plain")
                        subject = filedata["subject"].replace("_", " ").capitalize()
                        print("      found",q,subject)
                        tpe = mydict[filedata[ref_income]]
                        combined_income["Type"].append(tpe)
                        combined_income["Subject"].append(subject)
                        combined_income["Quantity"].append(str(q))
                        combined_income["Short Name"].append(filedata["shortname"].strip())

                        if tpe in ["Gains","Losses","Expenses","Revenues"]:
                            combined_income["Ranking"].append(0)
                        elif tpe in ["Non-Operational Income","Interest Payments"]:
                            combined_income["Ranking"].append(1)
                        elif tpe in ["Taxes"]:
                            combined_income["Ranking"].append(2)
                        elif tpe in ["Nontaxable Profits", "Nontaxable Losses"]:
                            combined_income["Ranking"].append(3)
                        else:
                            combined_income["Ranking"].append(4)


                    except Exception as e:
                        self.notify(
                            "Cannot handle the symbolic expression %s" % sign + filedata["quantity"],title="Error")

        except:
            self.notify(title="Error", message="An error occurred.")

        try:
            result = pd.DataFrame(combined_income).set_index("Subject")


            # sort after ranking
            result = result.sort_values('Ranking')

            # remove ranking
            result = result.drop(columns= "Ranking")

            model = PandasModel(result)

            if my_agent not in IncomeViewer.instances:
                myview = IncomeViewer(self,name=my_agent)
            else:
                myview = IncomeViewer.instances[my_agent]
            # mview.setGeometry(100,500)
            myview.set_model(model)
            # mview.webView.setHtml(df_html)

            if not self.test_mode:
                myview.show()

        except Exception as e:
            self.notify(title="Error", message="An error occurred." + str(e))


    def gen_cashflow_single(self):
        if self.drawcanvas.highlighted is None:
            self.notify(title="No agent selected", message="No agent selected. Please select one first.")
            return
        if self.drawcanvas.highlighted.ishelper:
            self.notify(title="No agent selected", message="No valid box selected. Please select an agent.")
            return
        my_agent = self.drawcanvas.highlighted.name

        combined_income =  {"Subject":[],"Short Name": [],"Quantity":[], "Type":[], "Ranking":[]} # ranking will be removed later
        """
        """
        k = 0
        try:
            for filedata in self.entry_data:
                agent1 = filedata["agent1"].strip()
                agent2 = filedata["agent2"].strip()

                print("agent1",agent1,"agent2",agent2)
                if agent1 == my_agent:
                    ref_agent = "agent1"
                    ref_income = "cashflow1"

                elif agent2 == my_agent:
                    ref_agent = "agent2"
                    ref_income = "cashflow2"
                else:
                    pass

                #assets1 = filedata["a1"] + "\n"
                #liabs1 = filedata["l1"] + "\n" + filedata["e1"] + "\n"

                #assets2 = filedata["a2"] + "\n"
                #liabs2 = filedata["l2"] + "\n" + filedata["e2"] + "\n"

                if (agent1 == my_agent or agent2 == my_agent) and str(filedata[ref_income]) != 'None':
                    mydict = {"Gain": "Gains",
                              "Loss": "Losses",
                              "Expense": "Expenses",
                              "Revenue": "Revenues",
                              "Tax": "Taxes",
                              "Nontax. Profit": "Nontaxable Profits",
                              "Nontax. Loss": "Nontaxable Losses",
                              "Non-Op. Income": "Non-Operational Income",
                              "Interest": "Interest Payments"}

                    try:
                        if agent1 == my_agent:
                            sign = "-"
                        if agent2 == my_agent:
                            sign = "+"

                        q = sympy.latex(sympy.simplify(sign + filedata["quantity"]), mode="plain")
                        subject = filedata["subject"].replace("_", " ").capitalize()
                        print("      found",q,subject)
                        tpe = filedata[ref_income]
                        combined_income["Type"].append(tpe)
                        combined_income["Subject"].append(subject)
                        combined_income["Quantity"].append(str(q))
                        combined_income["Short Name"].append(filedata["shortname"].strip())
                        combined_income["Ranking"].append(0)
                        """
                        if tpe in ["Gains","Losses","Expenses","Revenues"]:
                            combined_income["Ranking"].append(0)
                        elif tpe in ["Non-Operational Income","Interest Payments"]:
                            combined_income["Ranking"].append(1)
                        elif tpe in ["Taxes"]:
                            combined_income["Ranking"].append(2)
                        elif tpe in ["Nontaxable Profits", "Nontaxable Losses"]:
                            combined_income["Ranking"].append(3)
                        else:
                            combined_income["Ranking"].append(4)
                        """

                    except Exception as e:
                        self.notify(
                            "Cannot handle the symbolic expression %s" % sign + filedata["quantity"] + str(e),title="Error")

        except:
            self.notify(title="Error", message="An error occurred.")

        try:
            result = pd.DataFrame(combined_income).set_index("Subject")


            # sort after ranking
            result = result.sort_values('Ranking')

            # remove ranking
            result = result.drop(columns= "Ranking")

            model = PandasModel(result)

            if my_agent not in CashFlowViewer.instances:
                myview = CashFlowViewer(self,name=my_agent)
            else:
                myview = CashFlowViewer.instances[my_agent]
            # mview.setGeometry(100,500)
            myview.set_model(model)
            # mview.webView.setHtml(df_html)
            if not self.test_mode:
                myview.show()

        except Exception as e:
            self.notify(title="Error", message="An error occurred." + str(e))


    def gen_tex_ics(self):
        combined_sheets = {}

        """
        {
        agent_name: {
                    "Assets": {
                                asset_name : [entries],
                                ...},

                    "Liabilities and Equity": {
                                name : [entries],
                                ...},

                    }
        }
        """

        combined_income = defaultdict(lambda: {"Gains": [], "Losses": [], "Revenues": [], "Taxes": [], "Expenses": [],
                                               "Nontaxable Losses": [], "Nontaxable Profits": [],
                                               "Non-Operational Income": [],
                                               "Interest Payments": []
                                               })

        """
        {
        agent_name: {
                "Gains":  [entries],
                "Losses":[entries],
                "Expenditures":[entries],
                "Revenues": [entries],
                "Taxes":[entries]
        }
        """

        k = 0
        texstr = ""

        try:
            for filedata in self.entry_data:
                            #   self.parent.agent1.value = filedata["agent1"]
                            # self.parent.agent2.value = filedata["agent2"]

                            # self.parent.flow_check.value = str(bool(filedata["log transaction"]))
                            # self.parent.kind.value = filedata["kind"]
                            # self.parent.subject.value = filedata["subject"]
                            # self.parent.quantity.value = filedata["quantity"]

                            agent1 = filedata["agent1"]
                            agent2 = filedata["agent2"]

                            assets1 = filedata["a1"] + "\n"
                            liabs1 = filedata["l1"] + "\n" + filedata["e1"] + "\n"

                            assets2 = filedata["a2"] + "\n"
                            liabs2 = filedata["l2"] + "\n" + filedata["e2"] + "\n"

                            my_table = pd.DataFrame.from_dict(
                                {"Assets": assets1.split("\n"), "Liabilities and Equity": liabs1.split("\n")},
                                orient='index').T
                            my_table2 = pd.DataFrame.from_dict(
                                {"Assets": assets2.split("\n"), "Liabilities and Equity": liabs2.split("\n")},
                                orient='index').T

                            tex_table1 = my_table.to_latex(index_names=False, index=False)
                            tex_table2 = my_table2.to_latex(index_names=False, index=False)

                            # merge_table = pd.concat(tex_table1,tex_table2)

                            # ============================ modify combined sheet

                            #
                            # AGENT 1
                            #

                            if agent1 not in combined_sheets:
                                combined_sheets[agent1] = {}

                            if "Assets" not in combined_sheets[agent1]:
                                combined_sheets[agent1]["Assets"] = {}
                            if "Liabilities and Equity" not in combined_sheets[agent1]:
                                combined_sheets[agent1]["Liabilities and Equity"] = {}

                            for change in assets1.split("\n"):
                                try:
                                    sign = change[0]  # first letter is sign + or -

                                    name = change[1:].strip()
                                    q = sympy.latex(sympy.simplify(sign + filedata["quantity"]), mode="inline")
                                    subject = "   (" + filedata["subject"].replace("_", " ") + ")"

                                    #print("name", name)
                                    #print("combined_sheets[agent1]", combined_sheets[agent1])
                                    if name not in combined_sheets[agent1]["Assets"]:
                                        combined_sheets[agent1]["Assets"][name] = ""

                                    combined_sheets[agent1]["Assets"][name] += q + subject + "\n"
                                except:
                                    pass
                            for change in liabs1.split("\n"):
                                try:
                                    sign = change[0]  # first letter is sign + or -

                                    name = change[1:].strip()
                                    try:
                                        q = sympy.latex(sympy.simplify(sign + filedata["quantity"]), mode="inline")
                                    except Exception as e:
                                        self.notify(
                                            "Cannot handle the symbolic expression %s" % sign + filedata[
                                                "quantity"],title="Error")

                                    subject = "   (" + filedata["subject"].replace("_", " ") + ")"

                                    if name not in combined_sheets[agent1]["Liabilities and Equity"]:
                                        combined_sheets[agent1]["Liabilities and Equity"][name] = ""

                                    combined_sheets[agent1]["Liabilities and Equity"][name] += q + subject + "\n"
                                except:
                                    pass

                            if str(filedata["income1"]) != 'None':
                                mydict = {"Gain": "Gains",
                                          "Loss": "Losses",
                                          "Expense": "Expenses",
                                          "Revenue": "Revenues",
                                          "Tax": "Taxes",
                                          "Nontax. Profit": "Nontaxable Profits",
                                          "Nontax. Loss": "Nontaxable Losses",
                                          "Non-Op. Income": "Non-Operational Income",
                                          "Interest": "Interest Payments"}

                                try:
                                    q = sympy.latex(sympy.simplify(sign + filedata["quantity"]), mode="inline")
                                    subject = "   (" + filedata["subject"].replace("_", " ") + ")"
                                    combined_income[agent1][mydict[filedata["income1"]]].append((str(q), subject))

                                except Exception as e:
                                    self.notify(
                                        "Cannot handle the symbolic expression %s" % sign + filedata["quantity"],title="Error")


                            #
                            # AGENT 2
                            #

                            if agent2 not in combined_sheets:
                                combined_sheets[agent2] = {}

                            if "Assets" not in combined_sheets[agent2]:
                                combined_sheets[agent2]["Assets"] = {}
                            if "Liabilities and Equity" not in combined_sheets[agent2]:
                                combined_sheets[agent2]["Liabilities and Equity"] = {}

                            for change in assets2.split("\n"):

                                try:
                                    sign = change[0]  # first letter is sign + or -

                                    name = change[1:].strip()
                                    try:
                                        q = sympy.latex(sympy.simplify(sign + filedata["quantity"]), mode="inline")
                                    except Exception as e:
                                        self.notify(
                                            "Cannot handle the symbolic expression %s" % sign + filedata[
                                                "quantity"],title="Error")

                                    subject = "   (" + filedata["subject"].replace("_", " ") + ")"

                                    if name not in combined_sheets[agent2]["Assets"]:
                                        combined_sheets[agent2]["Assets"][name] = ""

                                    combined_sheets[agent2]["Assets"][name] += q + subject + "\n"
                                except:
                                    pass

                            for change in liabs2.split("\n"):
                                try:
                                    sign = change[0]  # first letter is sign + or -

                                    name = change[1:].strip()
                                    try:
                                        q = sympy.latex(sympy.simplify(sign + filedata["quantity"]), mode="inline")
                                    except Exception as e:
                                        self.notify(
                                            "Cannot handle the symbolic expression %s" % sign + filedata[
                                                "quantity"],title="Error")

                                    subject = "   (" + filedata["subject"].replace("_", " ") + ")"

                                    if name not in combined_sheets[agent2]["Liabilities and Equity"]:
                                        combined_sheets[agent2]["Liabilities and Equity"][name] = ""

                                    combined_sheets[agent2]["Liabilities and Equity"][name] += q + subject + "\n"
                                except:
                                    pass

                            if str(filedata["income2"]) != 'None':
                                mydict = {"Gain": "Gains",
                                          "Loss": "Losses",
                                          "Expense": "Expenses",
                                          "Revenue": "Revenues",
                                          "Tax": "Taxes",
                                          "Nontax. Profit": "Nontaxable Profits",
                                          "Nontax. Loss": "Nontaxable Losses",
                                          "Non-Op. Income": "Non-Operational Income",
                                          "Interest": "Interest Payments"}
                                q = sympy.latex(sympy.simplify(sign + filedata["quantity"]), mode="inline")
                                subject = "   (" + filedata["subject"].replace("_", " ") + ")"
                                combined_income[agent2][mydict[filedata["income2"]]].append((str(q), subject))

                                # ============================

                            transfer_str = ""

                            if convert_bool(filedata["log transaction"]):
                                transfer_str = "\nFlow:~" + filedata["kind"].strip().replace("->",
                                                                                             "$\\rightarrow$") + "&~\\\\" + "\n"
                                transfer_str += "Subject:~" + filedata["subject"].strip().title() + "&~\\\\" + "\n"
                                # transfer_str += "Quantity:~" + filedata["quantity"].strip() + "&~\\\\"+ "\n"

                            table_str = """\\begin{tabular}{ll}

                %s & %s \\\\
                ~ & ~ \\\\
                """ % (filedata["agent1"], filedata["agent2"])
                            table_str += tex_table1 + "&" + tex_table2 + "\\\\\\\\" + transfer_str

                            table_str += "\n\n\\end{tabular}"
                            texstr += """\\begin{table}[H]\n"""
                            texstr += table_str
                            texstr += """\caption{%s}\n\end{table}""" % (filedata["subject"] + "(%s)"%filedata["shortname"])

            texstr = texstr.replace("_", " ")
            texstr = texstr.replace("None", "")

            # ============ add combined sheets ======================
            print(combined_sheets)

            # pd.DataFrame(combined_sheets).to_excel("test.xlsx") <- for manual testing

            # convert the combined sheets to tex
            texstr_combined = ""
            for agent, data in combined_sheets.items():
                agent_titled = agent.replace("_", " ").title()

                assets = data["Assets"]
                liabs = data["Liabilities and Equity"]

                mys = """
            \\begin{table}[H]
            \\centering
            """
                mys += """
            \\begin{tabular}{|l|l|}
            \hline
            ~&~\\\\
            \\textbf{Assets} & \\textbf{Liabilities and Equity}\\\\
            ~&~\\\\

                        """

                mys += """
            \\begin{tabular}{ll}
                        """

                for item, entry in assets.items():

                    mys += item + "&~ \\\\\hline~&~\\\\\n"

                    for sub_entry in entry.split("\n"):
                        try:
                            lt_subentry = sub_entry
                            mys += "~&" + lt_subentry + "\\\\" + "\n"
                        except:
                            pass

                mys += """
            \end{tabular} & \\begin{tabular}{ll}""" + "\n"

                for item, entry in liabs.items():
                    if item != "Equity":
                        mys += item + "&~ \\\\\hline~&~\\\\\n"

                        for sub_entry in entry.split("\n"):
                            try:
                                lt_subentry = sub_entry
                                mys += "~&" + lt_subentry + "\\\\" + "\n"
                            except:
                                pass

                try:
                    item = "Equity"
                    entry = liabs["Equity"]
                    mys += item + "&~ \\\\\hline~&~\\\\\n"

                    for sub_entry in entry.split("\n"):
                        try:
                            lt_subentry = sub_entry
                            mys += "~&" + lt_subentry + "\\\\" + "\n"
                        except:
                            pass
                except:
                    pass

                mys += """
            \\end{tabular}
            \\\\~&~
            \\\\\hline"""
                mys += """
            \\end{tabular}"""
                mys += """
            \\caption{Balance Sheet of %s}""" % agent_titled + """
            \\end{table}
            """
                texstr_combined += mys

                # =========== add income

                if agent in combined_income:
                    income_data = combined_income[agent]
                    income_str = """
            \\begin{table}[H]\n\centering\n
            \\begin{tabular}{|ll|}\n\hline"""

                    for k in "Revenues", "Gains", "Expenses", "Losses", \
                             "Interest Payments", "Non-Operational Income", "Taxes", "Nontaxable Profits", "Nontaxable Losses":
                        v = income_data[k]

                        income_str += "~&~\\\\"
                        income_str += "\t" + k + "&~\\\\\n"

                        for sub_value in v:
                            income_str += "\t" + "~&" + sub_value[0] + sub_value[1] + "\\\\\n"
                        if len(v) == 0:
                            income_str += "\t" + "~&" + ".-" + "\\\\\n"

                        if k != "Nontaxable Losses":
                            income_str += "~&~\\\\\hline\n"

                    income_str += """\n
            ~&~\\\\\hline\n\\end{tabular}"""
                    income_str += """\n
            \\caption{Income Statement of %s}""" % agent_titled + """
            \\end{table}"""

                    texstr_combined += income_str

            # =======================================================
            pyperclip.copy(texstr_combined)
            self.notify(message="LaTeX code copied to clipboard. Have fun!", title="Have fun")

            if False: # depreciated

                path = os.path.dirname(os.path.abspath(__file__))
                with open(os.path.join(path , "files/income_statments.tex"), "w") as file:
                    file.write("""
    \documentclass{article}
    \\usepackage{tabularx}
    \\usepackage{amsmath}
    \\usepackage{float}

    \\begin{document}

    """)
                    file.write(texstr_combined)
                    file.write("""
    \\end{document}
    """)

                import subprocess
                try:

                    path = os.path.dirname(os.path.abspath(__file__))
                    subprocess.run("pdflatex %s" % (os.path.join(path, "files/income_statments.tex"))).check_returncode()

                    shutil.move(path + "income_statments.tex", path + "files\\income_statments.tex")
                    shutil.move(path + "income_statments.log", path + "files\\income_statments.log")
                    shutil.move(path + "income_statments.aux", path + "files\\\mincome_statments.aux")
                    shutil.move(path + "income_statments.pdf", path + "files\\income_statments.pdf")
                    self.notify(message="TeX File created in %s" % path + "\\files" ,title="Success")

                except Exception as e:
                    self.notify(message=str(e.__context__) + "\n" + str(e), title=e.__class__.__name__)


        except Exception as e:
            self.notify(message=str(e.__context__) + "\n" + str(e), title=e.__class__.__name__)

    def add_helper(self):
        new_name = self.HelperNameEdit.text()
        # TODO add security mechanism to avoid overwriting an agent
        if new_name == "":
            self.notify("Please enter a valid name", title="IBM Error")
        elif not new_name[0].isupper():
            self.notify("Please enter a valid name with\nuppercase first letter or camelcase, e.g. 'MyAgent'", title="IBM Error")
        else:
            self.drawcanvas.add_agent(new_name)

    def remove_helper(self):
        self.drawcanvas.remove_agent()

    def add_new(self):

        # TODO assert that quantity is not yet in any other transaction
        self.made_changes = False


        new_entry = {}

        new_entry["a1"] = self.AssetListLeft.toPlainText()
        new_entry["a2"] = self.AssetListRight.toPlainText()
        new_entry["l1"] = self.LiabilityListLeft.toPlainText()
        new_entry["l2"] = self.LiabilityListRight.toPlainText()
        new_entry["e1"] = self.EquityListLeft.toPlainText()
        new_entry["e2"] = self.EquityListRight.toPlainText()

        # new_entry["a1"] = self.AssetListLeft.toPlainText()
        # new_entry["l1"] = self.LiabilityListLeft.toPlainText()
        # new_entry["a2"] = self.LiabilityListRight.toPlainText()
        # new_entry["l2"] = self.AssetListRight.toPlainText()
        # new_entry["e1"] = self.EquityListLeft.toPlainText()
        # new_entry["e2"] = self.EquityListRight.toPlainText()

        new_entry["agent1"] = camel(self.agent1Edit.text()) #.capitalize()
        new_entry["agent2"] = camel(self.agent2Edit.text()) #.capitalize()

        self.agent1Edit.setText(camel(self.agent1Edit.text())) # .capitalize())
        self.agent2Edit.setText(camel(self.agent2Edit.text())) #.capitalize())

        if not self.drawcanvas.check_exist(new_entry["agent1"]):
            if new_entry["agent1"] != "":
                yes =  self.ask_question('',"The agent %s does not exist.\nDo you wish to continue and automatically create a new agent?"%new_entry["agent1"])
                if not yes:
                    return

        if not self.drawcanvas.check_exist(new_entry["agent2"]):
            if new_entry["agent2"] != "":
                yes =  self.ask_question('', "The agent %s does not exist.\nDo you wish to continue and automatically create a new agent?"%new_entry["agent2"])
                if not yes:
                    return


        box1 = self.drawcanvas.add_agent(new_entry["agent1"])
        box2 = self.drawcanvas.add_agent(new_entry["agent2"])

        my_items = []
        data = new_entry
        allentries = "\n".join([data["l1"], data["a1"], data["e1"], data["l2"], data["a2"], data["e2"]])
        for sub_item in allentries.split("\n"):
            for sub_entry in sub_item.split("\n"):
                entry = sub_entry.replace("-","").replace("+","").strip()
                if entry !=  "":
                    my_items.append(entry)

        self.drawcanvas.add_connection(box1, box2, name= str(self.editShortname.text()),subject=self.editSubject.text(),items=my_items)

        new_entry["uni-directional"] = \
            str(self.comboUnidir.currentText())

        new_entry["log transaction"] = \
            self.registerFlowBox.currentText()

        new_entry["cashflow1"] = \
            str(self.comboCashLeft.currentText())
        new_entry["cashflow2"] = \
            str(self.comboCashRight.currentText())

        new_entry["kind"] = \
            str(self.editType.currentText())

        new_entry["income1"] = \
            str(self.comboIncomeLeft.currentText())
        new_entry["income2"] = \
            str(self.comboIncomeRight.currentText())

        new_entry["quantity"] = \
            str(self.editQuantity.text())

        new_entry["subject"] = \
            str(self.editSubject.text())

        new_entry["shortname"] = \
            str(self.editShortname.text())

        new_entry["description"] = \
            str(self.editDescription.text())
        
        new_entry["add_args"] = \
            str(self.editAddArgs.text())

        new_entry["add_code"] = \
            str(self.editAddCode.toPlainText())

        self.entry_data.append(new_entry)
        self.update_table()



        darkMode = True
        try:
            if self.theme_manager.theme == "bright":
                darkMode = False
        except:
            pass

        try:
            self.selection_idx = len(self.entry_data)-1
            self.row_select(self.selection_idx)
        except Exception as e :
            self.notify("ERROR:" + tr(e),title="Error")

        """
        if self.selection_idx is not None:
            for i in range(self.transactionView.columnCount()):

                if darkMode:
                    self.transactionView.item(self.selection_idx, i).setBackground(QtGui.QColor(21, 21, 21))
                else:
                    self.transactionView.item(self.selection_idx, i).setBackground(QtGui.QColor(233, 234, 227))

            self.selection_idx = self.transactionView.rowCount()-1
            for i in range(self.transactionView.columnCount()):
                if darkMode:
                    self.transactionView.item(self.selection_idx, i).setBackground(QtGui.QColor(18, 18, 18))
                else:
                    self.transactionView.item(self.selection_idx, i).setBackground(QtGui.QColor(159, 159, 159))
        """




    def goto_next(self):
        pass


    def udpate_display(self):
        try:

            filename = self.filename

            with open(filename, 'r') as stream:
                filedata = yaml.safe_load(stream)
                print(filedata)

                self.agent1Label.text = filedata["agent1"]
                self.agent2Label.text = filedata["agent2"]

                # self.a1.value = filedata["a1"]  # + "\n"
                # self.e1.value = filedata["e1"]  # + "\n"
                # self.l1.value = filedata["l1"]  # + "\n"
                # self.a2.value = filedata["a2"]  # + "\n"
                # self.e2.value = filedata["e2"]  # + "\n"
                # self.l2.value = filedata["l2"]  # + "\n"

                # if "shortname" in filedata:
                #    self.parent.shortname.value = filedata["shortname"]

                # if "uni-directional" in filedata:
                #    self.parent.direction_check.value = bool(str(filedata["uni-directional"]))
                # else:
                #    self.parent.direction_check.value = False

                # if "description" in filedata:
                #    self.parent.description.value = filedata["description"]

                # self.parent.flow_check.value = filedata["log transaction"]
                # self.parent.kind.value = filedata["kind"]
                # self.parent.subject.value = filedata["subject"]
                # self.parent.quantity.value = filedata["quantity"]

                try:
                    # ["None","Revenue","Expense","Gain","Loss","Tax"]

                    my_dict = {
                        "None": 0,
                        "Revenue": 1,
                        "Expense": 2,
                        "Gain": 3,
                        "Loss": 4,
                        "Interest": 5,
                        "Non-Op. Income": 6,
                        "Tax": 7,
                        "Nontax. Profit": 8,
                        "Nontax. Loss": 9
                    }

                    # self.parent.income1.value = [my_dict[filedata["income1"]]]
                    # self.parent.income2.value = [my_dict[filedata["income2"]]]

                    # self.parent.cashflow1.value = [filedata["cashflow1"]]
                    # self.parent.cashflow2.value = [filedata["cashflow2"]]

                except:
                    pass

                #self.parent.display()

        except Exception as e:
            print(str(e)) # self.notify(str(e),"Exception") < this should not throw an exception



def run_app():
    # runs the main application window

    # create font 
    try:
        myFont = QFont("Cascadia Mono", 9)
    except:
        pass 

    app = QtWidgets.QApplication(sys.argv)
    try:
        QtWidgets.QApplication.instance().setFont(myFont)
    except:
        pass
    # pixmap = QPixmap("./splash.png")
    # splash = QSplashScreen(pixmap)
    # splash.show()

    # app.setStyle('Fusion')

    window = TransactionDesigner()
    try:
        window.setFont(myFont)
    except:
        pass 
    # splash.finish(window)

    # setup stylesheet
    # apply_stylesheet(app, theme='dark_teal.xml', invert_secondary=True)
    # apply_stylesheet(window, theme='dark_teal.xml', invert_secondary=True)

    window.show()
    window.switch_theme()
    window.switch_theme()

    app.exec_()





if __name__ == "__main__":

    run_app()
