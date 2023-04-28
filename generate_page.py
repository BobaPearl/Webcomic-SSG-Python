import os
import yaml
import glob
import shutil
import markdown
from datetime import datetime
from dateutil.parser import parse
from dateutil import tz
from markdown.extensions.nl2br import Nl2BrExtension

def read_front_matter(filename):
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading front matter file: {e}")
        return None

def read_site_info(filename):
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading site info file: {e}")
        return None


def generate_navigation(current_page, max_page_key):
    def page_url(page_key):
        return f'{page_key}.html'

    current_page_int = int(current_page)
    prev_page_key = f'{max(current_page_int - 1, 1):03d}'
    next_page_key = f'{min(current_page_int + 1, int(max_page_key)):03d}'

    return f'''
<div class="comicNav">
    <a href="{page_url("001")}"><img src="/img/comicnav/nav_first.png" alt="First"></a>
    <a href="{page_url(prev_page_key)}"><img src="/img/comicnav/nav_previous.png" alt="Previous"></a>
    <a href="{page_url(next_page_key)}"><img src="/img/comicnav/nav_next.png" alt="Next"></a>
    <a href="{page_url(max_page_key)}"><img src="/img/comicnav/nav_last.png" alt="Last"></a>
</div>
'''

def generate_html(front_matter, site_info, image_folder='assets'):
    last_generated_file = ""
    for key, metadata in sorted(front_matter.items()):  # Make sure the front_matter items are sorted
        file_prefix = key
        output_file = f"{file_prefix}.html"
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except OSError as e:
                print(f"Error deleting file {output_file}: {e}")
                continue  # Skip this iteration and move to the next key

        chapter = metadata['Chapter']
        title = metadata['title']
        page_number = key
        max_page_key = f'{len(front_matter):03d}'
        author_notes_html = markdown.markdown(metadata['note'], extensions=[Nl2BrExtension()])  # Convert the Markdown to HTML
        
        try:
            with open(output_file, 'w') as f:
                # <head> section
                f.write('<head>\n')
                f.write('    <meta charset="UTF-8">\n')
                f.write('    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">\n')
                # Replace hardcoded values with site_info values
                f.write(f'    <title>{site_info["title"]} - By {site_info["author"]} - {title}</title>\n')
                f.write('    <link href="../css/style.css" rel="stylesheet" type="text/css" media="all">\n')
                f.write('    <link rel="preconnect" href="https://fonts.googleapis.com/">\n')
                f.write('    <link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin="">\n')
                f.write('    <link href="../css/css2.css" rel="stylesheet">\n')
                f.write('</head>\n')
                
                f.write('<div align="center">\n')

                # <header> section
                f.write('<div class="writeHeader">\n')
                f.write('<header align="center">\n')
                f.write('<img src="img/logo.png" alt="">\n')
                f.write('<div id="nav">\n')
                # ADD PAGES HERE
                f.write(f'<a href=""> Home </a> | <a href="{site_info["domain"]}/some_other_page"> Some Other Page </a> | <a href="rss.xml"> Rss Feed: {site_info["domain"]}/rss.xml </a>\n')               
                f.write('</header>\n')
                f.write('</div>\n')
                
                # Add these lines to output Chapter, Page, and Title
                chapter = metadata['Chapter']
                page = metadata['page']
                f.write(f'<h1>Chapter: {chapter}</h1>\n')
                f.write(f'<h2>Page: {page}</h2>\n')
                f.write(f'<h2>Title: {title}</h2>\n')
                f.write('<div class="writeNav">\n')
                f.write(generate_navigation(page_number, max_page_key))
                f.write('</div>\n')
                f.write('<div class="comicPage">\n')

                matching_files = glob.glob(os.path.join(image_folder, f"{file_prefix}*.*"))
                for img_path in matching_files:
                    _, file_ext = os.path.splitext(img_path)
                    if file_ext == '.mp4':
                        f.write(f'<video src="{img_path}" controls>\n')
                        f.write(f'Your browser does not support the video tag.\n')
                        f.write(f'</video><br>\n')
                    else:
                        img_alt = metadata['desc']
                        f.write(f'<img src="{img_path}" alt="{img_alt}"><br>\n')

                f.write('</div>\n')

                f.write('<div class="writeNav">\n')
                f.write(generate_navigation(page_number, max_page_key))
                f.write('</div>\n')

                f.write('<h1>Author\'s Notes</h1>\n')
                f.write(f'<div class="authorNotes">{author_notes_html}</div>\n')  # Write the HTML converted from Markdown to the file
                f.write('</div>\n')

        except Exception as e:
            print(f"Error generating {output_file}: {e}")
            continue  # Skip this iteration and move to the next key

        print(f"Generated {output_file}")
        last_generated_file = output_file

    return last_generated_file


from_zone = tz.gettz('America/Los_Angeles')
to_zone = tz.gettz('UTC')

def generate_rss(front_matter, rss_file='rss.xml'):
    with open(rss_file, mode='w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<rss version="2.0">\n')
        f.write('    <channel>\n')
        f.write(f'        <title>{site_info["title"]} - By {site_info["author"]}</title>\n')
        f.write(f'        <link>{site_info["domain"]}</link>\n')
        f.write(f'        <description>{site_info["title"]}, a webcomic by {site_info["author"]}.</description>\n')
        f.write('        <language>en-us</language>\n')

        for key, metadata in sorted(front_matter.items(), reverse=True):
            file_prefix = key
            output_file = f"{file_prefix}.html"
            title = metadata['title']
            desc = metadata['desc']
            pub_date = datetime.strptime(metadata['date'], '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=from_zone).astimezone(to_zone).strftime('%a, %d %b %Y %H:%M:%S %z')

            f.write('        <item>\n')
            f.write(f'            <title>{title}</title>\n')
            f.write(f'            <link>{site_info["domain"]}/{output_file}</link>\n')
            f.write(f'            <description>{desc}</description>\n')
            f.write(f'            <pubDate>{pub_date}</pubDate>\n')
            f.write('        </item>\n')

        f.write('    </channel>\n')
        f.write('</rss>\n')

    print(f"Generated {rss_file}")

site_info = read_site_info("site_info.yaml")

if __name__ == "__main__":
       front_matter = "front_matter.yaml"
       metadata = read_front_matter(front_matter)
       last_generated_file = generate_html(metadata, site_info)
       # Print the last generated file
       print(f"Last generated file: {last_generated_file}")

       # Create a copy of the last generated HTML file as index.html
       try:
           shutil.copy(last_generated_file, "index.html")
           print("Created index.html")
       except shutil.Error as e:
           print(f"Error creating index.html: {e}")

        # Generate RSS feed
       generate_rss(metadata)

