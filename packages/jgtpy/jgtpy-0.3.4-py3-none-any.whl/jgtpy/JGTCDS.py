# %%

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

#import jgtfxcon.JGTPDS as pds
import JGTIDS as ids
import JGTPDSP as pds
from jgtos import get_data_path
from JGTChartConfig import JGTChartConfig
#from . import jgtconstants
#.columns_to_remove as columns_to_remove

import pandas as pd


import jgtconstants as c


# %%
def createFromPDSFileToCDSFile(instrument, timeframe, columns_to_remove=None, quiet=True,tlid_range=None):
  """
  Create a CDS file from a PDS file.

  Parameters:
  - instrument (str): The instrument name.
  - timeframe (str): The timeframe of the data.
  - columns_to_remove (list, optional): List of column names to remove from the CDS file. Default is None.
  - quiet (bool, optional): If True, suppresses the output. Default is True.
  - tlid_range (str, optional): The TLID range to retrieve. Default is None.

  Returns:
  - fpath (str): The file path of the created CDS file.
  - c (DataFrame): The DataFrame containing the data.

  """
  cdf = createFromPDSFile(instrument, timeframe, quiet,tlid_range=tlid_range)

  # Remove the specified columns
  if columns_to_remove is not None:
    cdf = cdf.drop(columns=columns_to_remove, errors='ignore')

  # # Reset the index
  # try:
  #   c.reset_index(inplace=True)
  # except:
  #   pass

  # Define the file path based on the environment variable or local path
  data_path_cds = get_data_path("cds")
  fpath = pds.mk_fullpath(instrument, timeframe, 'csv', data_path_cds)
  #print(fpath)
  cdf.to_csv(fpath)

  return fpath, cdf

def readCDSFile(instrument, timeframe, columns_to_remove=None, quiet=True):
  """
  Read a CDS file and return a pandas DataFrame.

  Parameters:
  instrument (str): The instrument name.
  timeframe (str): The timeframe of the data.
  columns_to_remove (list, optional): List of column names to remove from the DataFrame. Default is None.
  quiet (bool, optional): If True, suppresses the output messages. Default is True.

  Returns:
  pandas.DataFrame: The DataFrame containing the CDS data.
  """
  # Define the file path based on the environment variable or local path
  data_path_cds = get_data_path()
  fpath = pds.mk_fullpath(instrument, timeframe, 'csv', data_path_cds)
  cdf = pd.read_csv(fpath)

  # Set 'Date' as the index
  cdf.set_index('Date', inplace=True)
  # Remove the specified columns
  if columns_to_remove is not None:
    cdf = cdf.drop(columns=columns_to_remove, errors='ignore')
  return cdf

def createFromPDSFile(instrument,timeframe,quiet=True,tlid_range=None,cc: JGTChartConfig = None):
  """Create CDS (Chaos Data Service) with Fresh Data on the filestore

  Args:
      instrument (str): symbol
      timeframe (str): TF
      quiet (bool,optional): Output quiet
      tlid_range (str,optional): TLID range
      cc (JGTChartConfig, optional): The JGTChartConfig object to use for the processing. Defaults to None.
      cc (JGTChartConfig, optional): The JGTChartConfig object to use for the processing. Defaults to None.

  Returns:
      pandas.DataFrame: CDS DataFrame
  """
  try:
    df=pds.getPH_from_filestore(instrument,timeframe,quiet=quiet,tlid_range=tlid_range)
    if not quiet:
      print(df)
  
    dfi=createFromDF(df,quiet=quiet,cc=cc)
    return dfi
  except:
    return None

def createFromDF(df, quiet=True,cc: JGTChartConfig = None):
  """
  Creates a new DataFrame with indicators, signals, and cleansed columns added based on the input DataFrame.

  Args:
    df (pandas.DataFrame): The input DataFrame to add indicators, signals, and cleansed columns to.
    quiet (bool, optional): Whether to suppress console output during processing. Defaults to True.
    cc (JGTChartConfig, optional): The JGTChartConfig object to use for the processing. Defaults to None.

  Returns:
    pandas.DataFrame: The new DataFrame with indicators, signals, and cleansed columns added.
  """
  if cc is None:
    cc = JGTChartConfig()
    
  if df.index.name == 'Date':
      df.reset_index(inplace=True)
  dfi=ids.tocds(df,quiet=quiet,cc=cc) 
  return dfi


