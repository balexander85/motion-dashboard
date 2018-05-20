"""
    Programmatic way to upload photos with Photologue models
"""

from datetime import datetime
import pytz
import os
from typing import Generator
import logging
import sys
# import shutil

from django.conf import settings
from django.template.defaultfilters import slugify
from PIL import Image
import PIL.ExifTags
from photologue.models import Gallery, Photo

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)7s: %(message)s",
    stream=sys.stdout,
)
LOG = logging.getLogger("")


def gather_photos(photos_path: str) -> Generator:
    """
        With given path return a list of dictionaries
        that contains the paths and a list of photos
    """
    if os.path.isdir(photos_path):
        return (
            os.path.join(photos_path, photo)
            for photo in os.listdir(photos_path) if photo.endswith(".jpg")
        )
    else:
        yield


def get_photo_date(photo_path) -> datetime:
    """Get EXIF data from image."""
    with Image.open(photo_path) as img:
        exif = {
            PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        date_time = exif.get("DateTime")
        # time_zone = exif.get("TimeZoneOffset")
        return pytz.timezone("US/Central").localize(
            datetime.strptime(date_time, "%Y:%m:%d %H:%M:%S")
        )


def add_photo_to_gallery(photo_obj: Photo, gallery_name: str):
    """Add photo to gallery with the name given."""
    gallery = Gallery.objects.get(slug=gallery_name)
    photo_obj.galleries.add(gallery)


def upload_photo(photo_path: str, gallery_name: str=None):
    """
        Using Photo class from Photologue models upload photo to db
    """
    photo_date = get_photo_date(photo_path)
    upload_date = datetime.now(pytz.timezone("US/Central"))
    photo_file_name = photo_path.split("/")[-1]
    photo_title = photo_file_name.replace(".jpg", "")
    # new_photo_path = (
    #     f"public/photogallery/media/photologue/photos/{photo_file_name}"
    # )
    # photologue_path = f"photologue/photos/{photo_file_name}"
    # Move photo to photologue directory
    # shutil.copy(photo_path, new_photo_path)
    # os.rename(photo_path, new_photo_path)
    photo_model = Photo(
        image=photo_path, date_taken=photo_date, title=photo_title,
        slug=slugify(photo_title), caption='', date_added=upload_date,
        is_public=True
    )
    photo_model.save()
    if gallery_name:
        add_photo_to_gallery(photo_obj=photo_model, gallery_name=gallery_name)


if __name__ == "__main__":
    photos = gather_photos(settings.MOTION_PHOTO_DIRECTORY)
    LOG.info("Created photos generator, beginning for loop")
    for photo in photos:
        LOG.info(f"{photo} is being uploaded")
        upload_photo(photo_path=photo, gallery_name='upload-test')

