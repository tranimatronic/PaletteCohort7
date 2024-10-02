import pandas
import geopandas as gpd
import matplotlib.pyplot as plt
import lxml
#from matplotlib.backend_tools import ToolBase
from matplotlib.transforms import Bbox
import matplotlib as mpl
#mpl.rcParams['toolbar'] = 'toolmanager'
#print (mpl.__version__)


"""
Python 3.11.1
Pandas 1.5.3
Matplotlib 3.8.4

The part I REALLY dislike about pandas, matplotlib and jupyter is the implicit code execution.
pandas.DataFrame.plot() creates a Frame and an Axis in the global matplotlib.pyplot object (that I may not 
have even imported) in the background and the pyplot.show() shows but then clears it. 
I have asked for none of these things and I dont wish them to happen implicitly without
explicit calls, and I certainly dont expect them to be cleared of data without my knowledge, as this leaves 
me wondering "....wait it worked before, why not now?"
"""

wheat_production_url = r'https://en.wikipedia.org/wiki/List_of_countries_by_wheat_production'
population_url = r'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'

wheat_query = pandas.read_html(wheat_production_url)
population_query = pandas.read_html(population_url)
wheat_df = wheat_query[0]
population_df = population_query[0]

# remove totals row as this throws everything off and everything after 2019
clipped = wheat_df.iloc[1:, :5]
gaa = clipped.set_index("Country")
# swap columns and rows
gaa = gaa.transpose()
# erase anything already existing in pyplot
plt.close()

# plot the data into pyplot. This returns the axis
axis = gaa.plot(title="Country Wheat Production (Million Metric Tonnes)", marker = 'o')
legend = axis.get_legend()
legend.set_loc("upper right")
legend.set_bbox_to_anchor((1.1, 0, 0.07, 1))
legend.set_draggable(True)
current_figure = plt.gcf()
current_figure.set_size_inches(12, 4)
axis_lines = axis.get_lines()
legend_texts = legend.get_texts()
legend_lines = legend.get_lines()
map_legend_to_ax = {}
map_text_to_ax = {}
pickradius = 2  # Points (Pt)
global isolated
isolated = 0

'''
figure is a pyplot root item
legend is a child of the axis returned by plot()
'''

for legend_line, ax_line in zip(legend_lines, axis_lines):
    legend_line.set_picker(pickradius)  # Enable picking on the legend line.
    ax_line.set_picker(pickradius)  # Enable picking on the legend line.
    map_legend_to_ax[legend_line] = ax_line
    #get the text of the legend from the index of the line
    #text_legend = legend_texts[legend_lines.index(legend_line)]
    #map_text_to_ax[text_legend] = ax_line

'''
class RefreshTool(ToolBase):
    """
    Overloaded default ToolBase class that resets ALL lines to visible
    """
    def trigger(self, *args, **kwargs):
        global isolated
        for legend_line, axisLine in zip(legend_lines, axis_lines):
            axisLine.set_visible(True)
            axisLine.set_markersize(0.2)
            ax_line.set_picker(2) 
            legend_line.set_alpha(1.0)
            annotation_box.set_visible(False)
            #record that all items are shown
            isolated = 0

        current_figure.canvas.draw()
    '''
        


annotation_box = axis.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annotation_box.set_visible(False)

canvas_manager = current_figure.canvas.manager
#tool_manager = current_figure.canvas.manager.toolmanager
#toolbar = current_figure.canvas.manager.toolbar
#tool_manager.add_tool("Refresh", RefreshTool)
#current_figure.canvas.manager.toolbar.add_tool(tool_manager.get_tool("Refresh"), "toolgroup")
# pixels to scroll per mousewheel event
scroll_values = {"down" : 30, "up" : -30}


