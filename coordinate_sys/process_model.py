from coordinate_sys.extensions import engine, Dbobj
import pandas as pd
from coordinate_sys import root_path
import os, sys

dbo = Dbobj(engine)

dbo.excel_to_table('station_1108.xlsx', 'temp_station')
