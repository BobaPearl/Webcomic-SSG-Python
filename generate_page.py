import os
import yaml
import glob
import shutil
import markdown
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
from dateutil import tz
from markdown.extensions.nl2br import Nl2BrExtension

COMICS = ['boots', 'queen']  # List of comics

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
    
def read_header_links(filename):
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading header links file: {e}")
        return None
def read_custom_html(filename):
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: 'custom_html.yaml' file not found. Skipping custom HTML insertion.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error: Improperly formatted 'custom_html.yaml'. Skipping custom HTML insertion. Details: {e}")
        return {}
# Read YAML file and return a list of dictionaries
def read_yaml_file(filename):
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return None

# Usage example:
#custom_html_data = read_custom_html("custom_html.yaml")

# Generate a string of HTML for navigation
def generate_navigation_yaml(yaml_data):
    nav_html = '<div id="nav">\n'
    comic_links = []
    other_links = []
    for item in yaml_data:
        if item.get('is_comic', False):
            comic_name = item['name']
            comic_link = item['link']
            has_archives = item.get('has_archives', False)
            comic_links.append(f'<a href="{comic_link}"> {comic_name} </a>{" | " if has_archives else ""}<a href="{comic_link}/archive.html">Archives</a>' if has_archives else f'<a href="{comic_link}"> {comic_name} </a>')
        else:
            other_links.append(f'<a href="{item["link"]}"> {item["name"]} </a> | ')
    if comic_links:
        nav_html += '<div class="dropdown">\n'
        nav_html += '<button onclick="myFunction()" class="dropbtn">Comics</button>\n'
        nav_html += '<div id="myDropdown" class="dropdown-content">\n'
        for link in comic_links:
            nav_html += link + ' | '
        nav_html = nav_html.rstrip(' | ')  # remove the trailing separator
        nav_html += '\n</div>\n</div> | '
    for link in other_links:
        nav_html += link
    nav_html = nav_html.rstrip(' | ')  # remove the trailing separator
    nav_html += '\n</div>'
    return nav_html


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

