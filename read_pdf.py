##############
#
# read_pdfs
# written by: Andy Block
# date: Jan 5, 2021
#   
##############
#
# this function takes the data from tables in pdf files and returns that data as a pandas dataframe
#
# the three inputs are:
#   - the filepath of the given file that you want to grab the data from
#   - the numbers of the pages where you want to collect the data from
#   - any columns the user would like to drop, which helps with concat performance
#
# the function iterates thru the pages where the data exists and concats the data together
#
# the multiple_tables option may need to be set to True in order for all the tables to be captured the way that's preferrable
#
##############

import tabula
import pandas as pd
    
def read_pdf(filepath, page_nums, drop_cols=None):
        
    df = pd.DataFrame()
    
    for i in page_nums:
        pdf_table = tabula.read_pdf(filepath, pages=i)

        if drop_cols is not None:
        	pdf_table.drop(columns=drop_cols, inplace=True)
        
        df = pd.concat([df, pdf_table], ignore_index=True)
    
    return df