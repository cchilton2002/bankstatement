import pandas as pd
import pdfplumber  
import re


def format_date(date_str: str) -> str:
    """Format date by adding a space between month and day."""
    return date_str[:3] + ' ' + date_str[3:]

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'(\w{3})(\d{2})', r'\1 \2', text)

    return text

def extract_transactions_hsbc(text: str) -> pd.DataFrame:  
    pattern = r'(\d{2}\s\w{3}\s\d{2})\s+(\d{2}\s\w{3}\s\d{2})\s+(.+?)\s+(-?\d+\.\d{2})(CR|DR)?'
    transactions = []
    lines = text.strip().split('\n')
    for line in lines:
        cleaned_line = clean_text(line)
        match = re.search(pattern, cleaned_line)
        if match:
            received_date, transaction_date, details, amount, transaction_type = match.groups()
            details = re.sub(r'\)+', '', details).strip()  # Remove closing brackets
            details = re.sub(r'\(+', '', details).strip()  # Remove opening brackets
            transactions.append({
                "Received Date": received_date,
                "Transaction Date": transaction_date,
                "Details": details.strip(),
                "Amount": float(amount),
                "Type": transaction_type if transaction_type else None  # Type could be CR or DR
            })
    return pd.DataFrame(transactions)



def extract_transactions_amex(text: str) -> pd.DataFrame:
    
    pattern = r'(\w{3}\d{1,2})\s+(\w{3}\d{1,2})\s+(.+?)\s+(-?\d+\.\d{2})$'
    transactions = []
    lines = text.strip().split('\n')
    
    for i in range(len(lines)):
        cleaned_line = lines[i].strip()
        match = re.search(pattern, cleaned_line)
        if match:
            received_date, transaction_date, details, amount = match.groups()
            
            details = re.sub(r'\)+', '', details).strip()  # Remove closing brackets
            details = re.sub(r'\(+', '', details).strip()  # Remove opening brackets
            
            transaction_type = None
            if i + 1 < len(lines) and lines[i + 1].strip() == 'CR':
                transaction_type = 'CR'  # Credit transaction
            else:
                transaction_type = 'None'  # Debit transaction
            
            transactions.append({
                "Received Date": format_date(received_date),
                "Transaction Date": format_date(transaction_date),
                "Details": details.strip(),
                "Amount": float(amount),
                "Credit": transaction_type
            })

    return pd.DataFrame(transactions)

def extract_and_parse(pdf_path: str, option: str) -> pd.DataFrame:
    text = extract_text_from_pdf(pdf_path)
    if (option == 'hsbc'):
        return extract_transactions_hsbc(text)
    elif (option == 'amex'):
        return extract_transactions_amex(text)
    

        
# pdf_route = '/home/cchilton2002/Documents/bankStatements/Input/16_Sep_2024_-_15_Oct_2024.pdf'        
# df = extract_and_parse(pdf_route,'amex')
# print(df)
        



# def main() -> None:
#     pdf_route = '/home/cchilton2002/Downloads/fd statement ••• 20240913.pdf'
#     text = extract_text_from_pdf(pdf_route)
#     extract_transactions(text)
    


# if __name__ == "__main__":
#     main()