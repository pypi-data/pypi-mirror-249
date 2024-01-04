#Import Modules
import pandas as pd
from os.path import exists
from os import listdir, getenv
from datetime import datetime
from sqlalchemy import create_engine, text, types

#Custom Modules
import ncl_sqlsnippets as snips

#Init process
def initialise (output):
    #Does collate file exist?
    if not exists("./collate.csv"):

        #If not then create blank df with columns and export to csv
        pd.DataFrame(columns=output["columns"]).to_csv("./collate.csv", index=False)

    #Does the history file exist?
    if not exists("./history.csv"):

        #If not then create blank df with context columns and export to csv
        pd.DataFrame(columns=["Filename", "Date Added"]).to_csv("./history.csv", index=False)

#Get all files (not collate) in the directory
def get_loose_files(settings, suffix=".csv"):

    #Get a list of all files in the directory
    filenames = listdir(settings["PATH_PREFIX"])
    
    #Return all csv files that are not the collate file or the history file
    return [ filename for filename in filenames if (filename.endswith( suffix ) 
                                                    and filename != "collate.csv"
                                                    and filename != "history.csv")]

#Get all files listed in the history file
def get_history_files():

    #Load history csv
    history_files = pd.read_csv("./history.csv", index_col=False)

    #Return array of files
    return history_files['Filename'].array

#Derive new files
def derrive_missing_files(loose_array, history_array):

    #Get difference between both arrays
    new_files =  list(set(loose_array) - set(history_array))
    new_files.sort()

    return new_files

#For the "all" method the history and collate files need to be reset to remove no longer relevant data
def refresh_history(output):

    #Overwrite any existing collate file
    pd.DataFrame(columns=output["columns"]).to_csv("./collate.csv", index=False)
    
    #Overwrite any existing history file
    pd.DataFrame(columns=["Filename", "Date Added"]).to_csv("./history.csv", index=False)

#Get list of loose files
def get_new_files (output, settings):

    #Get array of loose files
    loose_files = get_loose_files(settings)

    if settings["METHOD"] == "memory":

        #Get a array of history files
        history_files = get_history_files()

        #Derive all files that exist in the loose files that are not in the history files
        return derrive_missing_files(loose_files, history_files)
    
    elif settings["METHOD"] == "all":

        refresh_history(output)

        return loose_files

    raise Exception ("No valid method specified")    

#Logic for if the data should be uploaded to SQL
def get_upload_bool(settings, change):

    #Variable for upload setting
    mode = settings["SQL_UPLOAD"]

    #always upload
    if mode == "always":
        print("Uploading to sql")
        return True

    #Upload if a change has occured
    if mode == "on change":
        if change == True:
            print("A change has occured")
            return True
        else:
            print("No change has occured")
            return False

    #Never upload
    if mode == "never":
        return False

#Convert columns into date format (for SQL to recognise the date conversion)
def col_conversion(data, output, format_date="%Y-%m-%d", format_datetime="%Y-%m-%dT%H:%M:%S"):

    #Data types defined in output
    dtypes = output["dtypes"]

    #If dateformats were specified
    if "dateformats" in output:
        dateformats = output["dateformats"]

    #For each type named in dtypes
    for dtype in dtypes:

        #Date type
        if (type(dtypes[dtype]) == type(types.Date)):

            #Check if custom  dateformat was specified (otherwise use default)
            if "dateformats" in output:
                if dtype in output["dateformats"]:
                    data[dtype] = pd.to_datetime(data[dtype], format=dateformats[dtype])
                else:
                    data[dtype] = pd.to_datetime(data[dtype], format=format_date)
            else:
                data[dtype] = pd.to_datetime(data[dtype], format=format_date)
        
        #DateTime type
        elif (type(dtypes[dtype]) == type(types.DateTime)):

            #Check if custom  dateformat was specified (otherwise use default)
            if "dateformats" in output:
                if dtype in output["dateformats"]:
                    data[dtype] = pd.to_datetime(data[dtype], format=dateformats[dtype])
                else:
                    data[dtype] = pd.to_datetime(data[dtype], format=format_datetime)
            else:
                data[dtype] = pd.to_datetime(data[dtype], format=format_datetime)

    return data

#Check the output columns exists in the target table before replacing data
def replace_safety_check(engine, output, settings):

    #Get columns that are declared in the output columns that do not exist in the target table
    exception_columns = snips.columns_exist(engine, settings["SQL_TABLE"], settings["SQL_SCHEMA"], output["columns"])

    if exception_columns:
        raise Exception (f"""Uploaded halted as these columns are not found in the target table: {exception_columns}. 
           Please drop the table [{settings["SQL_SCHEMA"]}].[{settings["SQL_TABLE"]}] before attempting to replace the data with data of a different column structure""")

