# notice-conversions

This arose from a business need to edit a substantial number of HTML notices within a short time frame. We needed to remove all external references to CSS and images, and to instead put those directly into our HTML file.
In our case, the referenced CSS was the same for all files, and all images for the files were located in the same remote directory.

Inserting the CSS is simple, and this script will read through the contents of your remote file and insert it within a style tag after removing the reference to your external file.

Embedding images is a little more difficult. The script will first search through each HTML file within your zip to locate image tags and will find that image in the external directory. From there, it will use base64 from the Python standard library to encode each image and will place that converted tag into the proper location.

Your new files will be outputted to your desired directory.

Packages used:
* BeautifulSoup (https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Very useful for parsing HTML files in Python
