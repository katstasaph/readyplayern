'''
Created on Nov 30, 2020

@author: katherine
'''
import webbrowser
from webbrowser import open_new_tab

def create_html_page(content):
    url_name = "test.html"
    f = open(url_name,'w+')

    html_code = f"""<html>
    <head>
    <title>Ready Player n</title>
    </head>
    <body><div style="white-space: pre-wrap;">{content}</div>
    </html>"""

    f.write(html_code)
    f.close()

    open_new_tab(url_name)