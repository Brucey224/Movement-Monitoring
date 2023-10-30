import plotly.graph_objects as go
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import plotly
import plotly.express as px

def Connect(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    return connection, cursor

def get_horizontal_vector(coords, readings):
    H1 = coords[:2]
    H2 = readings[:,:2]
    H_vector = 1000*(H2-H1)
    return H_vector

def get_vertical_vector(coords, readings):
    dZ = readings[2] - coords[2]
    return dZ

def get_ref_data(connection, cursor, Target_name):
    query = f"SELECT X, Y, Z, H_amber, H_red, V_settlement_amber, V_settlement_red, V_heave_amber, V_heave_red FROM Target_Info WHERE TargetLabel = ?"
    window = tk.Tk()
    window.withdraw()
    try:
        cursor.execute(query, (Target_name,))
        results = cursor.fetchall()
        if not results:
            raise ValueError("Value not found in the reference database. Check that you have set up origin coordinates and trigger levels")
        x,y,z, H_amber, H_red, V_settlement_amber, V_settlement_red, V_heave_amber, V_heave_red = results[0]
        coords = np.array([x,y,z])
        horizontal_trigger_levels = [H_amber,H_red]
        vertical_trigger_levels = [V_settlement_red, V_settlement_amber, V_heave_amber, V_heave_red]
    except ValueError as e:
        messagebox.showerror("Error: ", str(e))
        connection.close()
    except sqlite3.Error as e:
        errormessage = f"Following error occurred: {e}"
        messagebox.showerror("Check you have created tables in the database", errormessage)
        connection.close()
    return coords, horizontal_trigger_levels, vertical_trigger_levels

def get_movement_readings(connection, cursor, Target_name):
    query = f"SELECT Recording_date, X_measurement, Y_measurement, Z_measurement FROM Recordings WHERE TargetLabel = ?"
    cursor.execute(query, (Target_name,))
    window = tk.Tk()
    window.withdraw()
    try:
        results = cursor.fetchall()
        if results is None:
            raise ValueError("No recorded values found for target")
        dates = [datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S") for result in results]
        readings = np.array([[r[1],r[2],r[3]] for r in results])
    except ValueError as e:
        messagebox.showerror("Error: ", str(e))
    return dates, readings


def plot_H(Target_name, dates, H_vector, horizontal_trigger_levels, construction_start_date):
    fig = go.Figure()
    start_date = min(dates)
    end_date = max(dates)
    x = H_vector [:,0]
    y = H_vector [0:,1]
    data = pd.DataFrame ({'date':dates, 'x':x, 'y':y})
    data['color'] = data['date'].apply(lambda d: 'Before significant construction works' if d<construction_start_date else 'After significant construction works')
    fig = px.scatter(data, x='x', y='y', color='color', color_discrete_map={'Before significant construction works': 'black', 'After significant construction works': 'red'})
    fig.add_shape(type = "circle", xref = "x", yref = "y", x0 = horizontal_trigger_levels[0]*-1, y0 = horizontal_trigger_levels[0]*-1, x1 = horizontal_trigger_levels[0], y1 = horizontal_trigger_levels[0], line_color = "orange")
    fig.add_shape(type = "circle", xref = "x", yref = "y", x0 = horizontal_trigger_levels[1]*-1, y0 = horizontal_trigger_levels[1]*-1, x1 = horizontal_trigger_levels[1], y1 = horizontal_trigger_levels[1], line_color = "red")
    fig.update_layout(title=go.layout.Title(text = Target_name +"<br><sup>Trigger Levels[Amber, Red] = " + str(horizontal_trigger_levels) +"<sup>"))
    fig.update_yaxes(scaleanchor="x",    scaleratio=1 )
    plotly.offline.plot(fig, filename = f"{Target_name} - horizontal movements.html")    
    return fig, data

def plot_horizontal_movements(Target_name, db_name, construction_start_date):
    connection, cursor = Connect(db_name)
    coords, horizontal_trigger_levels, vertical_trigger_levels = get_ref_data(connection, cursor, Target_name)
    dates, readings = get_movement_readings(connection, cursor, Target_name)
    H_vector = get_horizontal_vector(coords, readings)
    plot_H(Target_name, dates, H_vector, horizontal_trigger_levels, construction_start_date)
    connection.close()

def plot_vertical_movements(Target_name, db_name, construction_start_date):
    pass


