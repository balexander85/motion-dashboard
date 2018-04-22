"""
    Programmatic way to upload photos with Photologue models
"""

from datetime import datetime
import pytz
import os
from typing import List

from django.template.defaultfilters import slugify
from PIL import Image
import PIL.ExifTags
from photologue.models import Gallery, Photo


top_dir = "public/photogallery/media/uploaded_photos"


def gather_photos(photos_path: str) -> List:
    """
        With given path return a list of dictionaries
        that contains the paths and a list of photos
    """
    return [
        os.path.join(photos_path, photo)
        for photo in os.listdir(photos_path) if photo.endswith(".jpg")
    ]


def get_photo_date(photo_path) -> datetime:
    """Get EXIF data from image."""
    with Image.open(photo_path) as img:
        exif = {
            PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        date_time = exif.get("DateTime")
        # time_zone = exif.get("TimeZoneOffset")
        date_taken = pytz.timezone("US/Central").localize(
            datetime.strptime(date_time, "%Y:%m:%d %H:%M:%S")
        )
        return date_taken


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
    new_photo_path = (
        f"public/photogallery/media/photologue/photos/{photo_file_name}"
    )
    photologue_path = f"photologue/photos/{photo_file_name}"
    # Move photo to photologue directory
    os.rename(photo_path, new_photo_path)
    photo_model = Photo(
        image=photologue_path, date_taken=photo_date, title=photo_title,
        slug=slugify(photo_title), caption='', date_added=upload_date,
        is_public=True
    )
    photo_model.save()
    if gallery_name:
        add_photo_to_gallery(photo_obj=photo_model, gallery_name=gallery_name)


if __name__ == "__main__":
    photos = gather_photos(top_dir)
    for photo in photos:
        upload_photo(photo_path=photo, gallery_name='upload-test')
