"""
Projects Generator Module
Handles the generation of project sections with grouping and enhanced visuals
"""

import os
import html as html_lib
from typing import Dict, Optional

# Template marker constants
CARD_START_MARKER = '<!--PROJECT_CARD_START-->'
CARD_END_MARKER = '<!--PROJECT_CARD_END-->'
IMAGE_START_MARKER = '<!--IMAGE_SECTION_START-->'
IMAGE_END_MARKER = '<!--IMAGE_SECTION_END-->'
GROUP_START_MARKER = '<!--PROJECT_GROUP_START-->'
GROUP_END_MARKER = '<!--PROJECT_GROUP_END-->'

# Template cache for performance
_template_cache = {}


def escape_html(text: str) -> str:
    """
    Escape HTML special characters for security.

    Args:
        text: Raw text string that may contain HTML special characters

    Returns:
        HTML-escaped string safe for insertion into HTML
    """
    return html_lib.escape(text)


def validate_project(project: Dict) -> None:
    """
    Validate that a project has all required fields.

    Args:
        project: Project dictionary to validate

    Raises:
        ValueError: If required fields are missing
    """
    required_fields = ['title', 'description', 'url', 'button_text']
    missing = [field for field in required_fields if field not in project]

    if missing:
        raise ValueError(
            f"Project missing required fields: {', '.join(missing)}")


def load_projects_template(template_path: str) -> str:
    """
    Load the projects HTML template with caching.

    Args:
        template_path: Path to the template file

    Returns:
        Template content as string
    """
    if template_path not in _template_cache:
        with open(template_path, 'r', encoding='utf-8') as f:
            _template_cache[template_path] = f.read()

    return _template_cache[template_path]


def extract_template_section(template_content: str, start_marker: str, end_marker: str) -> str:
    """
    Extract a section from the template between markers.

    Args:
        template_content: Full template content
        start_marker: Starting marker (e.g., '<!--SECTION_START-->')
        end_marker: Ending marker (e.g., '<!--SECTION_END-->')

    Returns:
        Extracted template section, or empty string if markers not found
    """
    start_idx = template_content.find(start_marker)
    end_idx = template_content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        return ""

    # Extract content between markers (excluding the markers themselves)
    start_idx += len(start_marker)
    return template_content[start_idx:end_idx].strip()


def generate_stars_badge(stars: Optional[int]) -> str:
    """
    Generate HTML for stars badge (for Advent of Code projects).

    Args:
        stars: Number of stars achieved (optional)

    Returns:
        HTML string with stars badge or empty string
    """
    if stars is None or stars == 0:
        return ""

    # SVG star icon
    star_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16"><path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/></svg>'

    escaped_stars = escape_html(str(stars))
    return f'<div class="project-stars-badge">{star_svg} {escaped_stars} stars</div>'


def generate_project_card(project: Dict, card_template: str, image_template: str) -> str:
    """
    Generate HTML for a single project card.

    Args:
        project: Dictionary with keys:
            - title (required): Project title
            - description (required): Project description
            - url (required): GitHub or project URL
            - button_text (required): Text for the action button
            - image (optional): Image URL
            - tags (optional): List of technology tags
            - stars (optional): Number of stars for Advent of Code projects
        card_template: HTML template string with {{placeholders}}
        image_template: HTML template for image section

    Returns:
        Complete HTML string for the project card

    Raises:
        ValueError: If required fields are missing

    Example:
        >>> project = {
        ...     'title': 'My Project',
        ...     'description': 'A cool project',
        ...     'url': 'https://github.com/user/project',
        ...     'button_text': 'View on GitHub',
        ...     'language': 'Python',
        ...     'stars': 50
        ... }
        >>> html = generate_project_card(project, card_tpl, img_tpl)
    """
    # Validate project has required fields
    validate_project(project)

    # Generate image section if image URL is provided
    image_section = ""
    if project.get('image'):
        image_section = image_template.replace(
            '{{image}}', escape_html(project['image']))
        image_section = image_section.replace(
            '{{title}}', escape_html(project['title']))

    # Generate language tag (only primary language)
    language_tag = (project.get('language'))

    # Generate stars badge for Advent of Code projects
    stars_badge = generate_stars_badge(project.get('stars'))

    # Fill in the card template with escaped content
    card_html = card_template
    card_html = card_html.replace('{{image_section}}', image_section)
    card_html = card_html.replace('{{title}}', escape_html(project['title']))
    card_html = card_html.replace(
        '{{description}}', escape_html(project['description']))
    card_html = card_html.replace('{{language_tag}}', language_tag)
    card_html = card_html.replace('{{stars_badge}}', stars_badge)
    card_html = card_html.replace('{{url}}', escape_html(project['url']))
    card_html = card_html.replace(
        '{{button_text}}', escape_html(project['button_text']))

    return card_html


