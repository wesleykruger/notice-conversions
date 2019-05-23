import os
import fnmatch
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
        print(type(image_file))
        encoded_string = base64.b64encode(image_file.read())
        b64Dict[file] = encoded_string.decode()


with open(css_file, 'r') as f1:
    css_contents = f1.readlines()
    css_contents_str = '\n\n' + ''.join(css_contents) + '\n\n'


for file in os.listdir(source_directory):
    count = 0
    with open(os.path.join(Path(source_directory, file)), 'r', encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
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
            #print(image)
            #print(dictKey)
            #print(b64_tag)
            #image.replace_with(b64_tag)
            count +=1
            if count > 1:
                print(file)

