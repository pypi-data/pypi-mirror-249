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
import basefunctions
import decouple
import requests
import pandas as pd
import numpy as np
import stockstats


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
#  CLASS DEFINITIONS
# -------------------------------------------------------------
class Downloader(basefunctions.ThreadPoolFunction):
    # -------------------------------------------------------------
    # VARIABLE DEFINTIONS
    # -------------------------------------------------------------
    params = {
        "apiKey": decouple.config("EOD_API_KEY"),
    }

    # -------------------------------------------------------------
    #  Constructor of the Downloader class. We can set here the
    #  maximum number of retries and the default timeout value
    # -------------------------------------------------------------
    def __init__(self, defaultNumOfRetires=3, defaultTimeout=5):
        """
        Constructor of the Downloader class.

        Parameters
        ----------
        defaultNumOfRetires : int, optional
            The default number of retries to get the data from the URL. The default is 3.
        defaultTimeout : int, optional
            The default timeout value for the request in seconds. The default is 5.
        """
        # call parent constructor
        super().__init__()
        # set variables
        self.params["numOfRetries"] = defaultNumOfRetires
        self.params["timeout"] = defaultTimeout

        # -------------------------------------------------------------
        #  callable method gets called by the threadpool after a
        #  new command has arrived in the input queue. From the class
        #  it's not possible to predict from which thread this function
        #  is called. The function has to be thread safe.
        # -------------------------------------------------------------
        # -------------------------------------------------------------
        #  callable method gets called by the threadpool after a
        #  new command has arrived in the input queue. From the class
        #  it's not possible to predict from which thread this function
        #  is called. The function has to be thread safe.
        # -------------------------------------------------------------

    def callable(self, outputQueue, item):
        """
        Downloads data from a URL and puts it into the output queue.

        Parameters
        ----------
        outputQueue : Queue
            The queue to put the downloaded data into.
        item : dictionary with the following keys:
            - "symbol": str, the symbol associated with the data
            - "url": str, the URL to download the data from
            - "numOfRetries": int, optional, the number of retries to get the data from the URL
            - "timeout": int, optional, the timeout value for the request in seconds

        Raises
        ------
        ValueError
            If the data cannot be retrieved after the maximum number of retries.
        """
        # init variables
        done = False
        if not isinstance(item, dict):
            raise ValueError("item is not a dictionary")
        numOfRetries = (
            item["numOfRetries"] if "numOfRetries" in item else self.defaultNumOfRetires
        )
        while numOfRetries > 0:
            try:
                # load data from url with timeout parameter set, convert them afterwards to json
                data = requests.get(item["url"], timeout=item["timeout"]).json()
                # put data into output queue
                if "symbol" not in item:
                    item["symbol"] = "unknown"
                outputQueue.put((item["symbol"], data))
                # all done, so clean up
                done = True
                break
            except Exception as e:
                numOfRetries -= 1
                continue
        if not done:
            raise ValueError(
                f"could not download data for request {item['symbol']} {item['url']}"
            )

    # -------------------------------------------------------------
    #  get the params dictionary
    # -------------------------------------------------------------
    def getParams(self, **kwargs):
        params = self.params.copy()
        for key, value in kwargs.items():
            params[key] = value
        return params

    # =============================================================================
    #
    # helper functions
    #
    # =============================================================================
    def buildResultDataFrame(
        self,
        queue,
        normalize=False,
        dropnaTickers=False,
        dropna=False,
        dropVolume=False,
        capitalize=False,
        formatStockstats=False,
    ):
        """this function builds the result dataframe
        from both offline db and online requests

        Parameters
        ----------
        queue : Queue
            Queue with pandas dataFrames
        normalize: boolean, optional
            normalize all columns to first value
        dropnaTickers: boolean, optional
            drop all tickers with NaN values
        dropna: boolean, optional
            drop all rows with NaN values
        dropVolume: boolean, optional
            drop volume column
        capitalize: boolean, optional
            capitalize all tickers
        formatStockstats: boolean, optional
            return stockstats dataframe

        Returns
        -------
        pandas dataframe
            pandas dataframe with requested data
        """
        # build result
        sortList = ["open", "high", "low", "close", "adjusted_close", "volume"]
        dfList = []
        keyList = []
        while not queue.empty():
            ticker, json = queue.get()
            df = pd.DataFrame(json)
            if "date" in df.columns:
                df.set_index("date", inplace=True)
            keyList.append(ticker)
            dfList.append(df)
        if len(dfList) == 0:
            return pd.DataFrame()
        if len(dfList) > 1:
            df = pd.concat(dfList, axis=1, keys=keyList)
            if dropnaTickers:
                df = df[[col for col in df.columns if not np.isnan(df[col].iloc[0])]]
            df = df.swaplevel(axis=1).sort_index(axis=1)
        else:
            df = dfList[0]
        if dropnaTickers:
            df = df.dropna(axis=1)
        if dropna:
            df = df.dropna()
        if normalize:
            df = df.apply(lambda x: x / x.iloc[0], axis=0)
        if "adjusted_close" in df.columns:
            df = df[sortList].sort_index()
        if "volume" in df.columns and dropVolume:
            df = df.drop(columns=["volume"], level=0)
        if capitalize:
            df.columns = df.columns.set_levels(
                df.columns.levels[0].str.capitalize(), level=0
            )
        if formatStockstats:
            df = stockstats.StockDataFrame(df)
        return df
