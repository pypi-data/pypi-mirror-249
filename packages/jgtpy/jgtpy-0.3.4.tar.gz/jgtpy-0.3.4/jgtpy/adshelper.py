

#@STCGoal Aim to become the container for lighting JGTADS

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import JGTPDSP as pds
import JGTIDS as ids
import JGTCDS as cds
import jgtwslhelper as wsl
import pandas as pd

from JGTChartConfig import JGTChartConfig

import logging
_loglevel= logging.WARNING

# Create a logger object
l = logging.getLogger()
l.setLevel(_loglevel)

# Create a console handler and set its level
console_handler = logging.StreamHandler()
console_handler.setLevel(_loglevel)

# Create a formatter and add it to the console handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
l.addHandler(console_handler)



def read_csv(csv_fn):
    df=pd.read_csv(csv_fn)
    # try:
    #     df.set_index('Date', inplace=True)
    # except:
    #     pass
    try:
        df.drop(columns=['Unnamed: 0'],inplace=True)
    except:
        pass
    return df

#IN_CHART_BARS=300

def prepare_cds_for_ads_data(instrument, timeframe,tlid_range=None,cc: JGTChartConfig=None):
    """
    Prepare CDS (Credit Default Swap) data for ADS (Automated Trading System).

    Args:
        instrument (str): The instrument symbol.
        timeframe (str): The timeframe of the data.
        tlid_range (str, optional): The range of TLID to select. Defaults to None.
        cc (JGTChartConfig, optional): The chart configuration. Defaults to None.

    Returns:
        pandas.DataFrame: The prepared CDS data with Selected number of bars

    """
    if cc is None:
        cc = JGTChartConfig()
        
    #@STCIssue Deprecating this value for later 
    
    
    if tlid_range is not None:
        raise NotImplementedError("tlid_range is not implemented yet.")
    #@STCGoal local retrieve data from cache if available or from WSL if not  (jgtfxcli)
        
    cache_data=False
    cache_dir = "cache"
    if cache_data:
        os.makedirs(cache_dir, exist_ok=True)

    fn =  instrument.replace("/", "-") + "_" + timeframe + ".csv"
    fnpath = os.path.join(cache_dir,fn)
    l.info("fnpath:"+ fnpath)


    try:
        df = pds.getPH(instrument,timeframe,cc=cc)
        #print("pds df:",str(len(df))+" rows")
    except:
        l.warning("Could not get DF, trying to run thru WSL the update")
        wsl.jgtfxcli(instrument, timeframe, cc.nb_bar_to_retrieve)
        df = pds.getPH(instrument,timeframe,cc.nb_bar_to_retrieve) #@STCIssue Limitation of full range to be given yo jgtfxcli
    # Select the last 400 bars of the data
    try:#@q Is the selected correspond to desirrd bars ?
        #Make sure we have enough bars to select
        nb_to_select = cc.nb_bar_to_retrieve
        if nb_to_select < cc.min_bar_on_chart:
            nb_to_select = cc.min_bar_on_chart
            selected = df.copy()
        else:
            selected = df.iloc[-nb_to_select:].copy()
        
        #selected.to_csv("output_ads_prep_data.csv")
    except:
        l.warning("Could not get DF, trying to run thru WSL the update")
        wsl.jgtfxcli(instrument, timeframe, cc.nb_bar_to_retrieve)
        try:
            df = pds.getPH(instrument,timeframe,cc.nb_bar_to_retrieve)
            selected = df.copy()
        except:
            l.warning("Twice :(Could not select the desired amount of bars, trying anyway with what we have")
            pass
        l.warning("Could not select the desired amount of bars, trying anyway with what we have")
        pass
    #print(selected)
    #len_selected = len(selected)
    data = cds.createFromDF(selected)
    if cache_data:
        data.to_csv(fnpath)
        
    nb_bars = len(data)
    #print("AH:Debug: nb_bar_on_chart:",nb_bar_on_chart)
    #print("AH:Debug:nb_bars b4 prep ends well:",nb_bars)
    if nb_bars> cc.nb_bar_on_chart:
        r = data.iloc[-cc.nb_bar_on_chart:].copy()
    else:
        r= data
    #len_r = len(r)
    #print("AH:Debug:nb_bars after prep ends well:",len_r)
    return r


def get(instrument,timeframe,nb_bar_on_chart=500):
  data = prepare_cds_for_ads_data(instrument, timeframe, nb_bar_on_chart)
  return data
#p=pds.getPH(instrument,timeframe)
