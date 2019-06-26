import os
import base64
from pathlib import Path
from bs4 import BeautifulSoup

source_directory = Path("path/to/html/file")
css_file = Path("path/to/css/file")
image_directory = Path("path/to/image/directory")
b64Dict = {}

# Map out dictionary key/value pairs for encoded images
for file in os.listdir(image_directory):
    with open(os.path.join(image_directory, file), 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
        b64Dict[file] = encoded_string.decode()


# Read out CSS file contents for insertion
with open(css_file, 'r') as css_file_read:
    css_contents = css_file_read.readlines()
    css_contents_str = '\n\n' + ''.join(css_contents) + '\n\n'


# Read through file, instantiate HTML soup
for file in os.listdir(source_directory):
    with open(os.path.join(Path(source_directory, file)), 'r+', encoding='utf-8') as replace_run:
        soup = BeautifulSoup(replace_run, 'html.parser')
        # Find CSS link tag and replace it with CSS file contents
        link_tag = soup.link
        if link_tag:
            style_tag = soup.new_tag('style')
            style_tag.string = css_contents_str
            link_tag.replace_with(style_tag)

        # Find all images in the file, overwrite their src with our encoded value pulled from dictionary
        # Do not replace entire image tag to retain any sizing attributes
        for image in soup.find_all('img'):
            img_src = image['src']
            dictKey = img_src.split('/')[-1]
            DictValue = b64Dict[dictKey]
            image['src'] = 'data:image/jpeg;base64,' + DictValue

    # Write new file in output directory using modified HTML soup
    with open(os.path.join(Path("path/to/fixed-notices", file)), 'w', encoding='utf-8') as replace_write:
        replace_write.write(str(soup))

