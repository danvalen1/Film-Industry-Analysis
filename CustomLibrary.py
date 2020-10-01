# Standard libraries to import
def import_libs():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    

# Setting standard style
def set_style():
    pass

# Converting columns in a dataframe that have string dollar amounts to ints    
def clean_dollars(dataframe, column_str):
    dataframe[column_str] = dataframe[column_str].str.replace(',', '').str.replace('$', '').astype(int)
    return dataframe

# Parses out a column of strings into indicator variables
def indicator_str_parser(dataframe, parsed_column_str, list_of_strs):
    
    # If column full of strings has no string to be parsed, set value to 'none'
    dataframe[dataframe[parsed_column_str].isnull()] = "none"
    
    # Create indicator columns for columns with no string to be parsed
    dataframe[parsed_column_str + '_not_parsed_id'] = [1 if x == "none"
                                                       else 0 
                                                       for x in dataframe[parsed_column_str]]
    
    
    
    # starts list of created series to be used as arguments
    list_of_series = []
    
    # Loop over elements in list
    for string in list_of_strs:
        
        # Make a new indicator column from the parsed column adn the element to be searched for
        dataframe[parsed_column_str + '_' + string + '_id'] = [1 if string in x 
                                                            else 0 
                                                            for x in dataframe[parsed_column_str]]
        
        # Include new column in list to be fed into function
        list_of_series.append(dataframe[parsed_column_str + '_' + string + '_id'])
        
    # Unpack list_of_series to be fed as arguments into zip function for unique tuples
    dataframe[parsed_column_str + '_tuple'] = list(zip(*list_of_series))
    
    # Indicate the number of parsed out strings
    dataframe[parsed_column_str + '_num_of_parses'] = [sum(list(x)) for x in dataframe[parsed_column_str + '_tuple']]
    
    # return dataframe for quick view/analysis
    return dataframe

def prep_Data(DataFrame1, DataFrame2):
    # We first need to match the column names for the movie titles to be able to join the two dataframes
    df_title_movie = DataFrame1.rename(columns = {'primary_title':'movie'})
    
    # Second: create a colum for start year as an integer type. This allows us join the dataframes by
    # the year of production so that we don't have errors with possible remakes.
    DataFrame2['start_year']= [int(x[-4:]) for x in DataFrame2['release_date']]
    
    # Third: merge the datasets on 'movie' and 'start_year'
    df_budget_merge = pd.merge(DataFrame2, df_title_movie, how ='inner', on = ('movie', 'start_year'))

def clean_Data(DataFrame):
    # Find any duplicates in the dataframe
    df_duplicates = DataFrame[DataFrame['movie'].duplicated()]
    
    # Drop the duplicates from the dataframe
    DataFrame.drop(df_duplicates.index, axis = 0, inplace = True)
    
    # Check for placeholder values by finding where worldwide_gross = '$0'
    df_no_values = DataFrame.loc[DataFrame['worldwide_gross'] == '$0']
    
    # Drop the placeholder values from the dataframe
    DataFrame.drop(df_no_values.index, axis = 0, inplace = True)
    
    # Change the number values represented by dtype String with dtype integers. Use clean_dollars function
    clean_dollars(DataFrame, 'production_budget')
    clean_dollars(DataFrame, 'domestic_gross')
    clean_dollars(DataFrame, 'worldwide_gross')
    
    # Create a new column for advertisement budget by using the production_budget column
    # Uses assumption that advertisement costs will generally cost the same as production
    DataFrame['advertisement_budget'] = DataFrame['production_budget']
    
    # Create a total costs column by adding the advertisement budget and the production budget
    df_budget_merge['total_costs'] = df_budget_merge['production_budget'] + df_budget_merge['advertisement_budget']
    
    # Create a profit column by taking the difference between the 'worldwide_gross' and 'total_costs' column
    DataFrame['profit'] = DataFrame['worldwide_gross'] - DataFrame['total_costs']
    
    # Sort the values by 'profit'
    DataFrame.sort_values(by = ['profit'], axis = 0, ascending = False, inplace = True)
    
    # Create a Return on Investment (ROI) percentage column by dividing profit and total costs multiplied by 100
    DataFrame['ROI'] = DataFrame['profit'] / DataFrame('total_costs') * 100
    
    # Seperate the different genres by using the indicator_str_parser function
    indicator_str_parser(df_budget_merge, 
                         'genres', 
                         ['Action', 'Adventure', 'Comedy', 'Drama', 'Family', 'Thriller', 'Documentary']
                        )
    

