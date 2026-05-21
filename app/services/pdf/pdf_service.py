from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os
from app.core.config import settings

def generate_payslip_pdf(payroll_record_id: int, employee_data: dict, salary_data: dict, destination_path: str):
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    c = canvas.Canvas(destination_path, pagesize=A4)
    width, height = A4
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "EMS PAYROLL INC.")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Payslip for Month {salary_data.get('month')} / {salary_data.get('year')}")
    
    # Employee Info
    c.drawString(50, height - 120, f"Employee Name: {employee_data.get('name')}")
    c.drawString(50, height - 140, f"Employee Code: {employee_data.get('code')}")
    c.drawString(50, height - 160, f"Account No: {employee_data.get('account')}")
    
    # Financials
    c.drawString(50, height - 220, "Earnings")
    c.drawString(300, height - 220, "Deductions")
    
    y_earn = height - 250
    y_ded = height - 250
    
    items = salary_data.get('items', [])
    for item in items:
        name = item.get("name")
        amount = item.get("amount")
        if item.get("type") == "earning":
            c.drawString(50, y_earn, f"{name}: {amount}")
            y_earn -= 20
        else:
            c.drawString(300, y_ded, f"{name}: {amount}")
            y_ded -= 20
    
    # tax amounts
    if salary_data.get('tax') and float(salary_data.get('tax')) > 0:
        c.drawString(300, y_ded, f"Income Tax: {salary_data.get('tax')}")
        y_ded -= 20
    if salary_data.get('pt') and float(salary_data.get('pt')) > 0:
        c.drawString(300, y_ded, f"Professional Tax: {salary_data.get('pt')}")
        y_ded -= 20
            
    final_y = min(y_earn, y_ded) - 20
    
    c.drawString(50, final_y, f"Gross Salary: {salary_data.get('gross')}")
    c.drawString(300, final_y, f"Total Deductions: {salary_data.get('deductions')}")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, final_y - 40, f"NET SALARY: {salary_data.get('net')}")
    
    c.save()
    return destination_path
