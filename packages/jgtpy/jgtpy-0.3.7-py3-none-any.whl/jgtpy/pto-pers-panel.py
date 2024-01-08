#%% Imp.orts
import os
#@URIR B:\Dropbox\jgt\drop\rl_comet_jgt_chart03.py


import plotly.graph_objects as go
from plotly.subplots import make_subplots
import panel as pn


import pandas as pd
from jgtpy import JGTADS as ads,adshelper as ah
import tlid
#@STCGoal An online Platform to View charting



#%% The Experiment
i="SPX500"
i="EUR/USD"
i="AUD/USD"

experiment_name = "Perspective_" + i.replace("/","-") 

#%% Print current working directory
print(os.getcwd())

#%% Load Many POV

timeframes = ["M1","W1","D1","H4", "H1","m15","m5"]
#timeframes = ["D1","H4", "H1"]
figures = {}

for t in timeframes:
  fnamebase = i.replace("/","-") + "_" + t
  fname = fnamebase + ".csv"
  # try: 
  #   DATA_ROOT = os.getenv("JGTPY_DATA")
  # except:
  DATA_ROOT = "../data"
  #if not exists(DATA_ROOT), use ../../data
  if not os.path.exists(DATA_ROOT):
    DATA_ROOT = "../../data"
  print(DATA_ROOT)
  fpath = DATA_ROOT + "/cds/" + fname
  data = pd.read_csv(fpath,index_col=0,parse_dates=True)
  # Plot some data expecting to see them in the experiment
  f,ax = ads.plot_from_cds_df(data,i,t,show=False)
  f.title= t
  figures[t] = f
  

#%% TABS




# Create a tabbed layout
tabs = pn.Tabs()

# Add a tab for each timeframe
for t in timeframes:
  tabs.append(figures[t])
  
  #tabs[int(t[-2:])] = figures[t]
html_fname = i.replace("/","-") + ".html"
html_output_path = "pto-pers-" + html_fname



tabs.save(html_output_path,embed=True)

#%% Pryint HTML
print(html_output_path)
# with open(html_output_path, 'r') as file:
#   html_content = file.read()

# experiment.log_asset(html_output_path)
# experiment.log_html(f'<a href="{html_fname}">OPEN TABS</a> - <a href=others/"{html_fname}">OPEN TABS2</a> - ')
#experiment.log_html(html_output_path)
# Display the tabs
#tabs.show()

# %%
pn.extension()
tabs
# %%
