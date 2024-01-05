# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : stocksdb
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  a simple package that creates a database based on postgres to store stock values
#
# =============================================================================

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
from basefunctions.threadpool import ThreadPool
from eod2pd.downloader import Downloader
from eod2pd.functions import (
    getStockPrices,
    getStockDividends,
    getExchanges,
    getStocksForExchange,
)

downloader = Downloader()
threadPool = ThreadPool(numOfThreads=10, callable=downloader)