def on_pick(event):
    # On the pick event, find the original line corresponding to the legend
    # proxy line, and toggle its visibility.
    #only pick visible items
    legend_item = event.artist
    ax_line = None
    global isolated
    # if the source is in the legend 
    if legend_item in map_legend_to_ax :
        ax_line = map_legend_to_ax[legend_item]
    elif legend_item in axis_lines:
        # if it is in main window, show the annotation box with values
        item_data = legend_item.get_data()
        contains, item_index = legend_item.contains(event.mouseevent)
        current_value = (str(item_data[1][item_index['ind'][0]]))
        item_text = str(legend_item).replace("Line2D(", "").replace(")", "")
        item_text = item_text + " " + current_value
        annotation_box.set_text(item_text)
        event_position = (float(event.mouseevent.x), float(event.mouseevent.y))
        annotation_box.set_visible(True)
        current_figure.canvas.draw_idle()
        return
    else:
        return
    
    # if we get here we are a Legend item
    # flag we have isolated an item
    isolated += 1
    for legend_line, axisLine in map_legend_to_ax.items():
        visible = not axisLine.get_visible()
        alpha = 1.0 if visible else 0.2
        markersize = 10 if not visible else 2
        # check that this one is the selected one. If so show it
        if legend_item == legend_line:
            axisLine.set_visible(True)
            axisLine.set_picker(2) 
            axisLine.set_markersize(3)
            legend_item.set_alpha(1.0)
        else:
            #if we have isolated something previously and the visible is on, leave this item
            # as we are showing multiple isolations
            current_viisibility = axisLine.get_visible()
            show_item = bool(bool(isolated>1) and current_viisibility) 

            if not show_item:
                axisLine.set_visible(False)
                axisLine.set_markersize(2)
                axisLine.set_picker(False) 
            legend_item.set_alpha(alpha)    
    

    #ax_line = map_legend_to_ax[legend_item]
    #visible = not ax_line.get_visible()
    #ax_line.set_visible(visible)
    # Change the alpha on the line in the legend, so we can see what lines
    # have been toggled.
    #legend_item.set_alpha(1.0 if visible else 0.2)
    current_figure.canvas.draw_idle()

def on_press(event):
    print ("Button press event")
    print (event)
    print (event.name)
    return
    legend_line = event.artist

def on_scroll(event):
    """
    scroll event function called by 'scroll_event'
    """
    print ("scroll")
    print (current_figure)
    print (event.button)
    if legend.contains(event)[0]:
        print ("legend", legend.contains(event))
        print ("axis", axis.contains(event))
        bbox = legend.get_bbox_to_anchor()
        offset = scroll_values[event.button]
        bbox = Bbox.from_bounds(bbox.x0, 
                                bbox.y0+offset, 
                                bbox.width, 
                                bbox.height)
        print (bbox)
        tr = legend.axes.transAxes.inverted()
        legend.set_bbox_to_anchor(bbox.transformed(tr))
        current_figure.canvas.draw_idle()
    
def on_press(event):
    """
    Keypress event monitoring. 
    """
    print (event.key)
    if (event.key == "r"):
        # reset "R" keypress.
        # reset all visibility to ON
        print ("R RPESS")
        global isolated
        for legend_line, axisLine in zip(legend_lines, axis_lines):
            axisLine.set_visible(True)
            axisLine.set_markersize(0.2)
            ax_line.set_picker(2) 
            legend_line.set_alpha(1.0)
            annotation_box.set_visible(False)
            #record that all items are shown
            isolated = 0

        current_figure.canvas.draw()


#current_figure.canvas.mpl_connect('figure_enter_event', on_hover)
#current_figure.canvas.mpl_connect('figure_leave_event', on_hover)

current_figure.canvas.mpl_connect('pick_event', on_pick)
current_figure.canvas.mpl_connect('scroll_event', on_scroll)
current_figure.canvas.mpl_connect('key_press_event', on_press)
#current_figure.canvas.mpl_connect("motion_notify_event", on_hover)

plt.show()


'''
>>> gaa = country_df2.set_index("Country")
>>> print (gaa)

Country  China  India  Russia  United States
2022[1]  137.7  107.7   104.2           44.9
2021[1]  136.9  109.6    76.1           44.8
2020[1]  134.3  107.9    85.9           49.8
2019[1]  133.6  103.6    74.5           52.6

>>> gaa.plot(title="Foo")

layout
top=0.935,
bottom=0.07,
left=0.03,
right=0.88,
hspace=0.155,
wspace=0.165
'''
# https://www.masc.mb.ca/masc.nsf/mmpp_browser_variety.html
# veriety yield data
#download manitoba data: https://geoportal.gov.mb.ca/datasets/8b64285c3bf6445a8d0d8ea4a1c43849/explore
# download .xls
# geopandas https://geopandas.org/en/stable/docs.html



