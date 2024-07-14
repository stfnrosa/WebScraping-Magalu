import os

email_subject = "Notebook Report"
email_html_message = """
        <!DOCTYPE html>
        <html>
        <body>
            <p>Hello, here is your report of notebooks extracted from Magazine Luiza.</p>
            <p>Best regards,</p>
            <p>Robot🤖.</p>
        </body>
        </html>
        """
recipient_email = "rosaa.estefanii@gmail.com"

excel_file_path = os.path.abspath(os.path.join('Output', 'Notebooks.xlsx'))