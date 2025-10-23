"""
Projects Generator Module
Handles the generation of project sections with grouping and enhanced visuals
"""

import os
import json


def load_projects_template(template_path):
    """Load the projects HTML template"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_template_section(template_content, start_marker, end_marker):
    """Extract a section from the template between markers"""
    start_idx = template_content.find(start_marker)
    end_idx = template_content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        return ""
    
    # Extract content between markers (excluding the markers themselves)
    start_idx += len(start_marker)
    return template_content[start_idx:end_idx].strip()


def generate_project_tags(tags):
    """Generate HTML for project tags"""
    if not tags:
        return ""
    
    tag_html_parts = []
    for tag in tags:
        tag_html = f'<span class="badge bg-secondary project-tag">{tag}</span>'
        tag_html_parts.append(tag_html)
    
    return '\n        '.join(tag_html_parts)


def generate_project_card(project, card_template, image_template):
    """Generate HTML for a single project card"""
    # Generate image section if image URL is provided
    image_section = ""
    if project.get('image'):
        image_section = image_template.replace('{{image}}', project['image'])
        image_section = image_section.replace('{{title}}', project['title'])
    
    # Generate tags
    tags_html = generate_project_tags(project.get('tags', []))
    
    # Fill in the card template
    card_html = card_template
    card_html = card_html.replace('{{image_section}}', image_section)
    card_html = card_html.replace('{{title}}', project['title'])
    card_html = card_html.replace('{{description}}', project['description'])
    card_html = card_html.replace('{{tags}}', tags_html)
    card_html = card_html.replace('{{url}}', project['url'])
    card_html = card_html.replace('{{button_text}}', project['button_text'])
    
    return card_html


def generate_project_group(group_data, card_template, image_template):
    """Generate HTML for a project group"""
    projects_html_parts = []
    
    for project in group_data['projects']:
        project_card = generate_project_card(project, card_template, image_template)
        projects_html_parts.append(project_card)
    
    # Combine all project cards
    projects_html = '\n    '.join(projects_html_parts)
    
    # Create the group HTML
    group_html = f'''<div class="project-group mb-5">
  <h3 class="project-group-title mb-3">{group_data['group_title']}</h3>
  <p class="project-group-description mb-4">{group_data['group_description']}</p>
  <div class="row g-4">
    {projects_html}
  </div>
</div>'''
    
    return group_html


def generate_projects_html(projects_data, template_dir):
    """
    Generate complete projects HTML from structured data
    
    Args:
        projects_data: Dictionary containing project groups and individual projects
        template_dir: Directory containing the projects template
    
    Returns:
        Complete HTML string for the projects section
    """
    # Load the template
    template_path = os.path.join(template_dir, 'projects_template.html')
    template_content = load_projects_template(template_path)
    
    # Extract templates for different components
    card_template = extract_template_section(
        template_content, 
        '<!--PROJECT_CARD_START-->', 
        '<!--PROJECT_CARD_END-->'
    )
    
    image_template = extract_template_section(
        template_content,
        '<!--IMAGE_SECTION_START-->',
        '<!--IMAGE_SECTION_END-->'
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
        group_html = generate_project_group(group, card_template, image_template)
        html_parts.append(group_html)
    
    return '\n\n'.join(html_parts)
