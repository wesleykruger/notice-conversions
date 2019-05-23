import os
import shutil
import base64
from pathlib import Path
from bs4 import BeautifulSoup

source_directory = Path("C:/Users/wesleykruger/Documents/BBVA/notice-external-ref/notices")
css_file = Path("C:/Users/wesleykruger/Documents/BBVA/notice-external-ref/letter.css")
image_directory = Path("C:/Users/wesleykruger/Documents/BBVA/notice-external-ref/LetterImages")
b64Dict = {}

for file in os.listdir(image_directory):
    with open(os.path.join(image_directory, file), 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
        b64Dict[file] = encoded_string.decode()


with open(css_file, 'r') as css_file_read:
    css_contents = css_file_read.readlines()
    css_contents_str = '\n\n' + ''.join(css_contents) + '\n\n'


for file in os.listdir(source_directory):
    with open(os.path.join(Path(source_directory, file)), 'r+', encoding='utf-8') as replace_run:
        soup = BeautifulSoup(replace_run, 'html.parser')
        link_tag = soup.link
        if link_tag:
            style_tag = soup.new_tag('style')
            style_tag.string = css_contents_str
            link_tag.replace_with(style_tag)

        for image in soup.find_all('img'):
            img_src = image['src']
            dictKey = img_src.split('/')[-1]
            DictValue = b64Dict[dictKey]
            b64_tag = soup.new_tag('img')
            b64_tag['src'] = 'data:image/jpeg;base64,' + DictValue
            image['src'] = 'data:image/jpeg;base64,' + DictValue

        for image in soup.find_all('img'):
            print(image)

    with open(os.path.join(Path("C:/Users/wesleykruger/Documents/BBVA/notice-external-ref/fixed-notices", file)), 'w', encoding='utf-8') as replace_write:
        replace_write.write(str(soup))

