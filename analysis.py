import pandas as pd 
from df import extract_and_parse 
from categorise import categorise_transaction
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
import os
import numpy as np



def auto_adjust_column_width(worksheet: Worksheet) -> None:
    for column_cells in worksheet.columns:
        max_length = max(len(str(cell.value)) for cell in column_cells if cell.value)  # Ignore empty cells
        worksheet.column_dimensions[get_column_letter(column_cells[0].column)].width = max_length + 2


def summary(df: pd.DataFrame) -> pd.DataFrame:
    if 'Category' in df.columns:
        
        category_totals = df.groupby('Category')['Amount'].sum().reset_index()
        category_totals.columns= ['Categories','Totals (£)']
        total = category_totals['Totals (£)'].sum()
        total_cr = category_totals[category_totals['Categories'].str.contains('credit', case=False, na=False)]['Totals (£)'].sum()

    
        
        category_totals['Spending Percentage (%)'] = ((category_totals['Totals (£)']/(total-total_cr))*100).round(2)
                
        total_row = pd.DataFrame([{'Categories':'Net Spend', 'Totals (£)':total}])
        credit_row = pd.DataFrame([{'Categories':'Credit', 'Totals (£)':total_cr}])        
        
        category_totals = pd.concat([category_totals,credit_row], ignore_index=True)
        category_totals = pd.concat([category_totals,total_row], ignore_index=True)
        return category_totals
        
    else:
        print("The df doesn't have a column called category")

def export_spreadsheet(total_breakdown: pd.DataFrame, transactions_df: pd.DataFrame, filename: str) -> None:
    with pd.ExcelWriter(f"Input/Output/{filename}") as writer:
        total_breakdown.to_excel(writer, sheet_name='Total Breakdown', index=False)
        worksheet = writer.sheets['Total Breakdown']
        auto_adjust_column_width(worksheet)
        for category, group in transactions_df.groupby('Category'):
            group.to_excel(writer, sheet_name=category, index=False)
            worksheet = writer.sheets[category]
            auto_adjust_column_width(worksheet)
            

def filename(df: pd.DataFrame) -> str:
    if 'Transaction Date' in df.columns:
        min_date = df.loc[0, 'Transaction Date']
        max_date = df.loc[len(df) - 1, 'Transaction Date']
        # Create the filename with dates in the correct order
        filename = f"Transaction-Summary ({min_date} to {max_date}).xlsx"
        return filename
    else:
        raise ValueError("DataFrame does not contain a 'Transaction Date' column.")


        
        
# pdf_route = '/home/cchilton2002/Downloads/fd statement ••• 20240913.pdf'
# df = extract_and_parse(pdf_route)

# df['Category'] = df['Details'].apply(categorise_transaction)

# summary_df = summary(df)

# export_spreadsheet(summary_df, df, 'transaction_summary.xlsx')


