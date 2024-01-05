# Introduction 
a simple library to quere EODHistoricalData in a multithreaded environment

ATTENTION - The lib doesn't support all of the function calls available from EOD,
at the moment just historical stockprices are supported

# Getting Started
This library is a simple wrapper over the function calls listed at eodhd.com in order to retrive the 
price datas for some tickers. As mentioned above, only a small set of functions is supported at the 
moment, my focus point was to have a multithreaded environment available when accessing the data for 
more then one asset. If you hand over a list of ticker symbols in the getStockPrices function, the 
lib will use multiple threads to query eodhd.com at the same time, so with this it's more time efficient
then doing it sequentially. 

# Build and Test
pip install eod2pd

# Project Homepage
https://dev.azure.com/neuraldevelopment/eod2pd

# Contribute
If you find a defect or suggest a new function, please send an eMail to neutro2@outlook.de