def create(instrument,timeframe,nb2retrieve=335,stayConnected=False,quiet=True,cc: JGTChartConfig = None):
  """Create CDS (Chaos Data Service) with Fresh Data

  Args:
      instrument (str): symbol
      timeframe (str): TF
      nb2retrieve (int, optional): nb bar to retrieve. Defaults to 335.
      stayConnected (bool, optional): Leave Forexconnect connected. Defaults to False.
      quiet (bool,optional): Output quiet
      cc (JGTChartConfig, optional): The JGTChartConfig object to use for the processing. Defaults to None.

  Returns:
      pandas.DataFrame: CDS DataFrame
  """
  
  df=pds.getPH(instrument,timeframe,nb2retrieve,with_index=False,quiet=quiet,cc=cc)
  dfi=createFromDF(df,quiet=quiet,cc=cc)
  return dfi
  

#createByRange
def createByRange(instrument,timeframe,start,end,stayConnected=False,quiet=True):
  """Create CDS with Fresh Data from a range

  Args:
      instrument (str): symbol
      timeframe (str): TF
      start (date): start date
      end (date): end date
      stayConnected (bool, optional): Leave FXCMPY connected. Defaults to False.
      quiet (bool,optional): Output quiet

  Returns:
      pandas.DataFrame: CDS DataFrame
  """
  pds.stayConnected=stayConnected
  df=pds.getPHByRange(instrument,timeframe,start,end,with_index=False,quiet=quiet)
  dfi=createFromDF(df,quiet=quiet)
  return dfi





columns_to_remove = ['aofvalue', 'aofhighao', 'aoflowao', 'aofhigh', 'aoflow', 'aocolor', 'accolor', 'fdbbhigh', 'fdbblow', 'fdbshigh', 'fdbslow']
def create_and_clean_data_from_file_df(instrument, timeframe):
    # Create DataFrame from PDS file
    cdf = createFromPDSFile(instrument, timeframe)

    # Remove specified columns if provided
    if columns_to_remove:
        cdf = cdf.drop(columns=columns_to_remove, errors='ignore')

    # Set 'Date' as the index
    cdf.set_index(c.DATE, inplace=True)

    return cdf


  
def _save_cds_data_to_file(df, instrument, timeframe):
    # Define the file path based on the environment variable or local path
    data_path = get_data_path()
    fpath = pds.mk_fullpath(instrument, timeframe, 'csv', data_path)

    # Save DataFrame to CSV
    df.to_csv(fpath)
    return fpath

def createFromFile_and_clean_and_save_data(instrument, timeframe):
    # Create DataFrame from PDS file
    cdf =create_and_clean_data_from_file_df(instrument, timeframe)
    _save_cds_data_to_file(cdf, instrument, timeframe)


    return cdf









def getSubscribed():
  return pds.getSubscribed()

def getActiveSymbols():
  AppSuiteConfigRootPath = os.getenv('AppSuiteConfigRootPath')
  fn='activesymbol.txt'
  fpath=os.path.join(AppSuiteConfigRootPath,fn)
  with open(fpath) as f:
    first_line = f.readline()
    print(first_line)

# %%
def getLast(_df):
  return _df.iloc[-1]

def getPresentBar(_df):
  r= _df#['High','Low',indicator_AO_awesomeOscillator_column_name,signalCode_fractalDivergentBar_column_name,indicator_AC_accelerationDeceleration_column_name]
  return r.iloc[-1:]

def getPresentBarAsList(_df):
  _paf =_df.iloc[-1:]
  _pa = _paf.to_dict(orient='list')
  _dtctx=str(_paf.index.values[0])
  _pa['Date'] = _dtctx
  return _pa


def getLastCompletedBarAsList(_df):
  _paf =_df.iloc[-2:-1]
  _pa = _paf.to_dict(orient='list')
  _dtctx=str(_paf.index.values[0])
  _pa['Date'] = _dtctx
  return _pa





def checkFDB(_instrument,_timeframe):
  _df=create(_instrument)
  pa = getPresentBarAsList(_df)
  isfdb = pa[c.FDB][0]  != 0.0
  fdb = pa[c.FDB]
  dtctx = pa[c.DATE]
  if isfdb:
    print(_instrument + "_" + _timeframe + " : We Have a Signal : " + dtctx)
    return True
  else:
    print(_instrument + "_" + _timeframe +  " : No signal now : " + dtctx)
    return False



def print_quiet(quiet,content):
    if not quiet:
        print(content)



