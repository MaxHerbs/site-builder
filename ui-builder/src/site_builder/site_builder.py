import os
import subprocess

import typer
import yaml

from ._ConfigManager import ConfigManager
from ._Templater import render_template
from ._Thumbnails import format_thumbnails
from .AssetClasses.PostFactory import create_posts


def site_builder(source_dir,output_dir):
    print(f"Building site from {source_dir}")

    if not os.path.exists(source_dir):
        typer.echo(f"Could not find '{source_dir}'. Has it been populated?")
        raise typer.Exit(1)

    items = os.listdir(source_dir)
    posts = create_posts(source_dir, items)

    print("Files with no thumbnails:\n\n\n")
    posts.sort(key=lambda x: x.date)
    for post in posts:
        if not post.is_valid:
            print(post)

    valid_posts = [post for post in posts if post.is_valid]
    print(f"Found {len(valid_posts)} valid posts.")
    if os.path.exists(output_dir):
        typer.echo(f"Output directory '{output_dir}' already exists. Cleaning...")
        subprocess.run(f"rm -rf {output_dir}/*", shell=True)
    os.mkdir(output_dir + "/images")
    os.mkdir(output_dir + "/thumbnails")
    subprocess.run(
        [
            "cp",
            "-r",
            f"{os.path.dirname(os.path.realpath(__file__))}/../../html_assets/styles",
            output_dir,
        ]
    )
    valid_posts.sort(key=lambda x: x.date, reverse=True)
    for post in valid_posts:
        post.move_content(source_dir + "/", output_dir)

    format_thumbnails(output_dir + "/thumbnails/")

    site = render_template(output_dir, valid_posts)


def validate_post():
    pass
