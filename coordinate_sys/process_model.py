from coordinate_sys.extensions import engine, Dbobj
import pandas as pd
import os, sys

dbo = Dbobj(engine)

# dbo.excel_to_table('jig_records_1205.xlsx', 'jig_records')