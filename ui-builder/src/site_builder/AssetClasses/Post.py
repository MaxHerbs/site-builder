import datetime
import os
import subprocess


class Post:
    def __init__(
        self,
        date,
        slide_files,
        thumbnail_file,
        src_dir,
        comment_file=None,
    ):
        self.comment_file = comment_file
        self.slide_files = slide_files
        self.thumbnail_file = thumbnail_file
        self.date = date

        self.is_valid = self.validate(src_dir)
        # self.is_valid = True

        # self.comment = "TEST COMMENT"
        if self.comment_file:
            with open(src_dir + "/" + self.comment_file) as f:
                self.comment = f.read().strip()

    def __repr__(self):
        return f"Post for {self.date} with {len(self.slide_files)} slides. {'Has' if self.comment_file else 'No'} comments."

    def validate(self, src_dir):
        for file in self.slide_files:
            if not os.path.exists(f"{src_dir}/" + file):
                return False
        if self.comment_file and not os.path.exists(f"{src_dir}/" + self.comment_file):
            return False
        if not os.path.exists(f"{src_dir}/" + self.thumbnail_file):
            return False
        return True

    def move_content(self, src, dst):
        subprocess.run(
            [
                "cp",
                src + self.thumbnail_file,
                dst + "/thumbnails/" + self.thumbnail_file,
            ]
        )
        for file in self.slide_files:
            subprocess.run(["cp", src + file, dst + "/images/" + file])
