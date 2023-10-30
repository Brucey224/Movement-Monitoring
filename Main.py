from Create_DB import Create_DB
from Import_readings import Import_readings
from Plot_from_DB import plot_horizontal_movements

from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
import os


window = tk.Tk()
window.withdraw()

# Database named by default
db_name = "Targets.db"

## PRELIMINARIES - GET INPUT FROM USER
Target_name = simpledialog.askstring("Input", "Target to query")
construction_start_date = datetime(2023,4,1)
# create the database containing reference data: includes:
#                           - Target Labels 
#                           - reference coords
#                           - trigger levels  
window.quit()                                                    

## 1. Create Database thaSOt includes all reference info for Targets (origin & Trigger levels)
Create_DB(db_name)

# 2. Import all movement readings for dates that have not yet been input into database
Import_readings(db_name)

# 3. Plot Horizontal movements using plotly
plot_horizontal_movements(Target_name, db_name, construction_start_date)

