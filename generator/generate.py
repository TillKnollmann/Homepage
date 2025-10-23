import os
import json

tag_hotwords = ["$about-text$", "$contact-text$"]

def generate_projects_html(projects):
    ''' Generates HTML for project cards from project data '''
    html_parts = []
    for project in projects:
        card_html = f'''<div class="col-md-6 mb-3"><div class="card h-100"><div class="card-body"><h5 class="card-title">{project['title']}</h5><p class="card-text">{project['description']}</p><a href="{project['url']}" target="_blank" class="btn btn-secondary">{project['button_text']}</a></div></div></div>'''
        html_parts.append(card_html)
    return ''.join(html_parts)

def generate_page(lang: str, path: str, cwd: str):
    ''' Generates the webpage using the file "template.html"
    in cwd, applying the language of lang using the replacements
    of a respective json file and copies the generated page to path.
    Additionally, tags hotwords in tag_hotwords with links defined by tags.json '''
    # get tags
    with open("/".join([cwd, "tags.json"]), "r") as tags:
        tags_content = json.loads(tags.read())
        # get json of localization
        with open("/".join([cwd, lang + ".json"]), "r") as json_file:
            lang_code = json.loads(json_file.read())

            with open("/".join([cwd, "template.html"])) as template_file:
                page_content = template_file.read()

                # plugin local text into template
                for hotword in lang_code.keys():

                    to_plug_in = lang_code[hotword]
                    
                    # Special handling for projects array
                    if hotword == "$projects$":
                        to_plug_in = generate_projects_html(to_plug_in)
                        page_content = page_content.replace("$projects-content$", to_plug_in)
                        continue

                    if hotword in tag_hotwords:
                        # tag text to be plugged in
                        for tag in tags_content.keys():
                            to_plug_in = to_plug_in.replace(tag, "<a target=\"_blank\" href=\"" + tags_content[tag] + "\">" + tag + "</a>")

                    page_content = page_content.replace(hotword, to_plug_in)

                # store the content
                if not os.path.exists(path):
                    os.makedirs(path)
                with open("/".join([path, "index.html"]), 'wt', encoding='utf-8') as target:
                    target.write(page_content)


cwd = os.getcwd()

languages = ["de", "en"]

paths = ["/".join(cwd.split("/")[:-1] + [lang]) for lang in languages]

for i in range(2):
    generate_page(languages[i], paths[i], cwd )

