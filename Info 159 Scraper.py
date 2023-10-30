import numpy as np
import requests
from bs4 import BeautifulSoup

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

print(find_class("INFO 159"))
