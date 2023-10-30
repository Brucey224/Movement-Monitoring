import os
import csv
import datetime
import sqlite3
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename


def Connect(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    return(connection, cursor)

def CreateTables(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS Target_Info (
                    TargetLabel TEXT PRIMARY KEY,
                    X REAL,
                    Y REAL,
                    Z REAL,
                    H_amber REAL,
                    H_red REAL,
                    V_settlement_amber REAL,
                    V_heave_amber REAL,
                    V_settlement_red REAL,
                    V_heave_red REAL
                )""")
    cursor.execute('''CREATE TABLE IF NOT EXISTS Recordings (
                    record_id INT AUTO_INCREMENT PRIMARY KEY,
                    TargetLabel TEXT,
                    Recording_date DATETIME,
                    X_measurement REAL,
                    Y_measurement REAL,
                    Z_measurement REAL,
                    CONSTRAINT unique_target_date UNIQUE (TargetLabel, Recording_date)
                )''')

def Import_missing_records(db_ref, connection, cursor):
    with open(db_ref,'r') as file:
        no_records = 0
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            unique_id = row[0]
            cursor.execute("""SELECT * FROM Target_info WHERE TargetLabel = ?""", (unique_id,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("INSERT INTO Target_Info VALUES (?,?,?,?,?,?,?,?,?,?)", row)
                connection.commit()
                no_records+= 1
    print('\n{} Records Transferred into the database'.format(no_records))

def Create_DB(db_name):
    ## INPUT DATABASE NAME ##
    root =tk.Tk()
    root.withdraw()
    db_ref = askopenfilename(title="Select file containing Target reference information to create database")
    print("selected directory:", db_ref)
    connection, cursor = Connect(db_name)
    CreateTables(cursor)
    Import_missing_records(db_ref, connection, cursor)
    connection.close()
