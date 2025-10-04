import tkinter
from tkinter import ttk, messagebox
import datetime
import csv
from doc_gen import generate_invoice   # import our generator
import smtplib
from email.message import EmailMessage
import os


invoice_list = []


# ---------- Email Sending Function ----------
def send_email(to_email, subject, body, attachment_path):
    sender_email = "hamadkhaliq526@gmail.com"   # <-- apna Gmail
    app_password = "roqm xrae ngds fdzu"        # <-- App password

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # Attach PDF
    with open(attachment_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(f.name)
    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

    print("✅ Invoice emailed successfully!")


# ---------- Functions ----------
def clear_item():
    qty_spinbox.delete(0, tkinter.END)
    qty_spinbox.insert(0, "1")
    desc_entry.delete(0, tkinter.END)
    price_spinbox.delete(0, tkinter.END)
    price_spinbox.insert(0, "0.0")


def add_item():
    qty = int(qty_spinbox.get())
    desc = desc_entry.get()
    price = float(price_spinbox.get())
    line_total = qty * price
    invoice_item = [qty, desc, price, line_total]
    tree.insert('', 0, values=invoice_item)
    clear_item()
    invoice_list.append(invoice_item)


def new_invoice():
    first_name_entry.delete(0, tkinter.END)
    last_name_entry.delete(0, tkinter.END)
    phone_entry.delete(0, tkinter.END)
    email_entry.delete(0, tkinter.END)
    clear_item()
    tree.delete(*tree.get_children())
    invoice_list.clear()


def generate_and_send():
    name = first_name_entry.get() + " " + last_name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    # Generate invoice
    pdf_path = generate_invoice(name, phone, invoice_list, email=email)

    if pdf_path is None:   # ✅ Agar PDF nahi bani
        messagebox.showerror("Error", "Invoice could not be converted to PDF. Please check docx2pdf.")
        return

    # Save history in CSV
    subtotal = sum(item[3] for item in invoice_list)
    total = subtotal * 1.1
    with open("invoice_history.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, phone, subtotal, total, datetime.datetime.now()])

    # Send email if provided
    if email.strip() != "":
        try:
            send_email(
                to_email=email,
                subject=f"Thank you for shopping with us – Your Invoice {name}",
                body="Dear Client,\n\nThank you for shopping with us! We truly appreciate your trust in MADDY TECHNOLOGY.\n\nPlease find attached your invoice.\n\nBest Regards,\nMADDY TECHNOLOGY",
                attachment_path=pdf_path
            )
        except Exception as e:
            messagebox.showerror("Email Error", f"Email sending failed: {e}")
            return

    messagebox.showinfo("Success", "Invoice generated and saved successfully!")
    new_invoice()


# ---------- GUI ----------
window = tkinter.Tk()
window.title("Automated Invoice Generator")

frame = tkinter.Frame(window)
frame.pack(padx=20, pady=10)

# Input fields
tkinter.Label(frame, text="First Name").grid(row=0, column=0)
tkinter.Label(frame, text="Last Name").grid(row=0, column=1)
first_name_entry = tkinter.Entry(frame)
last_name_entry = tkinter.Entry(frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

tkinter.Label(frame, text="Phone").grid(row=0, column=2)
phone_entry = tkinter.Entry(frame)
phone_entry.grid(row=1, column=2)

tkinter.Label(frame, text="Client Email").grid(row=0, column=3)
email_entry = tkinter.Entry(frame)
email_entry.grid(row=1, column=3)

# Item entry
tkinter.Label(frame, text="Qty").grid(row=2, column=0)
qty_spinbox = tkinter.Spinbox(frame, from_=1, to=100)
qty_spinbox.grid(row=3, column=0)

tkinter.Label(frame, text="Description").grid(row=2, column=1)
desc_entry = tkinter.Entry(frame)
desc_entry.grid(row=3, column=1)

tkinter.Label(frame, text="Unit Price").grid(row=2, column=2)
price_spinbox = tkinter.Spinbox(frame, from_=0.0, to=500, increment=0.5)
price_spinbox.grid(row=3, column=2)

tkinter.Button(frame, text="Add item", command=add_item).grid(row=4, column=2, pady=5)

# Items tree
columns = ('qty', 'desc', 'price', 'total')
tree = ttk.Treeview(frame, columns=columns, show="headings")
tree.heading('qty', text='Qty')
tree.heading('desc', text='Description')
tree.heading('price', text='Unit Price')
tree.heading('total', text="Total")
tree.grid(row=5, column=0, columnspan=4, padx=20, pady=10)

# Buttons
tkinter.Button(frame, text="Generate & Send Invoice", command=generate_and_send).grid(row=6, column=0, columnspan=4, sticky="news", padx=20, pady=5)
tkinter.Button(frame, text="New Invoice", command=new_invoice).grid(row=7, column=0, columnspan=4, sticky="news", padx=20, pady=5)

window.mainloop()
