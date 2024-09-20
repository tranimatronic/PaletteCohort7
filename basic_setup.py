import pandas
import matplotlib
import geopandas as gpd
import matplotlib.pyplot as plt
import lxml

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_wheat_production'
df = pandas.read_html(url)
df_zero=df[0]

#plt.close("all")
df_zero.plot(title="FooBar")
plt.show()