def generate_html(front_matter, site_info, comic_name, image_folder='assets'):
    custom_html_data = read_custom_html(f"{comic_name}/custom_html.yaml")
    header_links = read_header_links("header.yaml")
    last_generated_file = ""
    for key, metadata in sorted(front_matter.items()): # Make sure the front_matter items are sorted
        file_prefix = key
        output_file = f"{comic_name}/{file_prefix}.html"
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except OSError as e:
                print(f"Error deleting file {output_file}: {e}")
                continue # Skip this iteration and move to the next key

        chapter = metadata['Chapter']
        title = metadata['title']
        desc = metadata['desc']
        image_filename = metadata['image_filename']
        page_number = key
        max_page_key = f'{len(front_matter):03d}'
        author_notes_html = markdown.markdown(metadata['note'], extensions=[Nl2BrExtension()]) # Convert the Markdown to HTML

        try:
            with open(output_file, 'w') as f:
                print(f"Generating {desc}...")
                f.write('  <head>\n')
                f.write('    <meta charset="UTF-8">\n')
                f.write('    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">\n')
                f.write(f'    <title>{site_info["title"]} - By {site_info["author"]} - {title}</title>\n')
                f.write(f'    <meta property="og:title" content="{title}">\n')
                f.write(f'    <meta property="og:description" content="{desc}">\n')
                f.write(f'    <meta property="og:image" content="https://bobapearlessence.com/assets/{image_filename}">\n')
                f.write(f'    <meta property="og:url" content="https://bobapearlessence.com/{output_file}">\n')
                f.write(f'    <meta name="twitter:card" content="summary_large_image">\n')
                f.write(f'    <meta name="twitter:title" content="{title}">\n')
                f.write(f'    <meta name="twitter:description" content="{desc}">\n')
                f.write(f'    <meta name="twitter:image" content="https://bobapearlessence.com/assets/{image_filename}">\n')
                f.write('    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">\n')
                f.write('    <script src="https://bobapearlessence.com/js/dropdown.js"></script>\n')
                f.write('    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js" crossorigin="anonymous"></script>\n')
                f.write('    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>\n')
                f.write('    <link href="https://cdnjs.cloudflare.com/ajax/libs/ekko-lightbox/5.3.0/ekko-lightbox.css" rel="stylesheet" crossorigin="anonymous">\n')
                f.write('    <script src="https://cdnjs.cloudflare.com/ajax/libs/ekko-lightbox/5.3.0/ekko-lightbox.js" crossorigin="anonymous"></script>\n')
                f.write('    <link href="https://bobapearlessence.com/css/style.css" rel="stylesheet">\n')
                f.write('    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>\n')
                f.write('    <link rel="preconnect" href="https://fonts.googleapis.com/">\n')
                f.write('    <link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin="">\n')
                f.write('  </head>\n')
                f.write('<body>\n')
                f.write('<div align="center">\n')

                # <header> section
                f.write('<div class="writeHeader">\n')
                f.write('<header align="center">\n')
                f.write('<a href="https://bobapearlessence.com/"><img src="img/logo.png" alt=""></a>\n')
                f.write('<div id="nav">\n')
                f.write('</div>\n')
                f.write('</div>\n')
                
                # Add these lines to output Chapter, Page, and Title
                chapter = metadata['Chapter']
                page = metadata['page']
                f.write('<body>')
                f.write(f'<h1>Chapter: {chapter}</h1>\n')
                f.write(f'<h2>Page: {page}</h2>\n')
                f.write(f'<h2>Title: {title}</h2>\n')
                
                if metadata.get('noteaspage', 'false') == 'true':
                    f.write('<div class="writeNav">\n')
                    f.write(generate_navigation(page_number, max_page_key))
                    f.write('</div>\n')
                    f.write('<div class="comicPage">\n')
                    f.write(author_notes_html)
                    f.write('</div>\n')
                    f.write('<div class="writeNav">\n')
                    f.write(generate_navigation(page_number, max_page_key))
                    f.write('</div>\n')
                    f.write('</body>\n')
                else:
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
                            f.write(f'</video>\n')
                            f.write(f'</br>')
                        if file_ext == '.jpg' or file_ext == '.jpeg' or file_ext == '.png' or file_ext == '.gif' or file_ext == '.webp' or file_ext == '.svg' or file_ext == '.bmp':
                            f.write(f'<img src="{img_path}" alt="">\n')
                            f.write(f'</br>')
                    print(f"Matching files: {matching_files}")

                        


                    f.write('</div>\n')

                    f.write('<div class="writeNav">\n')
                    f.write(generate_navigation(page_number, max_page_key))
                    f.write('</div>\n')

                    f.write('<h1>Author\'s Notes</h1>\n')
                    # Add custom HTML if the current page has a matching key in custom_html_data
                    if str(page_number) in custom_html_data:
                        f.write(custom_html_data[str(page_number)]['html'])

                    f.write('<div class="authorNotes">\n')
                    f.write(f'{author_notes_html}\n')
                    f.write('</div>\n')
                    f.write('</body>\n')


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
            f.write(f'            <link>{output_file}</link>\n')
            f.write(f'            <description>{"desc"}</description>\n')
            f.write(f'            <pubDate>{pub_date}</pubDate>\n')
            f.write('        </item>\n')

        f.write('    </channel>\n')
        f.write('</rss>\n')

    print(f"Generated {rss_file}")


