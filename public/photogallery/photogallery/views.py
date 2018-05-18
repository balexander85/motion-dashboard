import pytz
from datetime import datetime

from django.conf import settings
from django.shortcuts import render_to_response, render

from photologue.models import Gallery
from .search_form import SearchForm

camera_host_list = [
    f"http://{settings.MOTION_HUB_HOST_NAME}.local:{i}" for i in range(
        8081, 8084
    )
]


def index(request):
    return render_to_response("index.html")


def live(request):
    return render_to_response(
        template_name="live.html", context={"host_list": camera_host_list}
    )


def search(request):
    form_class = SearchForm

    filtered_photos = []
    search_range = None

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            gallery = Gallery.objects.get(title='upload test')
            post_response = request.POST
            from_date = post_response.get("from_date", "")
            from_time = request.POST.get("from_time")
            from_datetime = datetime.strptime(
                f"{from_date} {from_time}",
                "%Y-%m-%d %H:%M:%S"
            )

            end_date = post_response.get("end_date", "")
            end_time = request.POST.get("end_time")
            end_datetime = datetime.strptime(
                f"{end_date} {end_time}",
                "%Y-%m-%d %H:%M:%S"
            )
            utc_start_date = pytz.timezone("UTC").localize(
                from_datetime
            )
            utc_end_date = pytz.timezone("UTC").localize(
                end_datetime
            )
            filtered_photos = gallery.photos.filter(
                date_taken__gte=utc_start_date, date_taken__lte=utc_end_date
            )
            search_range = (
                f"Start Date: {utc_start_date} End Date: {utc_end_date} "
                f"Total Results: {len(filtered_photos)}"
            )

    return render(
        request,
        template_name="search.html",
        context={
            "form": form_class,
            "photos": filtered_photos,
            "searchrange": search_range,
        }
    )
