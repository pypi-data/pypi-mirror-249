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
from sfctools import BalanceEntry

# qt modules
from PyQt5 import QtWidgets, uic,QtGui
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
        
        self.window = WorldViewerWindow(cluster_params, market_params, iter_func, wait_time, N_iter, indicators)
        self.worker = WorkerThread(self.window)
        self.worker.my_signal.connect(self.window.float_positions)
        self.worker.my_signal.connect(self.window.run_func)
        

        self.worker.start()
        self.window.show()


class WorkerThread(QThread):

    my_signal = pyqtSignal()

    def run(self):

        while True:
            time.sleep(.001)
            self.my_signal.emit()
        

class WorldViewerWindow(QtWidgets.QDialog):

    instance = None

    def __init__(self, cluster_params, market_params, iter_func, wait_time, N_iter, indicators):

        super().__init__() # Call the inherited classes __init__ method

        desk_rect = QtWidgets.QApplication.desktop().availableGeometry()
        cx, cy = desk_rect.center().x(), desk_rect.center().y()

        self.setGeometry(cx - 430, cy - 300, 860, 600)
        self.setWindowTitle("Viewer")
        self.positions = {}
        self.flucts = {}
        self.sizes = {}
        self.target_pos = {}
        self.current_pos = {} 

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
    
    def run_func(self):

        if self.n >= self.N_iter:
            return 
        
        self.t += 1

        if self.t % self.wait_time == 0:
            
            self.t = 0
            self.iter_func()
            self.n += 1 

            for k,v in self.indicator_labels.items():
                self.indicator_labels[k] = self.indicators[k]()
        
    
    def float_positions(self):
        
        # move around the boxes
        for k,v in self.flucts.items():
            dx = int(np.clip(v[0] + 0.67*np.random.uniform(-1,2), -20, 20))
            dy = int(np.clip(v[1] + 0.67*np.random.uniform(-1,2), -20, 20))

            self.flucts[k] = (dx, dy)
            
        
        for k, v in self.target_pos.items():
            a = 0.55
            self.current_pos[k] = (a * self.current_pos[k][0] + (1-a) * self.target_pos[k][0],(a * self.current_pos[k][1] + (1-a) * self.target_pos[k][1]))

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
                    
                
                    self.flucts[agent] = (0,0)
                    
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
        
        offsetx = 45
        offsety = 26
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

            self.qp.drawRect(int(scale*(other_pos[0]) + offsetx+ fluctx), int(scale*(other_pos[1]) + offsety + flucty), sz, sz)
        
        # draw legend 
        y_l = 20
        x_l = 20 

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
        
        yi = 26
        for name, f in self.indicator_labels.items():
            self.qp.drawText(15, yi , name)
            self.qp.drawText(80, yi , str(f))
            yi += 20
        
        self.qp.end()


    def paintEvent(self, event):

        self.paint()