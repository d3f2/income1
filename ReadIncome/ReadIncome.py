"""
Read class has methods to read the kenji - income.csv file into a dataframe that will then be used by MakeIncome class to print an income statement in the out.txt file, log messages and errors are logged to example.log
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

dateparse = lambda x: datetime.strptime(x, "%m/%d/%Y")

def checkColNames(df):
    # I couldn't work out how to do the expecting index and columns in one execution so I split them up
    # index check
    expecting_index = [
        'ScenarioName', 
        'AccountClass', 
        'AccountType', 
        'AccountName', 
        'JournalDate'
        ]
    if ( set(df.index.names) != set(expecting_index) ):
        raise ValueError(
            "csv self.df.index.names.tolist() != expecting"
            )
    # columns check
    expecting_columns = ['NetAmount']
    if ( set(df.columns.tolist()) != set(expecting_columns) ):
        raise ValueError(
            "csv self.df.columns != expecting"
            )

class Read(object):
    def __init__(self):
        """
        Initialise
        """
        self.df = pd.read_csv(
            'kenji - income.csv',
            header=0,
            dtype={
                'ScenarioName': str,
                'AccountClass': str,
                'AccountType': str,
                'AccountName': str,
                'JournalDate': str,
                'NetAmount': str
                },
            index_col=[0,1,2,3,4],
            parse_dates=[4], date_parser=dateparse
            # I have not used converters={5: to_decimal } function here because itis called once for each string so it is slow instead I have used a vector approach in parseAmountCol() method
        )
        self.parseColNames(self.df)
        self.parseAmountCol(self.df)
        self.addTypeCol(self.df)
        # read_csv includes an index automagically but there is a performance warning if it is not sorted
        self.sortIndex(self.df)
        logging.info('Success: ReadIncome.Read')

    def parseColNames(self,df):
        """
        Before getting started I thought it's good to check the column names are what we expect them to be otherwise raise a value error and log to the output file.
        """
        try:
            checkColNames(df)
        except:
            logging.info('Warn: unexpected column names in csv file')
            print("An exception occurred")
    
    def parseAmountCol(self,df):
        """
        Overwrite the amount column with a float object, since the csv has strings containing special characters: dollar signs and commas.
        """
        df['NetAmount'] = df['NetAmount'].replace({'\$':'',',':''},regex=True).astype(np.dtype("float"))
        logging.info('Success: parsed amount column of csv')

    def addTypeCol(self,df):
        """
        Add a column with the type so that can seperate journal from aggregates
        """
        ###################
        # if you want to include FormatType in the index then do the following:
        # df1 = pd.DataFrame({'FormatType':'journal'},index=df.index)
        # df2 = pd.concat([df,df1], axis=1)
        # df3 = df2.set_index(['FormatType'],append=True)
        # order = ['ScenarioName','AccountClass','AccountType','AccountName','FormatType','JournalDate']
        # df4 = df3.reorder_levels(order).sort_index()
        ################### 
        # However I don't think I want FormatType in the index because it's just used for formatting the output in the text file the different formats are Journal, SubTotal and Total that will be used for colors and line thickness.
        self.df['FormatType'] = 'Journal'
        logging.info('Success: type col added to df on load')
    
    def sortIndex(self,df):
        # to check index is sorted for performance uncomment the print statements below:
        # print(self.df.index.is_monotonic_increasing)
        self.df = df.sort_index()
        # print(self.df.index.is_monotonic_increasing)
        # print(df.index.has_duplicates)