def Low_Budget_Genres(DataFrame):
    
    # Create a list for rows of data
    r = []
    
    # Iterate through desired genres
    for x in ['Action', 'Adventure', 'Comedy', 'Documentary', 'Drama', 'Family', 'Thriller']:
        
        # Append  a list of [ROI, Genre] as a row to your list of rows. ROI should be for low budget films only
        r.append([DataFrame.loc[(DataFrame[f'genres_{x}_id'] == 1) & 
                                (DataFrame['total_costs'] < 25000000)].ROI.median(), x])
        
    # Create a new DataFrame for your list of rows with columns of Median ROI and Genre
    new_dF = pd.DataFrame(r, columns = ('Median ROI', 'Genre'))
    
    # Return your new DataFrame
    return new_dF
 
def Mid_Budget_Genres(DataFrame):
    
    # Create a list for rows of data
    r = []
    
    # Iterate through desired genres
    for x in ['Action', 'Adventure', 'Comedy', 'Documentary', 'Drama', 'Family', 'Thriller']:
        
        # Append  a list of [ROI, Genre] as a row to your list of rows. ROI should be for mid budget films only
        r.append([DataFrame.loc[(DataFrame[f'genres_{x}_id'] == 1) & 
                                (DataFrame['total_costs'] >= 25000000) & 
                                (DataFrame['total_costs'] < 100000000)].ROI.median(), x])
        
    # Create a new DataFrame for your list of rows with columns of Median ROI and Genre
    new_dF = pd.DataFrame(r, columns = ('Median ROI', 'Genre'))
    
    # Return your new DataFrame
    return new_dF

def High_Budget_Genres(DataFrame):
    
    # Create a list for rows of data
    r = []
    
    # Iterate through desired genres
    for x in ['Action', 'Adventure', 'Comedy', 'Documentary', 'Drama', 'Family', 'Thriller']:
        
        # Append  a list of [ROI, Genre] as a row to your list of rows. ROI should be for high budget films only
        r.append([DataFrame.loc[(DataFrame[f'genres_{x}_id'] == 1) & 
                                (DataFrame['total_costs'] > 100000000)].ROI.median(), x])
        
    # Create a new DataFrame for your list of rows with columns of Median ROI and Genre
    new_dF = pd.DataFrame(r, columns = ('Median ROI', 'Genre'))
    
    # Return your new DataFrame
    return new_dF

def LB_Genres_Graph(DataFrame):
    
    # Create a figure
    fig = plt.figure(figsize= (20, 16))
    
    # Use sns.barplot with 'Genre' on the x axis and 'Median ROI' on the y axis. Give it a unique color
    ax = sns.barplot(data = DataFrame, x = 'Genre', y = 'Median ROI', color = 'lightblue')
    
    # Give the graph a title and lables
    ax.set(title = 'Median ROI for Low Budget Films by Genre', xlabel = 'Genres', ylabel = 'Return on Investment')
    
    # Change the xticks so that the tick labels are not on each other
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 45, horizontalalignment = 'right')
    
    # Change the yticks so that the labels are in %
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    
    # return the graph
    return plt.show()

def MB_Genres_Graph(DataFrame):
    # Create a figure
    fig = plt.figure(figsize= (20, 16))
    
    # Use sns.barplot with 'Genre' on the x axis and 'Median ROI' on the y axis. Give it a unique color
    ax = sns.barplot(data = DataFrame, x = 'Genre', y = 'Median ROI', color = 'steelblue')
    
    # Give the graph a title and lables
    ax.set(title = 'Median ROI for Mid Bidget Films by Genre', xlabel = 'Genres', ylabel = 'Return on Investment')
    
    # Change the xticks so that the tick labels are not on each other
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 45, horizontalalignment = 'right')
    
    
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    
    # return the graph
    return plt.show()

def HB_Genres_Graph(DataFrame):
    
    # Create a figure
    fig = plt.figure(figsize= (20, 16))
    
    # Use sns.barplot with 'Genre' on the x axis and 'Median ROI' on the y axis. Give it a unique color
    ax = sns.barplot(data = DataFrame, x = 'Genre', y = 'Median ROI', color = 'blue')
    
    # Give the graph a title and lables
    ax.set(title = 'Median ROI for High Budget Film by Genre', xlabel = 'Genres', ylabel = 'Return on Investment')
    
    # Change the xticks so that the tick labels are not on each other
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 45, horizontalalignment = 'right')
    
    # Change the yticks so that the labels are in %
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    
    # return the figure
    return plt.show()

    
    