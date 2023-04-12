import os
import json

def generate_page(lang: str, path: str, cwd: str):
    ''' Generates the webpage using the file "template.html"
    in cwd, applying the language of lang using the replacements
    of a respective json file and copies the generated page to path. '''
    # get json
    with open("/".join([cwd, lang + ".json"]), "r") as json_file:
        lang_code = json.loads(json_file.read())

        with open("/".join([cwd, "template.html"])) as template_file:
            page_content = template_file.read()
            for hotword in lang_code.keys():
                page_content = page_content.replace(hotword, lang_code[hotword])

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

