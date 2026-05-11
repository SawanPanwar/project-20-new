# utility/FileUtility.py

import os
import uuid

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class FileUtility:

    @staticmethod
    def upload_photo(photo_file):

        if not photo_file:
            return ""

        # Extract extension
        ext = os.path.splitext(photo_file.name)[1].lower()
        # Generate unique filename
        filename = f"user_{uuid.uuid4().hex}{ext}"
        # Create upload directory if not exists
        upload_dir = os.path.join(
            settings.MEDIA_ROOT,
            settings.USER_PHOTO_DIR
        )

        os.makedirs(upload_dir, exist_ok=True)

        # Full file path
        file_path = os.path.join(upload_dir, filename)

        # Save file
        with open(file_path, "wb+") as destination:
            for chunk in photo_file.chunks():
                destination.write(chunk)

        # Save relative path in DB
        saved_path = os.path.join(
            settings.USER_PHOTO_DIR,
            filename
        ).replace("\\", "/")

        return saved_path
