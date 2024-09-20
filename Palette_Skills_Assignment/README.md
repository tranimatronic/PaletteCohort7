# Palette Skills Assignment Repository

The assignment notebook ('Stream_3_Assignment.ipynb') can be found inside directory 'Assignment_Notebook'. Assignment summary below:

# Tasks
1. Create a geographic data visualization that shows the average wheat production by country for the years 2020 to 2022 (30% of assignment grade)
   
2. Create a geographic data visualization that shows world population by country (30% of assignment grade)
   
3. Create a geographic data visualization that shows 2022 wheat production per 1 million people by country (40% of assignment grade)

# Datasets

A) List of countries by wheat production https://en.wikipedia.org/wiki/List_of_countries_by_wheat_production
  
B) List of countries and dependencies by population https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population
  
C) World Countries Generalized (general boundaries for countries of the world) https://hub.arcgis.com/datasets/esri::world-countries-generalized/explore

# Hints and Tips

- Datasets A and B have tables that can be read directly into a pandas dataframe using the following command: `pd.read_html(url)[0]`.

- Dataset C contains the geometry coordinates for geopandas plots. Download the file as a geojson and read it using the following command `gpd.read_file(geojson_file_path).rename(columns={'COUNTRY': 'Country'})`.

- Merge dataframes based on the country name. Ensure that the countries have the same name and can be merged together. You can use the following command: `pd.merge(df1, df2, on='Country', how='inner')`.

- Feel free to DM me (Alex D'Ippolito) on Slack if you have questions.

# Assignment Submission

- Create your own repository on github with your completed assignment and DM me the link

- Assignment is due by end of day on October 7, 2024
