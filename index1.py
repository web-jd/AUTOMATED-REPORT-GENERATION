import csv
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Step 1: Create CSV file
csv_file = "data.csv"
data = [
    ["Date", "Product", "Units Sold", "Revenue"],
    ["01-06-2025", "Product A", 10, 1000],
    ["02-05-2025", "Product B", 5, 500],
    ["03-05-2025", "Product A", 8, 800],
    ["04-05-2025", "Product C", 12, 1800],
    ["05-05-2025", "Product B", 7, 700]
]

with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"CSV file '{csv_file}' created successfully!")

# Step 2: Read and summarize the data
def read_data_summary(file_path):
    df = pd.read_csv(file_path)
    return df.describe().round(2)  # Rounded to 2 decimal places

def read_data_full(file_path):
    return pd.read_csv(file_path)

# Step 3a: Generate summary PDF
def generate_summary_pdf(data_summary, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Summary Report")
    c.setFont("Helvetica", 12)
    
    y = 760
    c.drawString(100, y, "Statistic")
    columns = list(data_summary.columns)
    x_positions = [200 + 100 * i for i in range(len(columns))]
    
    for i, col in enumerate(columns):
        c.drawString(x_positions[i], y, col)
    
    y -= 30
    for index, row in data_summary.iterrows():
        c.drawString(100, y, index)
        for i, val in enumerate(row):
            c.drawString(x_positions[i], y, str(val))
        y -= 20
        if y < 50:
            c.showPage()
            y = 800
    c.save()

# Step 3b: Generate detailed PDF
def generate_detailed_pdf(data, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Detailed Sales Report")
    c.setFont("Helvetica-Bold", 12)
    
    headers = ["Date", "Product", "Units Sold", "Revenue"]
    positions = [50, 150, 280, 380]
    
    y = 770
    for i, header in enumerate(headers):
        c.drawString(positions[i], y, header)
    
    c.setFont("Helvetica", 12)
    y -= 20
    
    for _, row in data.iterrows():
        c.drawString(positions[0], y, str(row["Date"]))
        c.drawString(positions[1], y, str(row["Product"]))
        c.drawString(positions[2], y, str(row["Units Sold"]))
        c.drawString(positions[3], y, f"₹{row['Revenue']:,.2f}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 800
    c.save()

# Run all
summary = read_data_summary(csv_file)
full_data = read_data_full(csv_file)

generate_summary_pdf(summary, "summary_report.pdf")
print("PDF 'summary_report.pdf' generated successfully!")

generate_detailed_pdf(full_data, "detailed_report.pdf")
print("PDF 'detailed_report.pdf' generated successfully!")
