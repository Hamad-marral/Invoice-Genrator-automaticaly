from docxtpl import DocxTemplate
import datetime
import os

try:
    from docx2pdf import convert
    DOCX2PDF_AVAILABLE = True
except ImportError:
    DOCX2PDF_AVAILABLE = False


def generate_invoice(name, phone, invoice_list, email=None, status="Unpaid"):
    # Create Invoices folder if not exists
    folder = "Invoices"
    os.makedirs(folder, exist_ok=True)

    # Load DOCX template
    doc = DocxTemplate("invoice_template.docx")

    # Calculate subtotal and total
    subtotal = sum(item[3] for item in invoice_list)  # item[3] = price
    salestax = 0.1
    total = subtotal * (1 + salestax)

    # Format numbers for professional invoice
    subtotal_formatted = f"₨{round(subtotal):,}"  # Rounded, comma separated
    total_formatted = f"₨{round(total):,}"        # Rounded, comma separated
    salestax_formatted = f"{salestax*100:.0f}%"  # e.g., "10%"

    # Context for template
    context = {
        "name": name,
        "phone": phone,
        "email": email,
        "invoice_list": invoice_list,
        "subtotal": subtotal_formatted,
        "salestax": salestax_formatted,
        "total": total_formatted,
        "status": status
    }

    # Generate file paths
    doc_name = f"invoice_{name.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')}"
    doc_path = os.path.join(folder, doc_name + ".docx")
    pdf_path = os.path.join(folder, doc_name + ".pdf")

    # Render DOCX
    doc.render(context)
    doc.save(doc_path)

    # Convert to PDF if possible
    if DOCX2PDF_AVAILABLE:
        try:
            convert(doc_path, pdf_path)
            return pdf_path
        except Exception as e:
            print("⚠️ PDF conversion failed:", e)
            return None
    else:
        print("⚠️ docx2pdf not installed! Run: pip install docx2pdf")
        return None
