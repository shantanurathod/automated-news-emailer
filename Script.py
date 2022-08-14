import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from bs4 import BeautifulSoup  # Web scraping
from cgitb import html
from urllib import response
import requests  # for http repuests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import sys
import maskpass

if(len(sys.argv) < 2):
    print("Enter email address with run command")
    exit()

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Send the email
# mail body
# system date and time manipulation

now = datetime.datetime.now()

# email content placeholder
content = ''

# extract news from Hacker News Stories


def extract_news(url):
    print("Extracting News from Hacker News Stories...")
    cnt = ''
    cnt += ('<b>HN Top Stories:</b>\n' + '<br>' + '-'*50 + '<br>')
    response = session.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        cnt += ((str(i+1)+' :: '+tag.text + "\n" + '<br>')
                if tag.text != 'More' else '')

    return(cnt)


cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>-------------<br>')
content += ('<br><br>End of Message')

# send the email

print("Composing Email...")

# update your email details

SERVER = 'smtp.gmail.com'  # your email server
PORT = 587  # your port number
FROM = ''  # your email id
TO = sys.argv[-1]  # to email id's, can be a list
PASS = maskpass.askpass(mask="*")  # your email id's password

msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories HN [Automated Mail]' + ' ' + \
    str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initialising Server...')

server = smtplib.SMTP_SSL(SERVER, 465)

server.set_debuglevel(1)
server.ehlo
server.starttls

server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email sent...')

server.quit()
