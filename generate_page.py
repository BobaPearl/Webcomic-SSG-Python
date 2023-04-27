# Import necessary libraries
import os
import yaml
import glob
import shutil
from datetime import datetime
from dateutil.parser import parse
from dateutil import tz
import markdown
from markdown.extensions.nl2br import Nl2BrExtension

# Define a function to read the front matter from a YAML file
def read_front_matter(filename):
    with open(filename, 'r') as f:
        # Use yaml.safe_load to parse the YAML content in the file and return the result
        return yaml.safe_load(f)

# Define a function to generate the navigation section of each HTML page
def generate_navigation(current_page, max_page_key):
    # Define a nested function to generate the URL for each page
    def page_url(page_key):
        return f'{page_key}.html'

    # Convert the current page number to an integer
    current_page_int = int(current_page)
    # Calculate the previous page key, making sure it's not less than 1
    prev_page_key = f'{max(current_page_int - 1, 1):03d}'
    # Calculate the next page key, making sure it's not greater than the maximum page key
    next_page_key = f'{min(current_page_int + 1, int(max_page_key)):03d}'

    # Return the navigation section HTML, After that create navigation section 001 is the first page, prev_page_key is the previous, next_page_key is the next, and max_page_key is the last page.
    return f'''

<div class="comicNav">
    <a href="{page_url("001")}"><img src="/img/comicnav/nav_first.png" alt="First"></a>
    <a href="{page_url(prev_page_key)}"><img src="/img/comicnav/nav_previous.png" alt="Previous"></a>
    <a href="{page_url(next_page_key)}"><img src="/img/comicnav/nav_next.png" alt="Next"></a>
    <a href="{page_url(max_page_key)}"><img src="/img/comicnav/nav_last.png" alt="Last"></a>
</div>
'''


def generate_html(front_matter, image_folder='assets'):
    last_generated_file = ""  # variable to store the last generated file

    # loop through the sorted front matter items
    for key, metadata in sorted(front_matter.items()):  
        file_prefix = key
        output_file = f"{file_prefix}.html"

        # remove the existing file if it exists
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # extract metadata for each page
        chapter = metadata['Chapter']
        title = metadata['title']
        page_number = key
        max_page_key = f'{len(front_matter):03d}'

        # convert author notes from Markdown to HTML
        author_notes_html = markdown.markdown(metadata['note'], extensions=[Nl2BrExtension()])  

        # write the HTML content to the output file
        with open(output_file, 'w') as f:
            # write the head section
            f.write('<head>\n')
            f.write('    <meta charset="UTF-8">\n')
            f.write('    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">\n')
            f.write(f'    <title>Boots - By Boba Pearl - {title}</title>\n')
            f.write('    <link href="../css/style.css" rel="stylesheet" type="text/css" media="all">\n')
            f.write('    <link rel="preconnect" href="https://fonts.googleapis.com/">\n')
            f.write('    <link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin="">\n')
            f.write('    <link href="../css/css2.css" rel="stylesheet">\n')
            f.write('</head>\n')
            
            # write the main container for the page
            f.write('<div align="center">\n')
            
            # write the header section
            f.write('<div class="writeHeader">\n')
            f.write('<header align="center">\n')
            f.write('<img src="img/logo.png" alt="">\n')
            f.write('<div id="nav">\n')
            f.write('<a href=""> Boots (current) </a> | <a href="https://bobapearlessence.com/steppe/?page_number=001"> Steppe Into The Ring </a> | <a href="rss.xml"> Rss Feed: https://bobapearlessence.com/rss.xml </a>\n')
            f.write('</div>\n')
            f.write('</header>\n')
            f.write('</div>\n')
            # Add these lines to output Chapter, Page, and Title
            # Get the chapter and page information from the front matter
            chapter = metadata['Chapter']
            page = metadata['page']

            # Write the Chapter, Page, and Title information to the output file
            f.write(f'<h1>Chapter: {chapter}</h1>\n')
            f.write(f'<h2>Page: {page}</h2>\n')
            f.write(f'<h2>Title: {title}</h2>\n')

            # Add the navigation bar to the output file
            f.write('<div class="writeNav">\n')
            f.write(generate_navigation(page_number, max_page_key))
            f.write('</div>\n')

            # Add the comic page content to the output file
            f.write('<div class="comicPage">\n')
            # Get all matching image or video files with the given file prefix
            matching_files = glob.glob(os.path.join(image_folder, f"{file_prefix}*.*"))
            # Write the matching files to the output file
            for img_path in matching_files:
                # Get the file extension of the matching file
                _, file_ext = os.path.splitext(img_path)
                if file_ext == '.mp4':
                    # If the file extension is .mp4, write a video tag to the output file
                    f.write('<div class="video-container">\n')
                    f.write(f'<video src="{img_path}" controls>\n')
                    f.write('Your browser does not support the video tag.\n')
                    f.write('</video>\n')
                    f.write('</div><br>\n')
                else:
                    # If the file extension is not .mp4, write an image tag to the output file
                    img_alt = metadata['desc']
                    f.write(f'<img src="{img_path}" alt="{img_alt}"><br>\n')
            f.write('</div>\n')

            # Add the navigation bar to the output file again
            f.write('<div class="writeNav">\n')
            f.write(generate_navigation(page_number, max_page_key))
            f.write('</div>\n')

            # Add the author's notes to the output file
            f.write('<h1>Author\'s Notes</h1>\n')
            f.write(f'<div class="authorNotes">{author_notes_html}</div>\n') # Write the HTML converted from Markdown to the file
            f.write('</div>\n')

            # Print the generated output file name
            print(f"Generated {output_file}")
            # Update the last generated file name
            last_generated_file = output_file
        
    return last_generated_file

