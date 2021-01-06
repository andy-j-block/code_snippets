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
# the two inputs are:
#   - the filepath of the given file that you want to grab the data from
#   - the numbers of the pages where you want to collect the data from
#
# the function iterates thru the pages where the data exists and concats the data together
#
# the multiple_tables option may need to be set to True in order for all the tables to be captured the way that's preferrable
#
##############

import tabula
import pandas as pd
    
def read_pdf(filepath, page_nums):
        
    df = pd.DataFrame()
    
    for i in page_nums:
        pdf_table = tabula.read_pdf(filepath, pages=i)
        df = pd.concat([df, pdf_table], ignore_index=True)
    
    return df