import os
import uuid

from django.conf import settings


class FileUtility:
    ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"]

    @staticmethod
    def upload_photo(photo_file):

        if not photo_file:
            return ""

        ext = os.path.splitext(photo_file.name)[1].lower()

        if ext not in FileUtility.ALLOWED_EXTENSIONS:
            raise ValueError("Invalid file type")

        filename = f"user_{uuid.uuid4().hex}{ext}"

        relative_path = os.path.join(settings.USER_PHOTO_DIR, filename).replace("\\", "/")

        absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

        with open(absolute_path, "wb+") as destination:
            for chunk in photo_file.chunks():
                destination.write(chunk)

        return relative_path
