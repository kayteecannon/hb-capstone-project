
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import crud
import datetime

style_string = """<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>"""

from_email_test = os.environ['FROM_EMAIL_TEST']
to_email_test = os.environ['TO_EMAIL_TEST']

date_sent = datetime.datetime.now()
formatted_date = date_sent.strftime('%B %d, %Y')

def send_email(html_string):
  message = Mail(
      from_email=from_email_test,
      to_emails=to_email_test,
      subject='Fill Me Inventory - Expiration Report',
      html_content=f"""<!DOCTYPE html>
                    <html>
                    {style_string}
                    <body>
                    <h1 style="font-family: 'Francois One', sans-serif; text-align: center">Fill Me Inventory Report - {formatted_date}</h1>
                    <h2 style="font-family: 'Roboto', sans-serif; text-align: center">Items Expiring in the Next 30 Days</h2>

                    <table style="font-family: arial, sans-serif;
                        border-collapse: collapse;
                        width: 100%;">
                    <thead>
                    <tr style="font-family: 'Roboto', sans-serif;">
                        <th>Item</th>
                        <th>Quantity</th>
                        <th>Expiration Date</th>
                        <th>Date Added</th>
                    </tr>
                    </thead>
                    {html_string}
                    </table>
                    </body>
                    </html>""")

  try:
      sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
  except Exception as e:
      print(e.message)

def send_initial_email(html_string, email_frequency, next_run_date):
  message = Mail(
      from_email=from_email_test,
      to_emails=to_email_test,
      subject='Fill Me Inventory - Expiration Report Scheduled',
      html_content=f"""<!DOCTYPE html>
                    <html>
                    {style_string}
                    <body>
                    <h1 style="font-family: 'Francois One', sans-serif; text-align: center">Fill Me Inventory Report - {formatted_date}</h1>
                    <p>You have scheduled an expiration report email to arrive every {email_frequency} days starting on {next_run_date}.</p>
                    <p>Below is your expiration report for today, {formatted_date}.</p>
                    <h2 style="font-family: 'Roboto', sans-serif; text-align: center">Items Expiring in the Next 30 Days</h2>
                    <table style="font-family: arial, sans-serif;
                        border-collapse: collapse;
                        width: 100%;">
                    <thead>
                    <tr style="font-family: 'Roboto', sans-serif;">
                        <th>Item</th>
                        <th>Quantity</th>
                        <th>Expiration Date</th>
                        <th>Date Added</th>
                    </tr>
                    </thead>
                    {html_string}
                    </table>
                    </body>
                    </html>""")

  try:
      sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
  except Exception as e:
      print(e.message)