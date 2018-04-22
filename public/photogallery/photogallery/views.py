from django.conf import settings
from django.shortcuts import render_to_response


camera_host_list = [
    f"http://{settings.MOTION_HUB_HOST_NAME}.local:{i}" for i in range(8081, 8086)
]


def index(request):
    return render_to_response("index.html")


def live(request):
    return render_to_response(
        template_name="live.html", context={"host_list": camera_host_list}
    )
