import win32com.client as win32
import time

def send_email(subject, body, recipient, attachment_file=None):
    
    outlook = win32.Dispatch('Outlook.Application')  # Create an Outlook object
    email = outlook.CreateItem(0)

    email.Subject = subject
    email.HTMLBody = body
    email.To = recipient

    if attachment_file:
        email.Attachments.Add(attachment_file)

    email.Display()  # Show the email

    time.sleep(5)  # Wait for 5 seconds

    email.Send()   # Send the email 

    print("Email sent successfully!")
