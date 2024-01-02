from PyQt5 import QtWidgets, uic,QtGui
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog,QMessageBox,QTableWidgetItem,QAbstractItemView,QListWidgetItem
import sys
import os
import yaml
import shutil
import time
import datetime

# from pandasmodel import PandasModel
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QObject, pyqtSlot
import pickle as pkl
import re
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QFontDatabase, QColor, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence


class MainWatchDog(QObject):
    """
    This is a file watchdog. It frequently checks if external changes
    have been made to a file viewed in the code editor.
    """
    difference_detected = pyqtSignal()  # difference detected between current code and code stored in file

    def __init__(self,parent, file_ctrl):

        super().__init__()
        #self.file_name = os.path.join(file_name , agent_name + ".txt" ) # < source file sub_names

        self.parent_w = parent
        text = parent.textEdit.toPlainText()
        # self.finished = False
        self.file_ctrl = file_ctrl  # <-  set mutable type finished list

    def run(self):
        """Long-running task."""

        while True:

            time.sleep(1.0) # check every second

            if self.file_ctrl[0] is None:
                continue

            file_name = os.path.join(os.path.dirname(self.file_ctrl[0]) ,"python_code", "mainloop.py" ) # < source file sub_names

            # print("[Watchdog] check file", file_name)
            current_gui_text = self.parent_w.textEdit.toPlainText()
            current_file_text = None

            try:
                with open(file_name,"r") as file:
                    current_file_text = file.read()

                outdated = False
                file_time = os.path.getmtime(file_name)
                my_time = self.parent_w.mtime

                if MainLoopEditor.instance is None:
                    self.finished = True

                if file_time > my_time:
                    outdated = True

                if current_gui_text != current_file_text and outdated:
                    self.difference_detected.emit()

            except Exception as e:
                print(str(e))
                # pass



class Highlighter(QSyntaxHighlighter):
    def __init__(self,parent=None):
        super().__init__(parent)
        self._mapping = {}

    def add_mapping(self, pattern, pattern_format):
        self._mapping[pattern] = pattern_format

    def highlightBlock(self, text_block):
        for pattern, fmt in self._mapping.items():
            try:

                for match in re.finditer(pattern,text_block):
                    try:
                        start, end = match.span()
                        self.setFormat(start, end-start, fmt)
                    except:
                        pass

            except:
                pass

