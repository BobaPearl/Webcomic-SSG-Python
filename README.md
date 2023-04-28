Getting Started with the Python Webcomic Generator Script
=========================================================

Prerequisites
-------------

-   Python: You need to have Python installed on your computer to run this script. You can download Python from[ https://www.python.org/downloads/](https://www.python.org/downloads/)

-   Required Libraries: The script uses several libraries including os, yaml, glob, shutil, datetime, dateutil, and markdown. You can install these libraries using the following command in your terminal or command prompt:

### pip install os yaml glob shutil datetime python-dateutil markdown

Steps to Set Up Your Webcomic Project
-------------------------------------

1.  Create a Project Folder: Create a new folder for your website project and open it in your terminal or command prompt.

2.  Copy the Script: Copy the provided script and save it as generate_html.py in your project folder.

3.  Copy the Front Matter File: Copy the front_matter.yaml file and save it in your project folder. This file contains the metadata for each page of your webcomic.

4.  Copy the Site Info file: Copy the site_info.yaml file and save it in your project folder. This file contains the site info for your entire site.

5.  Copy the header file: Copy the header.yaml file and save it in your project folder. If you have more then just your comic link, this puts those links in every page. Note you will have to create the HTML file for the new page, and put the header at the top. Here is my header for an example

```
<div id="nav">
<a href="https://bobapearlessence.com"> Home </a> | <a href="https://bobapearlessence.com/steppe"> Steppe into the ring (Abandonded) </a> | <a href="https://bobapearlessence.com/voices.html"> Character voices </a> | <a href="https://bobapearlessence.com/rss.xml"> RSS Feed </a>
</header>
```

Which shows up as 

<div id="nav">
<a href="https://bobapearlessence.com"> Home </a> | <a href="https://bobapearlessence.com/steppe"> Steppe into the ring (Abandonded) </a> | <a href="https://bobapearlessence.com/voices.html"> Character voices </a> | <a href="https://bobapearlessence.com/rss.xml"> RSS Feed </a>
</header>

You can edit this by looking at:

```                for link in header_links:
                    f.write(f'<a href="{site_info["domain"]}{link["link"]}"> {link["name"]} </a> | ')
```
in the code (at time of writing lines 96 and 97) What ever you put in the code after the and before the links will be added.

6. The img/comicnav contains the files for your arrows, retain the naming structure, or edit the script for the new names, it's all commented

7. The css folder contains styles.css this one is your main style sheet.

8. Assets is where your comics go, the prefix has to match the key of the comic in the front_matter file, and the keys always have to be a 3 digit number so 001 002 003 etc. etc.

9. You're going to want to change the site info to your comic's name, your author name, and the like. It's all pretty clear, but the format for the website needs to be like you were actually accessing the homepage. So whatever your domain is.

10.  Run the Script: In your terminal or command prompt, navigate to your project folder and run the following command:

### python generate_html.py

This will generate HTML files based on the front matter data and an RSS feed. 8. Upload the Files: Upload all the generated files, the images, and the CSS files to your website hosting service.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Explanation of the Python Script
================================

The script is designed to generate HTML pages and an RSS feed for a webcomic. It first imports several necessary modules: os, yaml, glob, shutil, datetime, dateutil, and markdown.

### read_front_matter(filename)

This function takes a filename as an input and reads its contents, which are in YAML format, and returns the parsed data. The file is opened with the with statement, which automatically closes the file after it has been read.

### generate_navigation(current_page, max_page_key)

This function generates the navigation section of the HTML pages. It takes two arguments: current_page and max_page_key. current_page is the page number of the current page being generated, and max_page_key is the maximum page number in the comic. The function first defines a local function page_url(page_key) which takes a page key as an argument and returns the URL of the page. The function then calculates the previous page key and the next page key using the current_page argument and the max_page_key argument. Finally, it returns a string of HTML code for the navigation section, which includes links to the first page, previous page, next page, and last page of the comic.

### generate_html(front_matter, image_folder='assets')

This function takes two arguments: front_matter and image_folder. front_matter is a dictionary of metadata for each page of the comic, and image_folder is the folder that contains the images for the pages. The function first sets the last_generated_file variable to an empty string. Then it sorts the items in the front_matter dictionary and loops through each item, which is a page of the comic. For each page, the function creates an HTML file with the same name as the page key, removes the file if it already exists, and writes the content of the HTML file. The content includes the head section, which contains the meta information for the HTML page and the CSS stylesheets, the header section, which contains the logo and navigation links, the chapter, page, and title sections, the navigation section, which is generated by the generate_navigation() function, the images for the page, and the author's notes section, which is converted from Markdown to HTML using the markdown library. The function returns the name of the last generated file.

The if name == "main": statement at the bottom of the script is a special statement in Python that allows the script to be run as a standalone program. When the script is run, it reads the front matter from the front_matter.yaml file, generates the HTML pages, prints the name of the last generated file, creates a copy of the last generated file as index.html, and generates the RSS.
