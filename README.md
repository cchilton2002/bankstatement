The programme needs a pdf bank statement, it has been optimised for HSBC and AMEX credit card statements however can be easily tuned to other statements. 

1. To start place the pdf in the Input folder and then run the main.py script where it will first parse the pdf to text and then create a dataframe using a regex pattern to spot each transaction.

2. Once the dataframe has been created (df.py) specifying each transaction, you use categorise.py which feeds into the local LLM, in my case gemma2,  the description of each transaction and returns a category for it.

3. Then analyse.py groups the data by category and produces seperate tabs for a breakdown of each category in an exported .xslx file which you can find in the Output folder.

