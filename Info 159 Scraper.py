import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.message import EmailMessage
import tkinter as tk

URL = "https://classes.berkeley.edu/search/class/info%20159?retain-filters=1&f%5B0%5D=im_field_term_name%3A2885&f%5B1%5D=ts_course_level%3Aup"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

def find_class(name_desired: str):
    top_classes = []
    for data in soup.find_all('div', {'data-json': True}):
        text = data['data-json']
        data_dict = eval(text.replace('false', 'False').replace('true', 'True'))
        class_name = data_dict.get('displayName')
        if class_name:
            top_classes.append(class_name)
    return any([name_desired in text for text in top_classes])

def send_email():
    file = open('private.txt')
    GMAIL_USERNAME, GMAIL_PASSWORD = file.readlines()
    GMAIL_USERNAME.strip()
    GMAIL_PASSWORD.strip()


    msg = EmailMessage()
    msg.set_content(f"Info 159 has been posted!! Go sign up! \n {URL}")

    msg['Subject'] = 'Info 159!!'
    msg['To'] = GMAIL_USERNAME

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

def update_color():
    if find_class("INFO 159"):
        canvas.config(bg="green")
        send_email()
    else:
        canvas.config(bg="red")
    # Schedule the function to run again after 5 minutes
    root.after(300000, update_color)

root = tk.Tk()
root.attributes('-fullscreen', True)
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack()

# Initial call to start the update loop
update_color()

root.mainloop()
