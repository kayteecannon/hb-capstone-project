
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import crud

def send_email():
  message = Mail(
      from_email='kaytee.cannon@mac.com',
      to_emails='kayteecannon@gmail.com',
      subject='Sending with Twilio SendGrid is Fun',
      html_content='''<table class="table table-hover table-striped">
        <thead>
          <tr>
              <th>Name</th>
              <th>Quantity</th>
              <th>Expiration Date</th>
              <th>Date Added</th>
          </tr>
        </thead>
        <tr>
          <td>email</td>
          <td>sent</td>
          <td>through</td>
          <td>server.py</td>
        </tr>''')

  try:
      sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
  except Exception as e:
      print(e.message)