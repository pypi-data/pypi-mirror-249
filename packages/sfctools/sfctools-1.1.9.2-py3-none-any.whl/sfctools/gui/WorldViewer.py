# standard modules 
import sys
import os
import yaml
import shutil
import time
import datetime
import pickle as pkl
import re
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np 
from itertools import cycle
import networkx as nx 
# from community_layout.layout_class import CommunityLayout

from sfctools import World ,Agent
from sfctools.bottomup.matching import MarketMatching
from sfctools import BalanceEntry, BalanceMatrix,FlowMatrix
from sfctools.misc.reporting_sheet import ReportingSheet 

# qt modules
from PyQt5 import QtWidgets, uic,QtGui
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog,QMessageBox,QTableWidgetItem,QAbstractItemView,QListWidgetItem
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QFontDatabase, QColor, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

import time 


"""
This module provides a simple visualization window 
for the agents in the sfctools.World and the market connections

(BETA version)
"""


class WorldViewer:

  
    def __init__(self, cluster_params = None, market_params = None, N_iter = 1, iter_func= None , wait_time=1, indicators = None):
        """
        The world viewer is a little visualization winodw
        indicating agents as boxes, and connecting them with lines (market interactions)
        """

        if iter_func is None:
            def f():
                pass 

            iter_func = f
        
        if indicators is None:
            indicators = {}
        
        self.app = QtWidgets.QApplication(sys.argv)
        
        self.window = WorldViewerWindow(cluster_params, market_params, iter_func, wait_time, N_iter, indicators, parent=None)
        
        self.worker = WorkerThread(self.window)

        self.worker.my_signal.connect(self.window.float_positions)
        # self.worker.my_signal.connect(self.window.run_func)
    
        self.worker.start()
        self.window.show()
        
        
    def start(self):
        self.app.exec_()

class WorkerThread(QThread):

    my_signal = pyqtSignal()

    def run(self):

        while True:
            time.sleep(0.05)
            self.my_signal.emit()
        

