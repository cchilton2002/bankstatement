import pandas as pd
from df import extract_and_parse
from categorise import categorise_transaction
from analysis import summary, export_spreadsheet, filename


# WATCH_FOLDER = '/home/cchilton2002/Documents/bankStatements/Input/Output'
# OUTPUT_FOLDER = '/home/cchilton2002/Documents/bankStatements/Input'



def main() -> None:
        
    pdf_route = '/home/cchilton2002/Documents/bankStatements/Input/16_Sep_2024_-_15_Oct_2024.pdf' 
    df = extract_and_parse(pdf_route,'amex')
    fileName = filename(df)
    df['Category'] = df['Details'].apply(categorise_transaction)

    summary_df = summary(df)
    export_spreadsheet(summary_df, df, f"{fileName}")
    
if __name__ == "__main__":
    main()