#Main function for updating the collate table
def upload_collate (append_data, output, settings):

    #table, schema, database, append_data, output, settings

    #Get connection string
    conn_str = snips.get_connection_string (settings["SQL_ADDRESS"], settings["SQL_DATABASE"])

    #Create engine
    engine = snips.connect_to_sql(conn_str)

    if settings["SQL_REPLACE"] == True:

        #If replace is True then we want to reupload the whole dataset so use the collate file
        data = pd.read_csv("./collate.csv")


        #Check if the table to be replaced already exists
        if snips.table_exists(engine, settings["SQL_TABLE"], settings["SQL_SCHEMA"]):
            #Check the columns match the data being replaced or force the table to be dropped first 
            #(Safety feature to prevent blindly overwriting unrelated tables)
            replace_safety_check(engine, output, settings)

    else:
        #If replace is False then only use the new data
        data = append_data

    #Convert columns to types specified in the mapping variable "output["dtypes"]"
    #This is mostly to make sure dates are in a recognisible format to the MSSQL server
    data = col_conversion(data, output)

    #Upload data
    snips.upload_to_sql(data, engine, settings["SQL_TABLE"], settings["SQL_SCHEMA"], settings["SQL_REPLACE"], settings["SQL_CHUNKSIZE"], output["dtypes"])

#Return the map group for the file
def get_map_group(file, mapping, settings):
    #For each item in the group mapping
    for key, val in mapping["groups"].items():
        #If the data point is matched to this key
        if file in val:
            #Return that key
            return mapping["columns"][key]
        
    #Key not found so use the default
    return mapping["columns"][settings["DEFAULT_MAP"]]

#Map the data to the output columns  
def map_data(data, file_map):

    #For each column in the data
    for col in data.columns:

        try:
            mapped_value = file_map[col]
        except:
            raise Exception(f"The file map does not contain {col} column. File map: {file_map}")

        if mapped_value is None:
            #If no mapping then remove
            data = data.drop(columns=[col])
        else:
            #If mapping exists then rename
            data = data.rename(columns={col:file_map[col]})

    return data

#Add a data label to the data
def add_data_label(data, filename, col_input, output, settings):

    #Get label from settings
    label = settings["LABEL_DATA"]

    #Check to make sure the label is mentioned in the output["columns"] variable
    if label not in output["columns"]:
        print(f"WARNING: The label column '{label}' is not specified in the output columns and will not appear in the output.")

    #Check to make sure the label is NOT mentioned in the mapping["columns"] dict
    for key, item in col_input.items():
        if label == item:
            print(f"WARNING: The label column '{label}' already mapped to another column in the source data and will overwrite existing data.")

    #Add a column with the given label name that has the value of the filename (minus extension)
    data[label] = filename

    return data

#Filter data
def filter_data(df, output):

    df_f = df
    
    #Check if filters were specified
    if output.get("filters"):

        #Get the filter dictionary
        filters = output["filters"]

        #For each column with a filter
        for key in filters:

            #Filter the data
            df_f = df_f[df_f[key].isin(filters[key])]

    #Return the filtered data
    return df_f

#Process file
def process_file(file, output, mapping, settings):

    filename = file.split('.csv')[0]

    #Get data from the target file
    data = pd.read_csv(settings["PATH_PREFIX"] + file)

    #Get the column map
    column_map = get_map_group(filename, mapping, settings)

    #Map the columns
    mapped_data = map_data(data, column_map)

    #Filter the data
    mapped_data = filter_data(mapped_data, output)

    #Declare a blank df with output columns
    df_schema = pd.DataFrame(columns=output["columns"])

    #Concat the mapped data to a blank df to ensure mapped data has the right number of columns
    mapped_data = pd.concat([df_schema, mapped_data])

    #Add the data label column if specified
    if settings["LABEL_DATA"]:
        mapped_data = add_data_label(mapped_data, filename, column_map, output, settings)

    return mapped_data

#Append the data
def append_data(data):
    data.to_csv("./collate.csv", index=False, mode = 'a', header=0)

#Update history file
def update_history(filename):
    entry = pd.DataFrame({
        "Filename": [filename],
        "Date Added": [datetime.now().strftime('%d/%m/%Y')] 
    })

    entry.to_csv("./history.csv", index=False, mode = 'a', header=0)

#Main function
def main (output, mapping, settings):
    #Initialise the collate and history files
    initialise(output)

    #Get new files to add to the collate file
    new_files = get_new_files(output, settings)

    #Declare variable to track if a change been made
    change = False

    #Data frame for new data (for append mode)
    new_data = pd.DataFrame(columns=output["columns"])

    #For each new file
    for nf in new_files:

        #Debug
        print(f"New file: {nf}")

        #Get the data from that file mapped to the outputs
        mapped_data = process_file(nf, output, mapping, settings)

        #Append this data to the collate file
        append_data(mapped_data)

        #Update the history file
        update_history(nf)

        #Note a change has occured
        change = True

        #If set to append (SQL_REPLACE == False) then maintain dataframe of new data. Not needed if replacing SQL table with collate file or not uploading to SQL
        if (settings["SQL_REPLACE"] == False) and (settings["SQL_UPLOAD"] != "never"):
            new_data = pd.concat([new_data, mapped_data])

    #SQL Upload code

    #Determine if the upload should happen
    if get_upload_bool(settings, change):

        #Upload the current collate file
        upload_collate(new_data, output, settings)