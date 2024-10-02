#%matplotlib ipympl
#%matplotlib inline  
import pandas
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl


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

def on_pick(event):
    # On the pick event, find the original line corresponding to the legend
    # proxy line, and toggle its visibility.
    #only pick visible items
    
    print ("onPicvk")
    print (event)
    #legend_item = event.artist
    #print (legend_item )
    return

#figure = plt.figure(figsize=(15, 15))
gdf_rm = gpd.read_file("C:\\Users\\Trevor\\Documents\\GitHub\\Palette_Cohort_7\\data\\custom.geo.json")
axis = gdf_rm.plot(aspect=1, edgecolor='black',figsize=(15, 15))
current_figure = axis.get_figure()
#chicago.plot(column="POP2010");
axis_lines = axis.get_lines()
axis_artists = axis.artists
print ("Axis")

print (dir(axis))
print (" ")
print("figure")
print (dir(current_figure))
items = axis.get_children()
patchCollection = [ x for x in axis.get_children() if type(x) == mpl.collections.PatchCollection]
#if patchCollection[0].contains(mouseevent):
print ("PatchCopllection")
print (patchCollection)
axis.add_callback(on_pick)


    


current_figure.canvas.mpl_connect('pick_event', on_pick)

plt.show()

#population_query = pandas.read_html(population_url)
#population_df = population_query[0]

# remove totals row as this throws everything off and remove everything after 2019
#clipped = population_df.iloc[1:, 1:3]

#location = clipped['Location'][:80].to_numpy()
#location = [x.split(" ")[-1] for x in location ]
#population = clipped['Population'][:80].to_numpy()
#fig = plt.figure(figsize=(18,8))
#plt.inferno()
#plt.tight_layout()
#plt.bar(location, population, width=0.9, color={'tab:orange'})
#plt.xticks(rotation=80, ha='center')

plt.show()
