import os
import json
from projects_generator import generate_projects_html

tag_hotwords = ["$about-text$", "$contact-text$", "group_description"]


def apply_tags(value: str, tags_content: dict) -> str:
    """
    Replace all tag keys with HTML links in the given value.
    """
    for tag in tags_content.keys():
        value = value.replace(
            tag,
            f'<a target="_blank" href="{tags_content[tag]}">{tag}</a>'
        )
    return value


def apply_tags_to_lang_code(lang_code: dict, tags_content: dict) -> dict:
    """
    Recursively apply tags to all hotword keys in the language code JSON,
    regardless of their depth in the object structure.
    """
    def process_value(value):
        """Recursively process a value, applying tags where needed."""
        if isinstance(value, dict):
            for key, val in value.items():
                if key in tag_hotwords and isinstance(val, str):
                    # Apply tags to this value
                    value[key] = apply_tags(val, tags_content)
                else:
                    # Recurse into nested structures
                    value[key] = process_value(val)
            return value
        elif isinstance(value, list):
            return [process_value(item) for item in value]
        else:
            return value

    return process_value(lang_code)


def generate_page(lang: str, path: str, cwd: str):
    """
    Generates the webpage using the file "template.html" in cwd,
    applying the language of lang using the replacements
    of a respective json file and copies the generated page to path.

    Process:
    1. Load tags.json
    2. Load lang.json
    3. Apply tags to hotwords in the JSON
    4. Load template.html
    5. Replace all placeholders with localized content
    6. Generate and insert projects HTML
    7. Write to file
    """
    with open("/".join([cwd, "tags.json"]), "r") as tags_file:
        tags_content = json.loads(tags_file.read())

    with open("/".join([cwd, lang + ".json"]), "r") as json_file:
        lang_code = json.loads(json_file.read())

    lang_code = apply_tags_to_lang_code(lang_code, tags_content)

    with open("/".join([cwd, "template.html"])) as template_file:
        page_content = template_file.read()

    for key in lang_code.keys():
        value = lang_code[key]

        # Special handling for projects dictionary
        if key == "$projects$":
            projects_html = generate_projects_html(value, cwd)
            page_content = page_content.replace(
                "$projects-content$", projects_html)
            continue

        page_content = page_content.replace(key, str(value))

    if not os.path.exists(path):
        os.makedirs(path)
    with open("/".join([path, "index.html"]), 'wt', encoding='utf-8') as target:
        target.write(page_content)


cwd = os.getcwd()

languages = ["de", "en"]

paths = ["/".join(cwd.split("/")[:-1] + [lang]) for lang in languages]

for i in range(2):
    generate_page(languages[i], paths[i], cwd)