def generate_archive(front_matter, site_info, comic_name):
    try:
        with open(f"{comic_name}/archive.html", 'w') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<html>\n')
            f.write('  <head>\n')
            f.write('    <meta charset="UTF-8">\n')
            f.write('    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">\n')
            f.write(f'    <title>{site_info["title"]} - By {site_info["author"]} - Archives</title>\n')
            f.write('    <link rel="stylesheet" href="https://bobapearlessence.com/css/style.css">\n')
            f.write('    <script src="https://bobapearlessence.com/js/dropdown.js"></script>\n')
            f.write('    <link href="https://fonts.googleapis.com/css?family=Mali&display=swap" rel="stylesheet">\n')
            f.write('  </head>\n')
            f.write('<body>\n')

            # <header> section
            f.write('<header>\n')
            f.write('  <div id="nav">\n')
            f.write('    <a href="index.html"><img src="img/logo.png" alt=""></a>\n')
            f.write('  </div>\n')
            f.write('</header>\n')

            f.write('<main>\n')
            f.write('  <section>\n')
            f.write('    <article>\n')
            f.write('      <div class="subPage archivePage">\n')
            f.write('        <table class="archiveTable">\n')

            # Table headers
            f.write('          <tr>\n')
            f.write('            <th>Chapter</th>\n')
            f.write('            <th>Title</th>\n')
            f.write('            <th>Description</th>\n')
            f.write('          </tr>\n')

            for key, metadata in sorted(front_matter.items()):
                file_prefix = key
                output_file = f"{file_prefix}.html"
                chapter = metadata['Chapter']
                title = metadata['title']
                desc = metadata['desc']

                f.write('          <tr>\n')
                f.write(f'            <td><a href="{output_file}">{chapter}</a></td>\n')
                f.write(f'            <td><a href="{output_file}">{title}</a></td>\n')
                f.write(f'            <td>{desc}</td>\n')
                f.write('          </tr>\n')

            f.write('        </table>\n')  # Close table
            f.write('      </div>\n')  # Close .subPage
            f.write('    </article>\n')
            f.write('  </section>\n')
            f.write('</main>\n')

            f.write('<script>\n')
            f.write('document.querySelectorAll(".archiveTable tr").forEach(row => {\n')
            f.write('  row.addEventListener("click", () => {\n')
            f.write('    const href = row.querySelector("a").getAttribute("href");\n')
            f.write('    window.location.href = href;\n')
            f.write('  });\n')
            f.write('});\n')
            f.write('</script>\n')
            f.write('</body>\n')
            f.write('</html>\n')


        print("Generated archive.html")
    except Exception as e:
        print(f"Error generating archive.html: {e}")

    
# Replace the navigation section in an HTML file
def replace_nav_in_html(html_file, new_nav_html):
    try:
        with open(html_file, 'r+') as f:
            soup = BeautifulSoup(f, 'html.parser')
            nav_div = soup.find('div', {'id': 'nav'})
            if nav_div:
                nav_div.replace_with(BeautifulSoup(new_nav_html, 'html.parser'))
            else:
                print(f"No 'div' with id 'nav' found in {html_file}. Skipping...")
                return
            # Write the modified HTML back to the file
            f.seek(0)
            f.write(str(soup))
            f.truncate()
        print(f"Replaced navigation in {html_file}")
    except Exception as e:
        print(f"Error processing {html_file}: {e}")

site_info = read_site_info("site_info.yaml")

if __name__ == "__main__":
    for comic in COMICS:
        os.makedirs(comic, exist_ok=True) # Ensure the directory for the comic exists
        site_info = read_site_info(f"{comic}/site_info.yaml")
        front_matter = read_yaml_file(f"{comic}/front_matter.yaml")
        last_generated_file = generate_html(front_matter, site_info, comic)
        print(f"Last generated file: {last_generated_file}")
        try:
            shutil.copy(last_generated_file, f"{comic}/index.html")
            print(f"Created {comic}/index.html")
        except shutil.Error as e:
            print(f"Error creating {comic}/index.html: {e}")
        generate_rss(front_matter)
        generate_archive(front_matter, site_info, comic)
        nav_yaml_file = f'header.yaml'
        nav_yaml_data = read_header_links(nav_yaml_file)
        new_nav_html = generate_navigation_yaml(nav_yaml_data)
        html_files = glob.glob(f"{comic}/*.html")
        for html_file in html_files:
            replace_nav_in_html(html_file, new_nav_html)