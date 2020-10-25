from PIL import Image
from urllib.request import urlopen
import requests

imgcounter = 1
basename = "image%s.png"

def text_previewer(url):
    response = urlopen(url)
    html = response.read()
    return html.decode('utf-8')

def image_downloader(url, format):
    img_data = requests.get(url).content
    with open(basename % imgcounter, 'wb') as handler:
        handler.write(img_data)
