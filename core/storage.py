import os
from urllib.parse import urljoin
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CKEditorStorage(FileSystemStorage):
    def get_folder_name(self):
        return settings.CKEDITOR_5_UPLOAD_PATH

    def get_valid_name(self, name):
        return os.path.join(self.get_folder_name(), name)
