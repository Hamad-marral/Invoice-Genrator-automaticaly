
# Invoice Generator (Automated)

**Professional Invoice Generator with PDF Export – Built in Python**

---

## 🚀 Project Overview
The **Invoice Generator** is a simple yet powerful Python application designed to **create professional invoices automatically**.  

It allows users to:  

- Generate invoices in **DOCX format** using a customizable template.  
- Automatically calculate **subtotal, tax, and total**.  
- Display amounts in **Pakistani Rupees (₨)** with rounded values for a professional look.  
- Convert invoices into **PDF format** for easy sharing.  
- Maintain a history of invoices in a dedicated folder.  

This project is ideal for **small businesses, freelancers, and shops** that want to **automate their billing process** efficiently.  

---

## 💡 Features
- ✅ Auto-calculation of **subtotal, tax, and total**  
- ✅ Formatted currency (₨) and rounded numbers  
- ✅ Export invoices as **DOCX and PDF**  
- ✅ Support for **customizable invoice templates**  
- ✅ Easy integration for **email sharing or printing**  
- ✅ Professional branding support (logo, header/footer)  

---

## 📦 Installation
1. Clone this repository:  
```bash
git clone https://github.com/Hamad-marral/Invoice-Genrator-automaticaly.git

---
2. Navigate to the project folder:
```bash
cd Invoice-Genrator-automaticaly
---

3. Install dependencies:
```bash
pip install docxtpl docx2pdf

---

## Step 4: Usage
1. Update invoice_list with your items in the format:
**[item_name, quantity, unit_price, total_price]**
---
2. Call the generate_invoice() function with required details:
**generate_invoice(name="Customer Name", phone="0300XXXXXXX",Email="email", invoice_list=items)**
---
