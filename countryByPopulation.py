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

wheat_production_url = r'https://en.wikipedia.org/wiki/List_of_countries_by_wheat_production'
population_url = r'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'

population_query = pandas.read_html(population_url)
population_df = population_query[0]

# remove totals row as this throws everything off and remove everything after 2019
clipped = population_df.iloc[1:, 1:3]

location = clipped['Location'][:80].to_numpy()
location = [x.split(" ")[-1] for x in location ]
population = clipped['Population'][:80].to_numpy()
fig = plt.figure(figsize=(18,8))
plt.inferno()
plt.tight_layout()
plt.bar(location, population, width=0.9, color={'tab:orange'})
plt.xticks(rotation=80, ha='center')

plt.show()