# Check if the script is being run as the main program
if __name__ == "__main__":
    # Read front matter from the front_matter.yaml file
    front_matter = "front_matter.yaml"
    metadata = read_front_matter(front_matter)

    # Generate HTML pages
    last_generated_file = generate_html(metadata)

    # Print the last generated file
    print(f"Last generated file: {last_generated_file}")

    # Create a copy of the last generated HTML file as index.html
    shutil.copy(last_generated_file, "index.html")
    print("Created index.html")

# Time zones for converting the publication date
from_zone = tz.gettz('America/Los_Angeles')
to_zone = tz.gettz('UTC')

def generate_rss(front_matter, rss_file='rss.xml'):
    # Open the rss_file in write mode
    with open(rss_file, mode='w') as f:
        # Write the XML header
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<rss version="2.0">\n')
        f.write('    <channel>\n')

        # Write the channel information
        f.write('        <title>Boots - By Boba Pearl</title>\n')
        f.write('        <link>https://bobapearlessence.com/</link>\n')
        f.write('        <description>Boots, a webcomic by Boba Pearl.</description>\n')
        f.write('        <language>en-us</language>\n')

        # Write the items (metadata for each page)
        for key, metadata in sorted(front_matter.items(), reverse=True):
            file_prefix = key
            output_file = f"{file_prefix}.html"
            title = metadata['title']
            desc = metadata['desc']

            # Convert the publication date to the UTC time zone
            pub_date = datetime.strptime(metadata['date'], '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=from_zone).astimezone(to_zone).strftime('%a, %d %b %Y %H:%M:%S %z')

            f.write('        <item>\n')
            f.write(f'            <title>{title}</title>\n')
            f.write(f'            <link>https://bobapearlessence.com/{output_file}</link>\n')
            f.write(f'            <description>{desc}</description>\n')
            f.write(f'            <pubDate>{pub_date}</pubDate>\n')
            f.write('        </item>\n')

        # Close the channel
        f.write('    </channel>\n')
        f.write('</rss>\n')

    # Print the generated file
    print(f"Generated {rss_file}")

# Check if the code is being run as the main program
if __name__ == "__main__":
    # Read front matter from the front_matter.yaml file
    front_matter = "front_matter.yaml"
    metadata = read_front_matter(front_matter)
    
    # Generate HTML files based on the front matter data
    last_generated_file = generate_html(metadata)

    # Print the name of the last generated HTML file
    print(f"Last generated file: {last_generated_file}")

    # Create a copy of the last generated HTML file and name it index.html
    shutil.copy(last_generated_file, "index.html")
    print("Created index.html")

    # Generate the RSS feed
    generate_rss(metadata)