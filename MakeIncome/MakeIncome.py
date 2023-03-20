"""
    add the subtotals to the dataset with the type subtotal
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class Make(object):
    def __init__(self,og_df):
        """
        """
        self.df = og_df
        self.NetRevenue = self.addNetRevenue(self.df)
        self.TotalCogs = self.addTotalCogs(self.df)
        self.GrossProfit = self.addGrossProfit(self.df)
        self.df5 = pd.concat([self.df,self.NetRevenue,self.TotalCogs,self.GrossProfit],keys=['ScenarioName','AccountClass','AccountType','AccountName','JournalDate'],ignore_index=False,verify_integrity=True)
        self.printPvtTable(self.df5)

    def addNetRevenue(self,df):
        '''add a net revenue line with split apply combine'''
        dfA = df.xs('Revenue', axis=0, level=1, drop_level=False)
        df1 = dfA.groupby(by=['ScenarioName','JournalDate'], axis=0, as_index = True)['NetAmount'].sum()
        df2 = pd.DataFrame({'NetAmount':df1},index=df1.index)
        df2['AccountClass'] = 'Revenue'
        df2['AccountType'] = 'Revenue'
        df2['AccountName'] = 'Net Revenue'
        df2['FormatType'] = 'SubTotal'
        df3 = df2.set_index(['AccountClass','AccountType','AccountName'],append=True)
        order = ['ScenarioName','AccountClass','AccountType','AccountName','JournalDate']
        df4 = df3.reorder_levels(order).sort_index()
        return df4

    
    def addTotalCogs(self,df):
        '''add a total cogs line'''
        # level 1 is AccountClass level 2 is AccountType
        dfA = df.xs('Expenses', axis=0, level=1, drop_level=False)
        dfA = dfA.xs('COGS', axis=0, level=2, drop_level=False)
        df1 = dfA.groupby(by=['ScenarioName','JournalDate'], axis=0, as_index = True)['NetAmount'].sum()
        df2 = pd.DataFrame({'NetAmount':df1},index=df1.index)
        df2['AccountClass']='Expenses'
        df2['AccountType']='Total COGS'
        df2['AccountName']='Total COGS'
        df2['FormatType']='SubTotal'
        df3 = df2.set_index(['AccountClass','AccountType','AccountName'],append=True)
        order = ['ScenarioName','AccountClass','AccountType','AccountName','JournalDate']
        df4 = df3.reorder_levels(order).sort_index()
        df5 = pd.concat([df,df4],verify_integrity=True)
        return df5

    def addGrossProfit(self,df):
        '''add a gross profit line'''
        # level 1 is AccountClass level 2 is AccountType
        dfA = df.xs(('Revenue','Revenue'), axis=0, level=(1,2),drop_level=False)
        dfB = df.xs(('Expenses','COGS'), axis=0, level=(1,2),drop_level=False)
        dfAB = pd.concat([dfA,dfB],verify_integrity=True)
        ####
        df1 = dfAB.groupby(by=['ScenarioName','JournalDate'], axis=0, as_index = True)['NetAmount'].sum()
        df2 = pd.DataFrame({'NetAmount':df1},index=df1.index)
        df2['AccountClass']='Expenses'
        df2['AccountType']='Gross Profit'
        df2['AccountName']='Gross Profit'
        df2['FormatType']='SubTotal'
        df3 = df2.set_index(['AccountClass','AccountType','AccountName'],append=True)
        order = ['ScenarioName','AccountClass','AccountType','AccountName','JournalDate']
        # df5 = pd.concat([df,df4],verify_integrity=True)
        df4 =  df3.reorder_levels(order).sort_index()
        # print(df4.index.names)
        return df4
        

    def addGrossProfitMargin(self,df):
        '''add a gross profit margin line'''
        # a = df.loc[(df['AccountType']=='Revenue')|(df['AccountType']=='COGS')]
        # print(a.index)
        # b = a.groupby(by=['ScenarioName','date'], axis=0,as_index = True)

    def printPvtTable(self,df):
        table = pd.pivot_table(df, values=['NetAmount'],
                       index=['ScenarioName', 'AccountClass','AccountType','AccountName','FormatType'],
                       columns=['JournalDate'],
                       fill_value=0, aggfunc=np.sum, dropna=True, )
        labels1 = ['Revenue','Net Revenue','Expenses']
        labels2 = ['Revenue','Net Revenue','COGS','Total COGS','Gross Profit','OPEX','Expense']
        labels3= ['Gross Revenue','Discounts','Net Revenue','Raw Materials','Fulfilment','Transaction Fees','Total COGS','Gross Profit','Labor', 'Marketing', 'SGA & Other', 'EBITDA','Depreciation & Amortization', 'EBIT', 'Interest Expense', 'EBT', 'Taxes']
        table1 = table.reindex(labels1,level=1)
        table2 = table1.reindex(labels2,level=2)
        table3 = table2.reindex(labels3,level=3)
        print(table3)