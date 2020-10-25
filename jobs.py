from urllib.request import urlopen
import requests

def text_previewer(url):
    response = urlopen(url)
    html = response.read()
    return html.decode('utf-8')