def generate_project_group(group_data: Dict, card_template: str, image_template: str, group_template: str) -> str:
    """
    Generate HTML for a project group with multiple projects.

    Args:
        group_data: Dictionary with keys:
            - group_title (required): Title for the group
            - group_description (required): Description for the group
            - projects (required): List of project dictionaries
        card_template: HTML template for individual project cards
        image_template: HTML template for image sections
        group_template: HTML template for the group wrapper

    Returns:
        Complete HTML string for the project group
    """
    projects_html_parts = []

    # Generate each project card
    for project in group_data.get('projects', []):
        try:
            project_card = generate_project_card(
                project, card_template, image_template)
            projects_html_parts.append(project_card)
        except ValueError as e:
            # Log error but continue with other projects
            print(f"Warning: Skipping invalid project - {e}")
            continue

    # Combine all project cards
    projects_html = '\n    '.join(projects_html_parts)

    # Use template if available, otherwise fall back to hardcoded HTML
    if group_template:
        group_html = group_template
        group_html = group_html.replace(
            '{{group_title}}', escape_html(group_data.get('group_title', '')))
        group_html = group_html.replace('{{group_description}}', escape_html(
            group_data.get('group_description', '')))
        group_html = group_html.replace('{{projects}}', projects_html)
    else:
        # Fallback to hardcoded template
        group_html = f'''<div class="project-group mb-5">
  <h3 class="project-group-title mb-3">{escape_html(group_data.get('group_title', ''))}</h3>
  <p class="project-group-description mb-4">{escape_html(group_data.get('group_description', ''))}</p>
  <div class="row g-4">
    {projects_html}
  </div>
</div>'''

    return group_html


def generate_projects_html(projects_data: Dict, template_dir: str) -> str:
    """
    Generate complete projects HTML from structured data.

    Args:
        projects_data: Dictionary containing project groups:
            {
                "groups": [
                    {
                        "group_title": "...",
                        "group_description": "...",
                        "projects": [...]
                    }
                ]
            }
        template_dir: Directory containing the projects template

    Returns:
        Complete HTML string for the projects section including CSS
    """
    # Load the template with caching
    template_path = os.path.join(template_dir, 'projects_template.html')
    template_content = load_projects_template(template_path)

    # Extract templates for different components using constants
    card_template = extract_template_section(
        template_content,
        CARD_START_MARKER,
        CARD_END_MARKER
    )

    image_template = extract_template_section(
        template_content,
        IMAGE_START_MARKER,
        IMAGE_END_MARKER
    )

    group_template = extract_template_section(
        template_content,
        GROUP_START_MARKER,
        GROUP_END_MARKER
    )

    # Extract CSS styles
    css_start = template_content.find('<style>')
    css_end = template_content.find('</style>') + len('</style>')
    css_styles = template_content[css_start:css_end] if css_start != -1 else ""

    html_parts = []

    # Add CSS styles at the beginning
    if css_styles:
        html_parts.append(css_styles)

    # Generate HTML for each project group
    for group in projects_data.get('groups', []):
        try:
            group_html = generate_project_group(
                group, card_template, image_template, group_template)
            html_parts.append(group_html)
        except Exception as e:
            # Log error but continue with other groups
            print(f"Warning: Error generating group - {e}")
            continue

    return '\n\n'.join(html_parts)