class MainLoopEditor(QtWidgets.QDialog):

    instance = None

    def __init__(self,parent,text=""):

        super(MainLoopEditor, self).__init__(parent) # Call the inherited classes __init__ method
        path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(path,'simulation_edit.ui'), self) # Load the .ui file

        self.setFixedSize(self.size());

        self.backup_count = 0

        self.textEdit.textChanged.connect(self.text_changed)
        self.textEdit.cursorPositionChanged.connect(self.update_line_label)

        self.textEdit.installEventFilter(self)

        self.highlighter = Highlighter()

        self.setUpEditor()

        self.shortcut = QShortcut(QKeySequence("Ctrl+S"),self)
        self.shortcut.activated.connect(self.parent().save_and_build)

        self.shortcut2 = QShortcut(QKeySequence("Ctrl+Tab"),self)
        self.shortcut2.activated.connect(self.indent)

        self.shortcut2 = QShortcut(QKeySequence("Shift+Tab"),self)
        self.shortcut2.activated.connect(self.unindent)

        self.set_text(text)
        self.searchEdit.textChanged.connect(self.update_search)

        self.parent_widget = parent
        theme_manager = self.parent_widget.theme_manager
        self.setStyleSheet(theme_manager.get_background_style())
        self.setStyleSheet(theme_manager.get_stylesheet("main"))

        project_file = self.parent_widget.current_file
        print("Project File", project_file)

        self.__class__.instance = self
        self.thread = QThread()

        filepath = None # os.path.dirname(os.path.abspath(self.parent_widget.current_file))
        # python_path = os.path.join(filepath , "python_code")
        self.mtime = 0.0 # time.time() # os.path.getmtime(filepath) # last changes of project file

        self.file_ctrl = [filepath]
        self.worker = MainWatchDog(self, self.file_ctrl)
        self.worker.moveToThread(self.thread)
        self.worker.difference_detected.connect(self.process_differences)
        self.thread.started.connect(self.worker.run)

        self.thread.start()

    def start_watchdog(self,fname):
        # start a new watchdog on the file
        self.file_ctrl[0] = fname


    def set_text(self,text):
        text = text.replace("    ","\t")
        self.textEdit.setPlainText(text)

    def closeEvent(self, event):
        self.__class__.instance = None
        self.hide()
        # event.accept() # let the window close

    def process_differences(self):
        # process differences between the sfctl file and the external file changes
        self.warn_differences()
        self.set_text_from_external()

    def warn_differences(self):
        # self.main_widget.notify("Difference Detected!\n%s" % self.agent_name,title="External changes detected.")
        self.parent_widget.statusBar().showMessage("External changes in mainloop.py detected! Overwriting mainloop.py")

    def set_text_from_external(self):
        """
        set the text from the external file changes. Overwrite internal text
        """

        filepath = os.path.dirname(os.path.abspath(self.parent_widget.current_file))
        python_path = os.path.join(filepath , "python_code")

        new_text = None
        with open(os.path.join(python_path , "mainloop.py"),"r") as file:
            new_text = file.read()

        if new_text is None:
            return

        scroll_pos = self.textEdit.verticalScrollBar().value()

        cursor = self.textEdit.textCursor()
        old_position= cursor.position()

        self.textEdit.setPlainText(new_text)

        cursor = self.textEdit.textCursor()
        cursor.setPosition(old_position)

        self.textEdit.setTextCursor(cursor)
        self.textEdit.verticalScrollBar().setValue(scroll_pos)


    def update_search(self):
        self.setUpEditor()
        self.update()

    def eventFilter(self, obj, event):
        self.update()
        if event.type() == QtCore.QEvent.KeyPress and obj is self.textEdit:

            try:
                self.mtime = time.time()
            except Exception as e:
                print(str(e))

            if event.key() == QtCore.Qt.Key_Tab: # and self.text_box.hasFocus():
                print('Tab pressed')
                self.indent()
                return True
        return False

    def indent(self):
        # inert tab for whole selection

        scroll_pos = self.textEdit.verticalScrollBar().value()

        cursor = self.textEdit.textCursor()
        old_position= cursor.position()

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        text = self.textEdit.toPlainText()

        mystr = text[:start]
        my_lines = []

        for line in text[start:end].split("\n"):
            my_lines.append("\t" + line)

        new_str =  "\n".join(my_lines)
        new_end = start + len(new_str)
        mystr += new_str

        mystr += text[end:]

        self.textEdit.setPlainText(mystr)

        cursor = self.textEdit.textCursor()
        if new_end - start > 1:

            cursor.setPosition(start)
            cursor.setPosition(new_end, QtGui.QTextCursor.KeepAnchor)
        else:
            cursor.setPosition(new_end)

        self.textEdit.setTextCursor(cursor)
        self.textEdit.verticalScrollBar().setValue(scroll_pos)

    def unindent(self):
        # inert tab for whole selection

        scroll_pos = self.textEdit.verticalScrollBar().value()

        cursor = self.textEdit.textCursor()
        old_position= cursor.position()

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        text = self.textEdit.toPlainText()

        mystr = text[:start]
        my_lines = []

        for line in text[start:end].split("\n"):
            if line.startswith("\t"):
                my_lines.append(line[1:])
            else:
                my_lines.append(line)

        new_str =  "\n".join(my_lines)
        new_end = start + len(new_str)
        mystr += new_str

        mystr += text[end:]

        self.textEdit.setPlainText(mystr)

        cursor = self.textEdit.textCursor()

        if new_end - start > 1:

            cursor.setPosition(start)
            cursor.setPosition(new_end, QtGui.QTextCursor.KeepAnchor)
        else:
            cursor.setPosition(new_end)

        self.textEdit.setTextCursor(cursor)
        self.textEdit.verticalScrollBar().setValue(scroll_pos)

    def text_changed(self):
        self.send_data()
        self.update_line_label()
        self.update()

    def update_line_label(self):
        cursor = self.textEdit.textCursor()
        x = cursor.blockNumber() + 1
        y = cursor.columnNumber() + 1
        self.lineLabel.setText('{0:d}, {1:d}'.format(x,y))

    def send_data(self):
        self.parent().mainloop_str = self.textEdit.toPlainText()
        if self.backup_count == 10:
            self.parent().auto_backup()
            self.backup_count = 0
        self.backup_count += 1

    def paintEvent(self,event):
        qp = QtGui.QPainter(self)
        pen = QtGui.QPen(Qt.black ,1, Qt.SolidLine)
        brush = QtGui.QBrush(Qt.black)
        qp.setBrush(brush)
        qp.setPen(pen)

        pen = QtGui.QPen(QtGui.QColor("#ababab") ,1, Qt.SolidLine)
        qp.setPen(pen)
        brush = QtGui.QBrush(QtGui.QColor("#ababab"))
        qp.setBrush(brush)

        positions = []
        for block_number in range(self.textEdit.document().lineCount()):

            offset = self.textEdit.contentOffset()

            block= self.textEdit.document().findBlockByNumber(block_number)
            brect = self.textEdit.blockBoundingGeometry(block)
            # print("brect", brect)
            y = int(brect.y()+ offset.y()) + 20  #  53
            x = int(brect.x() + 6)
            w = brect.width()
            h = brect.height()

            if(y > 20 and y <= 820):
                try:
                    if y not in positions:
                        qp.drawText(x,y+ 4,"%04i" % int(block_number))
                        positions.append(y)
                except:
                    pass

    def setUpEditor(self):
        self.highlighter = Highlighter()
        # python stuff
        fmt = QTextCharFormat()
        fmt.setForeground(QtGui.QColor("#ff3838"))
        for pattern in ['def ','for ', 'if ', 'else:', "while ", ' in ', ' not ', 'elif ', "True", "False", "class "]:
            self.highlighter.add_mapping(pattern,fmt)

        # return statement
        fmt = QTextCharFormat()
        fmt.setForeground(QtGui.QColor("#dae0dc"))
        for pattern in ['return']:
            self.highlighter.add_mapping(pattern,fmt)

        #print
        fmt = QTextCharFormat()
        fmt.setForeground(QtGui.QColor("#3f88e8"))
        for pattern in ['print']:
            self.highlighter.add_mapping(pattern,fmt)

        # python stuff
        fmt = QTextCharFormat()
        fmt.setForeground(QtGui.QColor("#4bb53f"))
        for pattern in ['from ','import ', 'as ']:
            self.highlighter.add_mapping(pattern,fmt)

        # comments
        fmt = QTextCharFormat()
        fmt.setForeground(QtGui.QColor("#121212"))
        self.highlighter.add_mapping(r'\"{3}[A-Za-z0-9_\n\t\wx^^    ]+\"{3}',fmt)

        fmt = QTextCharFormat()
        # fmt.setFontWeight(QFont.Bold)
        fmt.setForeground(QtGui.QColor("#6a6a6a"))
        pattern = r'\#\s.+'
        self.highlighter.add_mapping(pattern,fmt)

        searchtext = self.searchEdit.text()

        if searchtext != "":
            try:
                fmt = QTextCharFormat()
                # fmt.setFontItalic(True)
                fmt.setFontWeight(QFont.Bold)
                fmt.setForeground(QtGui.QColor("#fcf75b"))
                fmt.setBackground(QtGui.QColor("#000000"))
                self.highlighter.add_mapping(searchtext,fmt)
            except Exception as e:
                print(str(e))

        self.highlighter.setDocument(self.textEdit.document())
