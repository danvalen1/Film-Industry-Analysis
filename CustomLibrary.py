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
