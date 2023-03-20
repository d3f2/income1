""" 
See the getting started in readme.md. This is the entry file.
"""

import logging

from ReadIncome import ReadIncome
from MakeIncome import MakeIncome

def main():
    df_income = ReadIncome.Read()
    MakeIncome.Make(df_income.df)

if __name__ == '__main__':
    logging.basicConfig(
        filename='example.log', 
        encoding='utf-8', 
        level=logging.DEBUG, 
        format='%(asctime)s %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p %Z'
        )
    main()