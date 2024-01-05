# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : eod2pd
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  a simple library to quere EODHistoricalData in a multithreaded environment
#
# =============================================================================


# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
from basefunctions.threadpool import ThreadPoolFunction
import eod2pd.downloader
import pandas as pd
import numpy as np

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
#  FUNCTION DEFINITIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
#  get stock prices from EODHistoricalData
# -------------------------------------------------------------
def getStockPrices(
    symbols="BMW.XETRA",
    start="1900-01-01",
    end="2999-12-31",
    freq="D",
    normalize=False,
    dropnaTickers=False,
    dropna=False,
    dropVolume=False,
    capitalize=False,
    formatStockstats=False,
):
    """
    Get historical stock prices for the given symbols.

    Parameters
    ----------
    symbols : str or list of str, optional
        The symbols of the stocks to retrieve prices for, default: "BMW.XETRA"
    start : str, optional
        The start date of the prices data, default: "1900-01-01"
    end : str, optional
        The end date of the prices data, default: "2999-12-31"
    freq : str, optional
        The frequency of the prices data, default: "D"
    normalize : bool, optional
        Whether to normalize the prices, default: False
    dropnaTickers : bool, optional
        Whether to drop tickers with missing data, default: False
    dropna : bool, optional
        Whether to drop rows with missing data, default: False
    dropVolume : bool, optional
        Whether to drop the volume column, default: False
    capitalize : bool, optional
        Whether to capitalize the column names, default: False
    formatStockstats : bool, optional
        Whether to format the column names for stockstats library, default: False

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the historical stock prices for the given symbols.
    """
    # check if symbol is a list
    if isinstance(symbols, str):
        symbols = [symbols]
    for symbol in symbols:
        params = eod2pd.downloader.getParams(
            symbol=symbol, start=start, end=end, freq=freq
        )
        url = f"https://eodhistoricaldata.com/api/eod/{params['symbol']}?from={params['start']}&to={params['end']}&api_token={params['apiKey']}&period={params['freq']}&fmt=json"
        params["url"] = url
        eod2pd.threadPool.getInputQueue().put(params)
    # wait until all jobs are done
    eod2pd.threadPool.getInputQueue().join()
    # get result dataframe
    df = eod2pd.downloader.buildResultDataFrame(
        eod2pd.threadPool.getOutputQueue(),
        normalize=normalize,
        dropnaTickers=dropnaTickers,
        dropna=dropna,
        dropVolume=dropVolume,
        capitalize=capitalize,
        formatStockstats=formatStockstats,
    )
    # return result
    return df


# -------------------------------------------------------------
#  get stock dividends from EODHistoricalData
# -------------------------------------------------------------
def getStockDividends(symbols="BMW.XETRA", start="1900-01-01", end="2999-12-31"):
    """
    Get historical stock dividends for the given symbols.

    Parameters
    ----------
    symbols : str or list of str, optional
        The symbols of the stocks to retrieve dividends for, default: "BMW.XETRA"
    start : str, optional
        The start date of the dividends data, default: "1900-01-01"
    end : str, optional
        The end date of the dividends, default: "2999-12-31"

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the historical stock dividends for the given symbols.
    """
    # check if symbol is a list
    if isinstance(symbols, str):
        symbols = [symbols]
    for symbol in symbols:
        params = eod2pd.downloader.getParams(
            symbol=symbol.lower(), start=start, end=end
        )
        url = f"https://eodhistoricaldata.com/api/div/{params['symbol']}?from={params['start']}&to={params['end']}&api_token={params['apiKey']}&fmt=json"
        params["url"] = url
        eod2pd.threadPool.getInputQueue().put(params)
    # wait until all jobs are done
    eod2pd.threadPool.getInputQueue().join()
    # get result dataframe
    df = eod2pd.downloader.buildResultDataFrame(eod2pd.threadPool.getOutputQueue())
    # return result
    return df


# -------------------------------------------------------------
#  get stock splits from EODHistoricalData
# -------------------------------------------------------------
def getStockSplits(symbols="BMW.XETRA", start="1900-01-01", end="2999-12-31"):
    """
    Get historical stock splits for the given symbols.

    Parameters
    ----------
    symbols : str or list of str, optional
        The symbols of the stocks to retrieve stock splits for, default: "BMW.XETRA"
    start : str, optional
        The start date of the splits data, default: "1900-01-01"
    end : str, optional
        The end date of the splits data, default: "2999-12-31"

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the historical stock splits for the given symbols.
    """
    # check if symbol is a list
    if isinstance(symbols, str):
        symbols = [symbols]
    for symbol in symbols:
        params = eod2pd.downloader.getParams(
            symbol=symbol.lower(), start=start, end=end
        )
        url = f"https://eodhistoricaldata.com/api/splits/{params['symbol']}?from={params['start']}&to={params['end']}&api_token={params['apiKey']}&fmt=json"
        params["url"] = url
        eod2pd.threadPool.getInputQueue().put(params)
    # wait until all jobs are done
    eod2pd.threadPool.getInputQueue().join()
    # get result dataframe
    df = eod2pd.downloader.buildResultDataFrame(eod2pd.threadPool.getOutputQueue())
    # return result
    return df


# -------------------------------------------------------------
#  get list of exchanges from EODHistoricalData
# -------------------------------------------------------------
def getExchanges():
    """
    Get the list of exchanges from EODHistoricalData.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the list of exchanges.
    """
    params = eod2pd.downloader.getParams()
    url = f"https://eodhistoricaldata.com/api/exchanges-list/?api_token={params['apiKey']}&fmt=json"
    params["url"] = url
    eod2pd.threadPool.getInputQueue().put(params)
    # wait until all jobs are done
    eod2pd.threadPool.getInputQueue().join()
    # get result dataframe
    df = eod2pd.downloader.buildResultDataFrame(eod2pd.threadPool.getOutputQueue())
    # return result
    return df


# -------------------------------------------------------------
#  get list of stocks for a specific exchange from EODHistoricalData
# -------------------------------------------------------------
def getStocksForExchange(exchangeCode="XETRA"):
    """
    Get the list of stocks for a specific exchange from EODHistoricalData.

    Parameters
    ----------
    exchangeCode : str, optional
        The code of the exchange, default: "XETRA"

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the list of stocks for the specified exchange.
    """
    params = eod2pd.downloader.getParams(exchangeCode=exchangeCode)
    url = f"https://eodhistoricaldata.com/api/exchange-symbol-list/{params['exchangeCode']}?api_token={params['apiKey']}&fmt=json"
    params["url"] = url
    eod2pd.threadPool.getInputQueue().put(params)
    # wait until all jobs are done
    eod2pd.threadPool.getInputQueue().join()
    # get result dataframe
    df = eod2pd.downloader.buildResultDataFrame(eod2pd.threadPool.getOutputQueue())
    # return result
    return df
