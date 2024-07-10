import os
import shutil


class DirectoryManager:
    def __init__(self, image_dir, output_dir=None):
        self.image_dir = image_dir
        self.output_dir = output_dir

    def ensure_directories(self):
        """Ensure that all required directories exist."""
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        if self.output_dir and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def cleanup(self):
        """Remove the directories and their contents."""
        if os.path.exists(self.image_dir):
            shutil.rmtree(self.image_dir, ignore_errors=True)
        if self.output_dir and os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir, ignore_errors=True)
