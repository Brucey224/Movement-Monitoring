import plotly.graph_objects as go
import sqlite3
import os
import csv
import numpy as np
import datetime
from tkinter import filedialog

def Connect(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    return(connection, cursor)

def translate_dates(file_name):
    year=int(file_name[0:4])
    month = int(file_name[4:6])
    day = int(file_name[6:8])
    hour = int(file_name[-4:-2])
    minute = int(file_name[-2:])
    date = datetime.datetime(year,month,day,hour,minute)
    return date

def get_records_folder():
    path = filedialog.askdirectory()
    if path:
        print("selected folder path:", path)
    else:
        print("no folder")
    return path

def scan_files(path, connection, cursor):
    files=0
    for file in os.listdir(path):
        file_name,file_ext = os.path.splitext(file)
        if file_ext == '.csv':
            files+=1
            data_import(path, file, connection, cursor)
    return files
            
def data_import(path, file, connection, cursor):
    insert_query = """
    INSERT OR IGNORE INTO Recordings (TargetLabel, Recording_date, X_measurement, Y_measurement, Z_measurement)
    VALUES (?, ?, ?, ?, ?)
    """
    with open(os.path.join(path,file), 'r') as f:
        reader = csv.reader(f)
        next(reader)
        file_name,file_ext = os.path.splitext(file)
        date = translate_dates(file_name)
        for row in reader:
            try:
                valid_row = [str(row[0]), float(row[1]), float(row[2]), float(row[3])]
            except (ValueError, IndexError):
                continue
            cursor.execute(insert_query, [row[0],date] + row[1:4])
            connection.commit()

def Import_readings(db_name):
    connection, cursor = Connect(db_name)
    path = get_records_folder()
    files = scan_files(path, connection, cursor)
    print('\n{} Files scanned for import into database'.format(files))
    connection.close()

