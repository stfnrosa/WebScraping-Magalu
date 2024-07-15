import os

email_subject = "Relatório Notebooks"
email_html_message = """
        <!DOCTYPE html>
        <html>
        <body>
            <p>Olá, aqui está o seu relatório dos notebooks extraídos da Magazine Luiza</p>
            <p>Atenciosamente,</p>
            <p>Robô🤖.</p>
        </body>
        </html>
        """
recipient_email = "rosaa.estefanii@gmail.com"

excel_file_path = os.path.abspath(os.path.join('Output', 'Notebooks.xlsx'))