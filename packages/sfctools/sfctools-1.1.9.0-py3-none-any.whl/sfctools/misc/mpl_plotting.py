__version__ = "0.4"
__author__ = "Thomas Baldauf"
__email__ = "thomas.baldauf@dlr.de"
__license__ = "MIT"
__birthdate__ = '15.11.2021'
__status__ = 'prod' # options are: dev, test, prod

"""
Small plotting library for bar plots and line plots. Usage is optional / voluntary...
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pylab import rcParams
import matplotlib.patches as mpatches
import matplotlib as mpl
from functools import partial
import itertools

def add_value_labels(ax, spacing=.9, fmt="{0:f}", stacked=False, legend="best"):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    my_figure = ax.get_figure()
    L = abs(ax.get_ylim()[1] - ax.get_ylim()[0])
    min_height = L*0.015
    small_height = L*0.05
    # print("min_heigth", min_height)

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        outside = False

        if abs(rect.get_height()) <= min_height:
            continue

        elif abs(rect.get_height()) <= small_height:
            outside = True
            y_value = rect.get_y() + rect.get_height() * 0.1
            x_value = rect.get_x() + rect.get_width() * 1.05

        # print("rect height", rect.get_height())
        else:
            y_value = rect.get_y() + rect.get_height() * 0.41
            x_value = rect.get_x() + rect.get_width() * 0.50

        # print("yvalue",x_value,y_value)
        # Number of points between bar and label. Change to your liking.

        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        # label = "{:.1f}".format(y_value)
        hgt = rect.get_height()
        if hgt != 0.0:
            label = fmt.format(hgt)
        else:
            label = ""

        # Create annotation
        if outside:
            rot = 33
            ha = "left"
        else:
            rot = 0
            ha = "center"

        t = ax.annotate(
            label,  # Use `label` as label
            (x_value, y_value),  # Place label at end of the bar
            xytext=(0, space),  # Vertically shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            ha=ha,  # Horizontally center label
            va=va)  # Vertically align label differently for

        if not outside:
            t.set_bbox(dict(facecolor='white', alpha=0.175, edgecolor='white',linewidth=0.0))
        # positive and negative values.


def matplotlib_barplot(data, xlabel, ylabel, title, color="indigo", hatches=None, size=(6, 5), tight_layout=True,
                       fmt="{0:f}", stacked=False, show_labels=True, legend="best", show=True,yerr=None,ax=None):
    """
    Creates a bar plot in matplotlib. The 'macro' plotting style will be used if it is set up

    :param xlabel: x axis  label
    :param ylabel: y axis  label
    :param title: plot title
    :param color: plot color
    :param hatches: hatch pattern
    :param size: figure size
    :param tight_layout: re-format plot
    :param fmt: number format, {0:d} or {0:f} for example
    :param stacked: stack column? or show side-by side (boolean)
    :paarm show_labels: show the column labels at bottom? (boolean)
    :param legend: location of legend, or 'off'
    :param show: if False, only the figure is returned. Else plot is shown
    :param ax: axis to plot on
    :param yerr: data for error bar (if any)
    """

    # if legend is 'off', no legend is shown

    plt.rcParams['axes.ymargin'] = .4
    rcParams['figure.figsize'] = size

    try:
        plt.style.use("macro") # if 'macro' plotting style is installed -> use it!
    except:
        pass

    plt.grid(alpha=0.0)

    if not isinstance(data, pd.DataFrame):
        if ylabel is None:
            ylabel = "Data"
        data = pd.DataFrame({ylabel: data})
        data.set_index(ylabel)

    # plt.figure(figsize=size)
    if ax is None:
        ax = plt.gca()
    
    data.plot.bar(color=color, stacked=stacked, ax=ax, yerr=yerr, capsize=6, ecolor="black")
    
    if hatches is not None:
        n_cols = len(data)
        myhatches = itertools.cycle(hatches)
        for i, bar in enumerate(plt.gca().patches):
            if i % n_cols == 0:
                hatch = next(myhatches)
            bar.set_hatch(hatch)
            
    plt.gca().set_title(title)
    # plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    if show_labels:
        add_value_labels(plt.gca(), fmt=fmt)

    if legend != "off":
        plt.legend(loc=legend)
    else:
        old_legend = plt.gca().get_legend()
        if old_legend is not None:
            old_legend.remove()
    if tight_layout:
        plt.tight_layout()

    # fix reverse labeling
    # https://stackoverflow.com/questions/46908085/bar-plot-does-not-respect-order-of-the-legend-text-in-matplotlib
    #
    ax = plt.gca()
    h, l = ax.get_legend_handles_labels()
    if legend != "off":
        ax.legend(h[::-1], l[::-1],loc=legend,framealpha=0.0)

    if show:
        plt.show()
    else:
        return plt.gcf()


def matplotlib_lineplot(data, xlabel=None, ylabel=None, title="", xlim=None, ylim=None, color="indigo", legend="best",marker=None,show=False,ax=None):
    """
    creates a line plot in matplotlib. The 'macro' plotting style will be used if it is set up

    :param xlabel: x axis  label
    :param ylabel: y axis  label
    :param title: plot title
    :param color: plot color
    :param xlim, ylim: tuples of plot limits
    :param legend: location of legend, or 'off', or 'outside'
    :param show: if False, only the figure is returned. Else plot is shown
    :param ax: axis to plot on

    when overlapping barplot and lineplot, make sure you add an additional axis, see
    https://stackoverflow.com/questions/42948576/pandas-plot-does-not-overlay

    """
    try:
        plt.style.use("macro")
    except:
        pass


    if not isinstance(data, pd.DataFrame):
        if ylabel is None:
            label = "Data"
        data = pd.DataFrame({ylabel: data})
        data.set_index(ylabel)

    if ax is None:
        ax = plt.gca()

    for col in data.columns:
        ax.plot(data[col],color=color,marker=marker,label=col)

    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.title(title)

    if legend != "off":
        plt.legend(loc=legend)
    elif legend == "outside":
        plt.legend(loc=(1.02,0))

    elif legen == "off":
        old_legend = plt.gca().get_legend()
        if old_legend is not None:
            old_legend.remove()

    if ylabel is not None:
        plt.ylabel(ylabel)

    if xlabel is not None:
        plt.gca().set_xlabel(xlabel)

    if ylabel is not None:
        plt.gca().set_ylabel(ylabel)
    plt.rcParams['axes.ymargin'] = .4

    if show:
        plt.show()
    else:
        return plt.gcf()





class Point:
    """
    a rudimentary point in 2d space
    """

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.offset_y = 0 # offset for bands

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y + self.offset_y

class Label:
    """
    a rudimentary node label
    """

    names = []

    def __init__(self,x,y,text):
        self.x = x
        self.y = y
        self.text = text
        if text in self.__class__.names:
            raise RuntimeError("Name already given")
        else:
            self.__class__.names.append(self.text)

    def shift_up(self):
        # shift the label upwards a bit
        self.y += 1.8
        self.x -= 0.2 # re-center


def casteljau(t,b0,b1,b2,b3):
    """
    casteljau bezier spline for 4 points.

    :param b0-b3: the point of the bezier curve as [x,y] array
    :param t: parameter for position on the curve, float
    """
    b = np.multiply((-b0 + 3*b1 - 3*b2 + b3),np.power(t,3))  + np.multiply((3*b0 - 6*b1 + 3*b2),np.power(t,2)) + np.multiply((-3*b0 + 3*b1),t) + b0
    return b


def bezier(pstart : Point, pend: Point ,npoints = 100, curv=None):
    """
    compute the path of a 1d bezier curve

    :param pstart: starting point of the bezier curve
    :param pend: end point of the bezier curve
    :param npoints: number of discrete points to retrun
    :param curv: optionally you can give a curvature parameter here (float) default None

    :return: x,y coordinate tuple as ndarray of shape (npoints,)
    """

    # de-casteljau b-spline
    tarr = np.linspace(0,1,npoints) # parameter of the curve position
    # define 4 points: b0, b1, b2, b3

    if pstart.x < pend.x: # pstart left of pend?
        pleft = pstart
        pright = pend
    else:
        pleft = pend
        pright = pstart

    if curv is None:
        curv = .27*(pright.x-pleft.x)

    b0 = np.array([pleft.x,pleft.y])
    b1 = np.array([pleft.x+curv,pleft.y])
    b2 = np.array([pright.x-curv,pright.y])
    b3 = np.array([pright.x,pright.y])

    spline = partial(casteljau,b0=b0,b1=b1,b2=b2,b3=b3)

    b = np.array([spline(t) for t in tarr])

    return b[:,0],b[:,1]


def plot_band(pstart: Point, pend: Point, npoints=100,curv=None, weight=2):
    """
    computes a band of two bezier curves

    :param pstart: starting point of the bezier curve
    :param pend: end point of the bezier curve
    :param npoints: number of discrete points to retrun
    :param curv: optionally you can give a curvature parameter here (float) default None
    :param weight: width of the band

    :return: x,y1,y2 coordinate 3-tuple of the band
    """

    w = weight # width of the band
    d = 0 # horizontal shift of the bands realtive to each other
    e = 0 # distance of  '<' and '>' arc

    qstart1 = Point(pstart.x-d,pstart.y)
    qstart2 = Point(pstart.x-d,pstart.y)

    qend  = Point(pend.x-d,pend.y)
    qend1  = Point(pend.x-d,pend.y)
    qend2  = Point(pend.x-d,pend.y)

    pstart1 = Point(pstart.x-d+.2*e,pstart.y)
    pend1 = Point(pend.x-d-e,pend.y)

    pstart2 = Point(pstart.x+d+.2*e,pstart.y+w)
    pend2 = Point(pend.x+d-e,pend.y+w)

    bezier_start1 = bezier(qstart1,pstart1)
    bezier_start2 = bezier(qstart2,pstart2)

    bezier_end1 = bezier(pend1,pend1)
    bezier_end2 = bezier(pend2,pend2)

    bezier1 = bezier(pstart1,pend1)
    bezier2 = bezier(pstart2,pend2)

    #x = np.array(list(bezier_start1[0])+list(bezier1[0])+list(bezier_end1[0]))
    #y1 = np.array(list(bezier_start1[1])+list(bezier1[1])+list(bezier_end1[1]))
    #y2 = np.array(list(bezier_start2[1])+list(bezier2[1])+list(bezier_end2[1]))

    x = np.array(list(bezier1[0]))  # + list(bezier_end1[0]))
    y1 = np.array(list(bezier1[1])) #  + list(bezier_end1[1]))
    y2 = np.array(list(bezier2[1])) # + list(bezier_end2[1]))


    return x, y1, y2


def draw_band(fig,pstart:Point, pend:Point, color="blue",alpha=.9,weight=2,norm=1.0,show_label=True,label=None,dv=0.6,rotation=0):
    """
    draw a band graphically

    """
    x,y1,y2 = band(pstart,pend,weight=weight)
    plt.fill_between(x,y1,y2,color=color,figure=fig,alpha=alpha)
    
    my_bez_x, my_bez_y = bezier(Point(pstart.x, pstart.y), Point(pend.x, pend.y))
    
    plt.plot(my_bez_x, my_bez_y, color="black",alpha=.7) # "black")

    if show_label and label is not None:
        # draw bezier
        
        # dv = 0.6
        bx = my_bez_x[int(dv*len(my_bez_x))]
        by = my_bez_y[int(dv*len(my_bez_y))]

        
        #bx2,by2 = casteljau(t=0.55,b0=np.array([pstart.x,pstart.y]),b1=b1,b2=b2,b3=np.array([pend.x,pend.y]))
        #bx3,by3 = casteljau(t=0.66,b0=np.array([pstart.x,pstart.y]),b1=b1,b2=b2,b3=np.array([pend.x,pend.y]))
        #rot = (90-.5*np.arctan2((bx3-bx2),(by3-by2))*180.0/np.pi)%360.0 # compute slope at point
        #rot = 0

        bbox = {'pad': 2, 'facecolor': color,'edgecolor':color,'linewidth':.0}
        props = {'ha': 'center', 'va': 'center', 'bbox': bbox}

        if label is not None:
            plt.gca().text(bx,by - .0, label, props, rotation=rotation,color="white", alpha=alpha)
        else:
            plt.gca().text(bx,by , "%.2f" %(weight/norm), props, rotation=rotation,color="black",alpha=alpha)

        
        # plt.annotate(str(weight),(bx,by),color="gray",alpha=alpha)

    pend.offset_y += 1.5*weight
    pstart.offset_y += 1.5*weight

def plot_sankey(data,title="",show_plot=True,
                show_values=True,
                colors=None,
                label_rot=65,
                fontsize=10,
                separation=0.8,
                norm_factor=1.5,
                min_width=0.1,
                dy=10,
                dx=55,
                dx_space=8.5,
                alpha=0.5,
                filling_fraction = 0.85):
    """
    plots a sankey diagram from data

    :param data: list of pandas dataframes, of the following format. length at least two.
    :param title: title of the plot
    :param show_plot: boolean switch to show plot window (default True). If False, figure is returned
    :param show_values: boolean switch to print numerical values of data as text label (default True)
    :param colors: (optional) a list of colors (if None, default colors are chosen)
    :param label_rot: rotation of the labels (default 65 degrees)
    :param fontsize: size of label font
    :param separation: separation point of the label along the bands, between 0 and 1,
    :param norm_factor: normalization factor for width 
    :param min_width: minimum width of bands
    :param dy: vertical distance of bands
    :param dx: horizontal distance of bands
    :param dx_space: space between layers
    :param filling_fraction: fraction by which the bands align (scaling with dy)

    :return fig: None or matplotlib figure

    Example: 

    +----------+----------+----------+-------------+
    |  from    |   to     |  value   | color_id    |
    +----------+----------+----------+-------------+
    |    A     |  C       | 1.0      |    0        |
    +----------+----------+----------+-------------+
    |    A     |  D       | 2.0      |    1        |
    +----------+----------+----------+-------------+
    |    B     |  D       | 3.0      |    2        |
    +----------+----------+----------+-------------+

    +----------+----------+----------+-------------+
    |  from    |   to     |  value   | color_id    |
    +----------+----------+----------+-------------+
    |    C     |  E       | 5.0      |    1        |
    +----------+----------+----------+-------------+
    |    C     |  F       | 6.0      |    2        |
    +----------+----------+----------+-------------+
    |    D     |  G       | 8.0      |    3        |
    +----------+----------+----------+-------------+

    """

    Label.names = []

    if not isinstance(data,list):
        data = [data] # convert to list

    if colors is None:
        colors = [
            "lightgray",
            "skyblue",
            "wheat",
            "lightgreen",
            "lavender",
        ]
    
    # 1. normalize the values to reasonable width of bands

    # norm_factor = 1.5 #normalization factor for width

    maxval = 0.0
    maxrows = 2

    for layer in data:

        maxrows = max(maxrows,len(list(layer.iterrows())))
        for idx,row in layer.iterrows():
            val = float(row["value"])

            maxval = max(val,maxval)

    # norm_factor = 1.5
    if maxval > 0.0:
        norm_factor = 1.0 /maxval

    fig = plt.figure(figsize=(2.4*len(data),1.05*maxrows)) # 1.8*maxrows

    # 2. plot the bezier patches

    i = 10  #
    j0 = 6 # < starting position (i,j)

    # dy = 10 # 8  # vertical distance of bands
    # dx = 55 #   # horizontal distance of layers

    # dx_space = 2.5 # white space between layers

    # define some points for the unique nodes
    my_points = {} # keys will be names, value will be Points
    my_labels = {} # keys will be names, value will be Labels
    my_values = {} # labels for values

    last_j = j0

    # iterate through the dataframes
    # heights = defaultdict(lambda: 0 )

    
    class Band:
    

            instances = [] 
            def __init__(self,n_from,n_to,w,color="steelblue"):
                self.n_from = n_from 
                self.n_to = n_to 
                self.shift_y =0.0 
                self.width =  2* w
                self.osy1 = 0.0
                self.osy2 = 0.0
                self.color = color
                self.__class__.instances.append(self) 

            def plot(self):
                fromnode = self.n_from 
                tonode = self.n_to
                w = self.width
                osy1 = self.osy1
                osy2 = self.osy2
                
                #vals_lower = [fromnode.y+osy1,tonode.y+osy2]
                #vals_upper = [fromnode.y+osy1 + w,tonode.y+osy2 + w]

                point_lower1 = Point(fromnode.x,fromnode.y+osy1)
                point_lower2  = Point(tonode.x, tonode.y + osy2)
                # point_lower2 = Point(fromnode.x,fromnode.y+osy1+w)

                # make the curves more smooth 
                x, vals_lower, vals_upper = plot_band(point_lower1, point_lower2,weight=w)
                plt.fill_between(x, vals_lower, vals_upper,color=self.color)
                
                
            def maxy(self):
                w = 2 * self.width 
                return max([self.n_from.y+ self.osy1 + w, self.n_to.y+ self.osy2 + w])
            

   

    from collections import defaultdict
    bands = defaultdict(lambda: [])

    
    for indx, layer in enumerate(data):

        j =  j0 

        k = 0
        for name in layer["from"].unique():

            if name not in my_points:
                new_point = Point(i+dx_space,j)
                my_points[name] = new_point

                j += dy

            if name not in my_labels:
                my_labels[name] = Label(new_point.x-5.2,new_point.y-.2,name) # plt.annotate(name,(new_point.x-1.8, new_point.y-.1))
            else:

                my_labels[name].shift_up()

            k+=1

        j = j0

        k = 0
        for name in layer["to"].unique():

            if name not in my_points:
                new_point = Point(i+dx,j)
                my_points[name] = new_point #Point(i+dx,j)

                j += dy 

            if name not in my_labels:
                my_labels[name] = Label(new_point.x+.5*dx_space,new_point.y-.2,name) # plt.annotate(name,(new_point.x+.5*dx_space,new_point.y-.1))
            else:
                my_labels[name].shift_up()
            
            k += 1

        last_j = j - dy

        for idx, row in layer.iterrows():

            fromnode = my_points[row["from"]]
            tonode = my_points[row["to"]]
            color_idx = row["color_id"]

            my_band = Band(fromnode, tonode, w = float(row["value"])*norm_factor * dy * (1-filling_fraction), color = colors[color_idx%len(colors)])
            
            bands[fromnode].append(my_band)
            bands[tonode].append(my_band)

        i += dx

        #for name,point in my_points.items():
        #    point.offset_y = 0

        # iterate through the dataframe rows


        for point, b in bands.items():
             
            offset1 = 0.0 
            offset2 = 0.0 

            for bi in b:

                if point == bi.n_from:
                    bi.osy1 = offset1
                    offset1 += bi.width 

                elif point == bi.n_to:
                    bi.osy2 = offset2
                    offset2 += bi.width 
          

        # plot all bands 
        for band in Band.instances:
            band.plot()

        """
        for idx, row in layer.iterrows():

            color_idx = int(row["color_id"]) # index for color map

            fromnode = my_points[row["from"]]
            tonode = my_points[row["to"]]
            weight = float(row["value"])*norm_factor # 8.5e-2 #  max(min_width,float(row["value"])*norm_factor) # <- make bars thicker

            draw_band(fig,fromnode,tonode,colors[color_idx%len(colors)],weight=weight,norm=norm_factor,show_label=show_values,rotation=0,dv=separation,label=str(row["value"]))

            # update weight for next layer
        """


    for label in my_labels.values(): # draw the labels here...
        if len(label.text) <= 2:
            plt.annotate(label.text.replace("$[source]","").replace("$[sink]",""),(label.x,label.y))
        else: # rotate label for better visibility
            plt.gca().text(label.x,label.y, label.text.replace("$[source]","").replace("$[sink]",""), rotation=label_rot,fontsize=fontsize)

    # 3. return the figure or show window

    plt.axis("off")

    max_x = 0
    max_y = 0

    for point in my_points.values():
        max_x = max(max_x,point.x)
        max_y = max(max_y,point.y)

    for label in my_labels.values():
        max_x = max(max_x,label.x)
        max_y = max(max_y,label.y)

    maxy = max([b.maxy() for b in Band.instances])
    plt.xlim([3,max_x+5])
    plt.ylim([3,maxy+3])

    #plt.autoscale()

    plt.tight_layout()

    plt.title(title)

    plt.tight_layout()

    if show_plot:
        plt.show()

    return fig
