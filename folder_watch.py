from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
from df import extract_and_parse
from categorise import categorise_transaction
from analysis import summary, export_spreadsheet

class NewPDFHandler(FileSystemEventHandler):
    def on_created(self,event):
        if event.is_directory or not event.src_path.endswith('.pdf'):
            return
        pdf_route = event.src_path
        print(f"New PDF detected: {pdf_route}")
        pdf_route = '/home/cchilton2002/Downloads/fd statement ••• 20240913.pdf'
        df = extract_and_parse(pdf_route)
        df['Category'] = df['Details'].apply(categorise_transaction)
        summary_df = summary(df)
        export_spreadsheet(summary_df, df, 'transaction_summary.xlsx')