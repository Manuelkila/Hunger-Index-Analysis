#Import useful libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#Create Helper functions

def dataExplorer(df):
    """Th functions takes a dataframe object and returns number of empty rows and data type for each colunm.

    Args:
        df (dataframe object): pandas dataframe object

    Returns:
        _type_: pandas dataframe object with two rows:
        first row is the sum of all empty rows in each column
        second row is the data type of the column.
    """
    a = df.isnull().sum()
    b = df.dtypes
    return a,b

def columnRenamer(df, old_name, new_name):
    """the function renames a column in a dataframe

    Args:
        df (dataframe): Dataframe that contains the column to be renamed.
        old_name (string): The old name to be modified.
        new_name (string): The new name.
    """
    df.rename(columns={old_name: new_name}, inplace=True)

def linePlotter(df, x_axis, y_axis, legend, title):
    """This functions plots a line chart

    Args:
        df (ataframe object): _description_
        x_axis (string): Name of the column to be on the x-axis of the line chart.
        y_axis (string): Name of the column on the Y-axis of the line chart.
        legend (string): Name of column whose values serves as legend in the graph.
        title (string): Chart title
    """
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

    for value in df[legend].unique():
        df[df[legend] == value].plot(x=x_axis, y=y_axis, ax=ax, label=value,  linestyle = '-', marker = '*', markersize = 7)
    plt.legend(loc='upper right', fontsize = 8)
    plt.xticks(df[x_axis].unique())
    plt.title(title)
    plt.show()

def boxPlotter(data, x_axis, y_axis,order, hue, title):
    """This function plots a boxplot from a dataframe. 

    Args:
        data (dataframe object): the dataframe object that holds the values to be plotted.
        x_axis (string): Name of the column to be on the x-axis of the Boxplot.
        y_axis (string): Name of the column on the Y-axis of the Boxplot.
        order (String): Name of the column whose values order the boxplots. 
        hue (_type_): _description_
        title (_type_): _description_
    """
    
    fig, ax = plt.subplots(figsize=(14, 7), dpi=100)
    sns.boxplot(data = data, x=x_axis, y= y_axis, order = order, palette='Set3', hue = hue, ax=ax)
    plt.title(title, font = 'Segoe UI', fontsize = 20)
    fig.patch.set_facecolor('ghostwhite')
    ax.patch.set_facecolor('mintcream')
    plt.show()


def barPlotter(data, x_axis, y_axis, color, title, _type):
    """A function that plots a bar chart.

    Args:
        data (dataframe): Dataframe that holds the plot values
        x_axis (string): Name of the column to be on the x-axis of the Bar chart.
        y_axis (string): Name of the column on the Y-axis of the Bar chart.
        color (String): Chart colour.
        title (String): Chart title.
        _type (String): Bar type: barh or bar
    """
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)

    data.plot(kind=_type, x= x_axis, y= y_axis, ax=ax, color = color)
    plt.xticks(rotation=0)
    plt.title(title, font = 'Segoe UI', fontsize = 20)
    if _type == 'barh':
        plt.xlabel(y_axis, fontsize =15)
    else:
        plt.ylabel(y_axis, fontsize = 15)
    ax.get_legend().remove()
    plt.show()
    

def periodClassifier(x):
    """A function that classfies years into five-year intervals.

    Args:
        x (list): The column that holds the years to be classified in the dataframe.

    Returns:
        String: Classification period. 
    """
    if x < 1996:
        return "Before 1996"
    elif (x > 1995 and  x < 2001):
        return "1996-2000"
    elif (x > 2000 and x < 2006):
        return "2001-2005" 
    elif (x > 2005 and x < 2011):
        return "2006-2010"
    elif (x > 2010 and x < 2016):
        return "2011-2015"
    else:
        return "2016-2021"


#read data

hunger_index = pd.read_csv("global-hunger-index.csv")
child_weight = pd.read_csv("share-of-children-underweight.csv")
continent_data = pd.read_csv("countryContinent.csv", encoding='latin-1')

a = [hunger_index, child_weight, continent_data]

for i in a:
    x = i.apply(dataExplorer)
    print("******************")
    print(x)

#rename 'Global Hunger Index (2021)' to 'GHI'
columnRenamer(hunger_index, 'Global Hunger Index (2021)','GHI')

#rename Prevalence of underweight, weight for age (% of children under 5) to Underweight
columnRenamer(child_weight, 'Prevalence of underweight, weight for age (% of children under 5)','Underweight %')

#Select needed columns from continent_mapping
continent_mapping = continent_data[['code_3', 'continent']]

#Join hunger_index with continent_mapping
hunger_index = hunger_index.join(continent_mapping.set_index('code_3'), on='Code', how='left', lsuffix='_left', rsuffix='_right')

#select needed columns from hunger_index
hunger_index = hunger_index[['Entity','Code','Year','GHI','continent']]

#Rename "continent_right" to "continent"
columnRenamer(hunger_index, 'Entity', 'country')

#Rename "continent_right" to "continent"
columnRenamer(hunger_index, 'continent_right', 'continent')

#Calculate average hunger index per continent for each year.
trends_by_continent = hunger_index.groupby(['continent','Year']).mean().reset_index()

#visualise trends_by_continent data
linePlotter(df = trends_by_continent ,y_axis= "GHI",x_axis= "Year",legend="continent", title= "Average Hunger Index Per Continent (2000- 2021)")


#Classify the year column into periods
child_weight["period"] = child_weight['Year'].apply(periodClassifier)


#group child weight into periods
child_trend = child_weight.groupby("period")["Underweight %"].mean().reset_index().sort_values("Underweight %", ascending=True)


#visualise child_trend data
barPlotter(child_trend, 'period','Underweight %', 'navy', 'Percentage of Underweight Children (1983-2021)','bar' )

#Get data for year 2000 and 2021 
change_df = hunger_index[hunger_index['Year'].isin([2000,2021])]

#visualise change_df data
boxPlotter(change_df, "GHI","continent", ['Africa','Oceania','Asia', 'Americas', 'Europe'], "Year", "Global Hunger Index Per Continent")

#Get 2021 data only
data_2021 = hunger_index[hunger_index['Year']==2021]

#Pick the top 20 GHI by value.
top_10 = data_2021.sort_values("GHI", ascending = False).head(10)


#Visualise top_10 data
barPlotter(top_10.sort_values("GHI", ascending = True), "country", "GHI","Navy", "Top 20 Countries with Highest GHI in 2021", 'barh')