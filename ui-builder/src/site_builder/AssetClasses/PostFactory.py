import datetime
import os

from .Post import Post

unique_dates = {}


def create_posts(config, items):
    for item in items:
        process_item(item)

    posts = []
    for date in unique_dates:
        posts.append(create_post(config, date))
    return posts


def create_post(dump_dir, date):
    post_files = unique_dates.get(date, None)
    if not post_files:
        # Not sure if this case is possible, but check anyways
        raise Exception("Post exists but has no files.")

    comment_file = get_comment_file(post_files)
    if comment_file:
        post_files.remove(comment_file)
    if [file for file in post_files if file.endswith(".xz")]:
        post_files = [file for file in post_files if not file.endswith(".xz")]

    thumbnail = get_thumbnail(post_files)
    post_files = remove_unused_thumbnails(post_files)
    post = Post(date, post_files, thumbnail, dump_dir, comment_file)
    return post


def get_thumbnail(files):
    # Check every case

    # Single video
    if len(files) == 2:
        if os.path.splitext(files[0])[0] == os.path.splitext(files[1])[0]:
            return os.path.splitext(files[0])[0] + ".jpg"

    # Single image
    if len(files) == 1:
        return files[0]

    # Combination of images and videos
    else:
        stem = "_".join(files[0].split("_")[:-1])
        print("Stem: ", stem)
        print("Files: ", files)

        return stem + "_1.jpg"


def remove_unused_thumbnails(files):
    videos = [file for file in files if file.endswith(".mp4")]
    corresponding_thumbnails = [file.replace(".mp4", ".jpg") for file in videos]
    for file in corresponding_thumbnails:
        if file in files:
            files.remove(file)
    return files


def get_comment_file(files):
    for file in files:
        if file.endswith(".txt"):
            return file
    return None


def process_item(file_name):
    this_date = extract_date(file_name)
    if this_date == -1:
        return
    if unique_dates.get(this_date, None):
        unique_dates[this_date].append(file_name)
    else:
        unique_dates[this_date] = [file_name]


def extract_date(file_name):
    date = "_".join(file_name.split("_")[0:2])
    try:
        return datetime.datetime.strptime(date, "%Y-%m-%d_%H-%M-%S")
    except:
        return -1
