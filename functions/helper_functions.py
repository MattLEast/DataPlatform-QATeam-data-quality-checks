import glob
import  os
import json, re
import bson
import datetime
from datetime import datetime, timedelta
import pandas as pd
import tkinter
from tkinter import filedialog
import gzip
from pathlib import Path
import base64

class Filelister:
    def __init__(self, path):
        self.path = path

    def list_files(self):
        files = os.listdir(self.path)
        #files = sorted(files, key=lambda x: int(x.split('_')[0]))
        files = sorted(files, key=lambda x: int(x.split('_')[0]) if x.split('_')[0].isdigit() else float('inf'))

        return files


def extract_values(obj, prefix=''):
    """Extracts values from nested dictionaries and lists"""
    values = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{prefix}.{key}" if prefix else key
            values.update(extract_values(value, new_key))
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            new_key = f"{prefix}[{index}]"
            values.update(extract_values(item, new_key))
    else:
        values[prefix] = obj
    return values


def count_events(events, count):
    for item in events:
        if isinstance(item, dict):
            count += 1
    return(count)

#def make_event_dataframe()

def sorted_files(directory: str, extension: str):
    """
    Given a full directory path and filename extension, returns a sorted list of all the files in that directory with
    the specified extension. Sorting is based on first part of filename, delimited by '_' and treated as an integer
    value.

    :param directory: full path to directory
    :param extension: extension of files to consider from that directory
    :return: a list of full path filenames of files in specified directory with specified extension, sorted by index.
    """

    # filenames like: 9087_00-50-06-422000.basketball.pose.complete
    # we require the 9087 as a numeric value for sorting, numeric so 9 is followed by 10 etc
    def sort_criteria(item):

        if extension == "bson" or extension == "json" or extension == "output" or extension == "xml":
            key = os.path.basename(item).partition('.')[0]
            return int(key)
        else:
            key = os.path.basename(item).partition('_')[0]
            return int(key)

    return sorted(glob.glob(directory + '\\*.' + extension), key=sort_criteria)

# Read json files as file or jlines
class JsonReader:

    def __init__(self, filename):
        self.filename = filename

    def read_json(self):
        with open(self.filename, 'r') as f:
            try:
                data = json.load(f)
                return data
            except:
                return False

    def read_lines(self):
        self.dataList = []
        with open(self.filename, 'r') as f:
            try:
                #data = json.loads(f)

                for item in f:
                    try:
                        dataDict = json.loads(item)
                        self.dataList.append(dataDict)
                    except:
                        pass
                return self.dataList
            except:
                return False

class BsonReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, 'rb') as f:
            bson_data = f.read()

        return bson.decode_all(bson_data) #bson.decode_all()

def count_events(events, count):
    for item in events:
        if isinstance(item, dict):
            count += 1
    return(count)


def hawkTime(givenTime):
    try:
        given_datetime = datetime.strptime(givenTime, '%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        given_datetime = datetime.strptime(givenTime, '%Y-%m-%dT%H:%M:%SZ')
    reference_time = datetime(2000, 1, 1)
    microseconds_since_2000 = int((given_datetime - reference_time).total_seconds() * 1_000_000)
    return microseconds_since_2000


def append_cleaned_dicts_to_dataframe(data_dict, existing_df):
    """
    Appends a dictionary to a DataFrame after cleaning null values.

    Args:
        data_dict (dict): A dictionary containing data to be appended.
        existing_df (pd.DataFrame): Existing DataFrame to append data to.

    Returns:
        pd.DataFrame: Updated DataFrame with the cleaned dictionary appended.
    """
    # Ensure the DataFrame is initialized properly if empty
    if existing_df.empty:
        # If the DataFrame is empty, determine columns dynamically from the dictionary
        columns = list(data_dict.keys())
        existing_df = pd.DataFrame(columns=columns)

    # Drop null values from the dictionary
    cleaned_data = {k: v for k, v in data_dict.items() if v is not None}

    # Append the cleaned dictionary to the DataFrame
    if cleaned_data:
        existing_df = pd.concat([existing_df, pd.DataFrame([cleaned_data])], ignore_index=True)

    return existing_df


def selectGame(file=None):
    root = tkinter.Tk()
    root.withdraw()
    if file == "file":
        base_path = filedialog.askopenfilename(title="Select a file")
    else:
        base_path = filedialog.askdirectory(title="Select a file")

    if base_path:
        print(base_path)
    else:
        print("No file selected")
    return base_path






