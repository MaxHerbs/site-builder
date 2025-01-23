import os

from jinja2 import Template


def render_template(output_dir, posts):
    """
    Render the template with the context data
    """
    print("len(posts):", len(posts))
    working_dir = os.path.dirname(os.path.realpath(__file__)) + "/html_assets"
    with open(working_dir + "/index.html") as f:
        template = Template(f.read())

    rendered_template = template.render(posts=posts)

    with open(output_dir + "/index.html", "w+") as f:
        f.write(rendered_template)