class WorldViewerWindow(QtWidgets.QMainWindow):

    instance = None
    

    def __init__(self, cluster_params, market_params, iter_func, wait_time, N_iter, indicators, parent=None):

        super().__init__(parent) # Call the inherited classes __init__ method
        path = os.path.dirname(os.path.abspath(__file__))
        

        desk_rect = QtWidgets.QApplication.desktop().availableGeometry()
        cx, cy = desk_rect.center().x(), desk_rect.center().y()

        
        
        self.setGeometry(cx - 430, cy - 300, 860, 600)
        self.setWindowTitle("Viewer")
        self.positions = {}
        self.flucts = {}
        self.sizes = {}
        self.target_pos = {}
        self.current_pos = {}
        self.current_pos_transformed = {} 

        self.velocities = {}

        # self.qp = QtGui.QPainter(self) # .paint_widget)

        self.indicators = indicators
        self.indicator_labels = {k: "-" for k in self.indicators.keys()}
        
        self.t = 0

        self.iter_func = iter_func 

        if cluster_params is not None:
            self.params = cluster_params
        else:
            self.params = {}
        
        if market_params is not None:
            self.mparams = market_params
        
        else:
            self.mparams = {}
    
        self.wait_time = wait_time 
        self.N_iter = N_iter 
        self.n = 0

        self.k = 0

        uic.loadUi(os.path.join(path,'WorldViewerWindow.ui'), self)
        
        self.BtnStep.pressed.connect(self.run_func)
        self.BtnStep.pressed.connect(self.update_bs_matrix)
        self.BtnStep.pressed.connect(self.update_tf_matrix)
        self.BtnStep.pressed.connect(self.fill_agents)
        self.BtnStep.pressed.connect(self.fill_reporting)
        self.BtnStep.pressed.connect(self.update_report_data)
        self.BtnStep.pressed.connect(self.show_report_data)

        self.refreshButton.pressed.connect(self.update_bs_matrix)
        self.refreshButton.pressed.connect(self.update_tf_matrix)
        self.refreshButton.pressed.connect(self.fill_agents)
        self.refreshButton.pressed.connect(self.fill_reporting)
        self.refreshButton.pressed.connect(self.update_agent_data)

        self.treeWidget.itemClicked.connect(self.update_agent_data)
        self.listWidget.itemClicked.connect(self.update_report_data)
        self.listWidget_2.itemClicked.connect(self.show_report_data)

        self.lineEdit.textChanged.connect(self.update_agent_data)

        self.plotButton.pressed.connect(self.plot_report)

        self.setMouseTracking(True)
    
    def plot_report(self):
        
        try:
            report_name = self.listWidget.currentItem().text()
            report = self.sheets[report_name]
            report.plot(show_plot=True)
        
        except Exception as e:
            print("Exception:", str(e))

    def show_report_data(self):

        try:
            sheet_name = self.listWidget_2.currentItem().text()
        
            #report_name = self.listWidget.currentItem().text()
            #report = self.sheets[report_name]

            if sheet_name in self.reports:

                report = self.reports[sheet_name]
                print("REPORT", report)

                self.OutputText.setPlainText(str(report.data))
        except:
            pass
    
    def update_report_data(self):

        try:
            name = self.listWidget.currentItem().text()
            if name in self.sheets:
                report = self.sheets[name]

                print(report.items)

                self.listWidget_2.clear()
                self.listWidget_2.addItems([str(item) for item in report.items])
        except:
            pass        

    def fill_reporting(self):
        print("instances", ReportingSheet.instances)

        # insert sheets into the list view
        self.listWidget.clear()
        self.sheets = {} 
        self.reports = {}

        for sheet in ReportingSheet.instances:
            self.sheets[str(sheet.name)] = sheet 

            for item in sheet.items:
                self.reports[str(item)] = item 

        self.listWidget.addItems(list(self.sheets.keys()))


    def update_agent_data(self):

        try:
            agent_name = self.treeWidget.currentItem().text(self.treeWidget.currentColumn())
        except:
            return 
        
        try:
            
            class_name = self.treeWidget.currentItem().parent().text(self.treeWidget.currentColumn())
        except:
            
            class_name = agent_name 


        print("->" , agent_name, class_name)
        if class_name != agent_name:

            agent = World().find_agent(agent_name)

            try:
                s = str(agent.balance_sheet.to_string())
                self.plainTextEdit.setPlainText(s)        

            except Exception as e:
                self.plainTextEdit.setPlainText(str(e))


            try:
                s = str(agent.income_statement.to_string())
                self.plainTextEdit_2.setPlainText(s)
            except Exception as e:
                self.plainTextEdit_2.setPlainText(str(e))

            try:
                s = str(agent.cash_flow_statement.to_string())
                self.plainTextEdit_3.setPlainText(s)
            except Exception as e:
                self.plainTextEdit_3.setPlainText(str(e))


            # try attribute search
            try:
                search_str = self.lineEdit.text()
                if hasattr(agent, search_str):
                    self.attrLabel.setText(str(agent.__getattribute__(search_str)))
                else:
                    self.attrLabel.setText("(not found)")

            except Exception as e:
                self.attrLabel.setText(str(e))


    def run_func(self):

        print("RUN FUNC", self.t)

        try:
            n_rep = int(self.lineEdit_nIter.text())
        except:
            n_rep = 1 
        
        for tk in range(n_rep):

            if self.n >= self.N_iter:
                return 
            
            self.t += 1

            self.label_niter.setText("%04i" % (self.n+1))
            self.update()

            if self.t % self.wait_time == 0:
                
                self.t = 0
                self.iter_func()
                self.n += 1 

                for k,v in self.indicator_labels.items():
                    self.indicator_labels[k] = self.indicators[k]()


    def fill_agents(self):
        """
        fills the tree widget to show the agents
        """
        
        last_state = {} 

        my_registry = dict(World().agent_registry)

        for key, value in my_registry.items():
            items = self.treeWidget.findItems(key,Qt.MatchFixedString)
            for item in items:
                if item.isExpanded():
                    last_state[str(key)] = True 
                else:
                    last_state[str(key)] = False 

        self.treeWidget.clear()

        for key, value in my_registry.items():
            root = QTreeWidgetItem(self.treeWidget, [str(key)])
            for val in value:
                item = QTreeWidgetItem([str(val)])
                root.addChild(item)
        # Or
        # QTreeWidgetItem(root, [val])
        #self.treeWidget.expandAll()
            
        for name, was_expanded in last_state.items():
            if was_expanded:
                items = self.treeWidget.findItems(name,Qt.MatchFixedString)
                for item in items:
                    self.treeWidget.expandItem(item)
        
        self.treeWidget.show()


    def update_tf_matrix(self):
        try:
            # BalanceMatrix().fill_data()

            s = FlowMatrix().to_string()
            self.TFMatrixText.setPlainText(s)
        
        except Exception as e:
            self.TFMatrixText.setPlainText(str(e))
 
    def update_bs_matrix(self):
        try:
            # BalanceMatrix().fill_data()
            if not self.checkBox.isChecked():
                s = BalanceMatrix().to_string()
            else:
                s = BalanceMatrix().to_string(flip=True)
            self.BSMatrixText.setPlainText(s)
        
        except Exception as e:
            
            self.BSMatrixText.setPlainText(str(e))

        #BalanceMatrix().reset()
        #BalanceMatrix().init_data()
    
    def float_positions(self):
        
        #self.k += 1
        #if self.k % 50 == 0:
        #    self.k = 0

        # move around the boxes
        for k,v in self.velocities.items():
            x = (np.clip(v[0] + np.clip(np.random.normal(0,.00015),-10.5,10.5), -2000, 2000))
            y = (np.clip(v[1] + np.clip(np.random.normal(0,.00015),-10.5,10.5), -2000, 2000))
            
            x = np.clip(x, -.01, .01)
            y = np.clip(y, -.01, .01)

            self.velocities[k] = (x, y)
            # print(x,y)
    
        for k, v in self.target_pos.items():
            a = 0.8
            self.current_pos[k] = (a * self.current_pos[k][0] + (1-a) * self.target_pos[k][0] ,(a * self.current_pos[k][1] + (1-a) * self.target_pos[k][1]))
            
            if k in self.velocities:
                self.current_pos[k]  = (self.current_pos[k][0] + self.velocities[k][0], self.current_pos[k][1] + self.velocities[k][1])
        
        self.repaint()

     
    def paint(self):

        self.qp = QtGui.QPainter(self)
        
        self.qp.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        self.qp.setRenderHint(QtGui.QPainter.TextAntialiasing)
        
        #self.pen =  QtGui.QPen()
        #self.qp.setPen(self.pen)
        
        cols = cycle(["blue", "gray", "red", "orange", "limegreen", "indigo"])
        
        for name, l in World().agent_registry.items():
            
            if name not in self.params.keys():
                continue 
            
            color = next(cols) 
            
            if len(l) == 0:
                continue 
            
            max_assets = max([a.balance_sheet.total_assets for a in l] )
            min_assets = min([a.balance_sheet.total_assets for a in l] )

            for agent in l:
                
                if agent not in self.flucts:
                    # assign new position
                    success = False
                    if str(name) in self.params:
                        color = self.params[name]
                        # print(color)
                    else:
                        # x0, y0 = (200, 200)
                        self.params[name] = "black"
                    
                
                    self.flucts[agent] = (np.random.uniform(-10.1, 10.1), np.random.uniform(-10.1, 10.1))
                    
                size = 3

                # re-scale agents according to their total assets 
                if abs(max_assets - min_assets) > 1e-6:
                    size = max(3, 10*(agent.balance_sheet.total_assets-min_assets) / (max_assets-min_assets))
                
                self.sizes[agent] = size 
                # self.qp.drawRect(int(x+ dx), int(y+dy), size, size)
        
        # market interactions 
        
        G = nx.Graph()
        for market, params in self.mparams.items():
            
            for s_agent in market.supply_list:
                #x,y = self.positions[s_agent]
                #dx,dy = self.flucts[s_agent]

                sz = 5 
                if s_agent in self.sizes:
                    sz = int(0.5*self.sizes[s_agent] )
                else:
                    self.sizes[s_agent] = 10 
                
                # a,b = (int(x+dx)  + sz, int(y+dy)+ sz)

                for d_agent in market.get_demanders_from(s_agent):
                    
                    #x,y = self.positions[d_agent]
                    #dx, dy = self.flucts[d_agent]

                    sz = 5 
                    if d_agent in self.sizes:
                        sz = int(0.5*self.sizes[d_agent] )
                    else:
                        self.sizes[d_agent] = 10   
                     
                    # u, v = (int(x+dx)+ sz, int(y+dy) + sz)
                    
                    # add link to graph 
                    G.add_edge(s_agent, d_agent, name=market)

                    lstyle, color = params
        

        for agent in self.sizes.keys():
            if agent not in G.nodes:
                G.add_node(agent)

        #nx.draw(G)
        #plt.show()
        # retrieve positions 
        # np.random.seed(23958)
        nodePos = nx.spring_layout(G, seed=349587)
        
        offsetx = 45 + self.paint_widget.x()
        offsety = 26 + self.paint_widget.y()
        scale = 500

        # scale such that everything is on the screen 
        maxx = 0
        maxy = 0
        minx = 500
        miny = 500

        for node, pos in nodePos.items():
            maxx = max(pos[0],maxx)
            maxy = max(pos[1],maxy)
            minx = min(pos[0],minx)
            miny = min(pos[1],miny)

        for node, pos in nodePos.items():
            nodePos[node] = [1.5*(pos[0] - minx)/(maxx-minx), (pos[1]-miny)/(maxy-miny)]

        for node, pos in nodePos.items():
            self.target_pos[node] = pos 

            if node not in self.current_pos:
                self.current_pos[node] = pos 

            if node not in self.velocities:
                self.velocities[node] = (np.random.uniform(-10.1, 10.1), np.random.uniform(-10.1, 10.1))

        # draw links 
        for edge in G.edges.data():
            a1 = edge[0]
            a2 = edge[1]

            style, color = self.mparams[edge[2]["name"]]
            # print("color", color)
            r, g, bl, alpha = mpl.colors.to_rgba(color)
            self.pen =  QtGui.QPen(QtGui.QColor(int(r*255),int(g*255),int(bl*255), 255), 1) 

            a = int(scale*(self.current_pos[a1][0] ) + offsetx + self.sizes[a1]*0.5 +  self.flucts[a1][0])
            b = int(scale*(self.current_pos[a1][1] ) + offsety + self.sizes[a1]*0.5 +  self.flucts[a1][1])

            u = int(scale*(self.current_pos[a2][0]) + offsetx + self.sizes[a2]*0.5 + self.flucts[a2][0])
            v = int(scale*(self.current_pos[a2][1]) + offsety + self.sizes[a2]*0.5 + self.flucts[a2][1])

            self.qp.setPen(self.pen)
            self.qp.drawLine(a,b,u,v)
        
        # self.qp.drawRect(offsetx,offsety,offsetx+1.5*scale,offsety+scale)
            
        # draw nodes
        for node, pos in nodePos.items():
        
            color = self.params[node.__class__.__name__]
            r, g, bl, alpha = mpl.colors.to_rgba(color)
            self.pen =  QtGui.QPen(QtGui.QColor(int(r*255),int(g*255),int(bl*255), 255), 1) 
                
            self.qp.setPen(self.pen)
            fluctx, flucty = self.flucts[node]
            sz = int(self.sizes[node])

            other_pos = self.current_pos[node]

            l,m = int(scale*(other_pos[0]) + offsetx+ fluctx), int(scale*(other_pos[1]) + offsety + flucty)
            self.current_pos_transformed[node] = (l,m)
            self.qp.drawRect(l,m, sz, sz)
        
        # draw legend 

        r,g,bl = 0,0,0
        self.pen =  QtGui.QPen(QtGui.QColor(int(r*255),int(g*255),int(bl*255), 255), 1) 
        self.qp.setPen(self.pen)
        k = 0

        for name, l in World().agent_registry.items():
            
            # TODO insert code here 

            # self.qp.drawRect(int(scale*(pos[0]) + offsetx+ fluctx), int(scale*(pos[1]) + offsety + flucty), sz, sz)
            # self.qp.
            
            k += 1

        # self.qp.drawRect(20,20,
        
        yi = 26 + self.paint_widget.y()
        for name, f in self.indicator_labels.items():
            self.qp.drawText(15+ self.paint_widget.x(), yi , name)
            self.qp.drawText(80+ self.paint_widget.x(), yi , str(f))
            yi += 20
        
        self.qp.end()


    def paintEvent(self, event):

        self.paint()