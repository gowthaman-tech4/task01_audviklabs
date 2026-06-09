import os
import random
from datetime import datetime, timedelta
from fpdf import FPDF
from faker import Faker

fake = Faker('en_IN')

class BankStatementPDF(FPDF):
    def header(self):
        # Logo placeholder
        self.set_fill_color(5, 150, 105) # Emerald green
        self.rect(10, 10, 20, 20, 'F')
        self.set_font('helvetica', 'B', 24)
        self.set_text_color(5, 150, 105)
        self.cell(25)
        self.cell(0, 10, 'Global Horizon Bank', border=False, ln=True, align='L')
        
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(25)
        self.cell(0, 5, 'Your Trusted Financial Partner', border=False, ln=True, align='L')
        
        self.ln(10)
        self.set_draw_color(5, 150, 105)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Global Horizon Bank Confidential', align='C')

def generate_bank_statement():
    pdf = BankStatementPDF()
    pdf.add_page()
    
    # Generate PII
    name = fake.name()
    address = fake.address().replace('\n', ', ')
    phone = fake.phone_number()
    email = fake.email()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%d-%m-%Y')
    pan = fake.pystr_format(string_format='?????####?')
    account_no = str(fake.random_number(digits=12, fix_len=True))
    ifsc = "GHB" + str(fake.random_number(digits=7, fix_len=True))
    
    statement_date = datetime.now().strftime('%d %b %Y')
    period_start = (datetime.now() - timedelta(days=90)).strftime('%d %b %Y')
    
    # --- Account Holder Block ---
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, 'MONTHLY ACCOUNT STATEMENT', ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(40, 6, 'Account Holder:')
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, name, ln=True)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(40, 6, 'Address:')
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 6, address)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(40, 6, 'Contact Info:')
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, f"{phone} | {email}", ln=True)
    
    pdf.ln(5)
    
    # --- Account Details Box ---
    pdf.set_fill_color(240, 248, 245)
    pdf.rect(10, pdf.get_y(), 190, 30, 'F')
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(40, 6, 'Account Number:')
    pdf.set_font('helvetica', '', 10)
    pdf.cell(50, 6, account_no)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(40, 6, 'IFSC Code:')
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, ifsc, ln=True)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(40, 6, 'PAN Number:')
    pdf.set_font('helvetica', '', 10)
    pdf.cell(50, 6, pan)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(40, 6, 'Date of Birth:')
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, dob, ln=True)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(40, 6, 'Statement Period:')
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, f"{period_start} to {statement_date}", ln=True)
    
    pdf.ln(10)
    
    # --- Account Summary ---
    opening_balance = round(random.uniform(5000, 50000), 2)
    
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'Account Summary', ln=True)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(50, 6, 'Opening Balance:')
    pdf.cell(0, 6, f"Rs. {opening_balance:,.2f}", ln=True)
    
    pdf.ln(10)
    
    # --- Transactions Header ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'Transaction Details', ln=True)
    
    # Table Header
    def render_table_header():
        pdf.set_fill_color(5, 150, 105)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(25, 8, 'Date', border=1, fill=True)
        pdf.cell(85, 8, 'Description', border=1, fill=True)
        pdf.cell(25, 8, 'Debit (Rs.)', border=1, fill=True, align='R')
        pdf.cell(25, 8, 'Credit (Rs.)', border=1, fill=True, align='R')
        pdf.cell(30, 8, 'Balance (Rs.)', border=1, fill=True, align='R')
        pdf.ln()
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('helvetica', '', 8)
        
    render_table_header()
    
    # Generate ~90 transactions
    balance = opening_balance
    current_date = datetime.now() - timedelta(days=90)
    
    transaction_templates = [
        "UPI/P2P/{name}/{phone}",
        "NEFT Transfer to {name}",
        "Salary Credit from {company}",
        "POS Purchase - {company}",
        "ATM Withdrawal - {city}",
        "Amazon India Purchase",
        "Utility Bill - {phone}",
        "Insurance Premium - {email}"
    ]
    
    total_debit = 0
    total_credit = 0
    
    for i in range(90):
        # Check page break
        if pdf.get_y() > 260:
            pdf.add_page()
            render_table_header()
            
        current_date += timedelta(days=random.randint(0, 2))
        t_date = current_date.strftime('%d-%m-%Y')
        
        # Pick template
        template = random.choice(transaction_templates)
        desc = template.format(
            name=fake.name(),
            phone=fake.phone_number(),
            company=fake.company(),
            city=fake.city(),
            email=fake.email()
        )
        
        is_credit = random.random() < 0.3
        
        if is_credit:
            amt = round(random.uniform(1000, 15000), 2)
            balance += amt
            total_credit += amt
            pdf.cell(25, 6, t_date, border=1)
            pdf.cell(85, 6, desc[:45], border=1)
            pdf.cell(25, 6, '', border=1)
            pdf.cell(25, 6, f"{amt:,.2f}", border=1, align='R')
            pdf.cell(30, 6, f"{balance:,.2f}", border=1, align='R')
        else:
            amt = round(random.uniform(50, 5000), 2)
            balance -= amt
            total_debit += amt
            pdf.cell(25, 6, t_date, border=1)
            pdf.cell(85, 6, desc[:45], border=1)
            pdf.cell(25, 6, f"{amt:,.2f}", border=1, align='R')
            pdf.cell(25, 6, '', border=1)
            pdf.cell(30, 6, f"{balance:,.2f}", border=1, align='R')
            
        pdf.ln()

    # Go back to Summary to update totals (Not strictly necessary in a real sequential PDF generation, 
    # but we can append a closing summary at the end instead of going back).
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(110, 6, 'Closing Balance Summary', border=0)
    pdf.ln()
    pdf.set_font('helvetica', '', 10)
    pdf.cell(50, 6, 'Total Withdrawals:')
    pdf.cell(0, 6, f"Rs. {total_debit:,.2f}", ln=True)
    pdf.cell(50, 6, 'Total Deposits:')
    pdf.cell(0, 6, f"Rs. {total_credit:,.2f}", ln=True)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(50, 6, 'Final Balance:')
    pdf.cell(0, 6, f"Rs. {balance:,.2f}", ln=True)

    output_path = os.path.join(os.path.dirname(__file__), 'realistic_bank_statement.pdf')
    pdf.output(output_path)
    print(f"Generated realistic PDF at {output_path}")

if __name__ == "__main__":
    generate_bank_statement()
