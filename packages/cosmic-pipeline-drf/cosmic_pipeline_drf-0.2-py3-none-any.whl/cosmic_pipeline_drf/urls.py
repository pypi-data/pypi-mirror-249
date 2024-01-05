from django.conf import settings
from django.urls import path, include

from cosmic_pipeline_drf.routers import router

app_name = "cosmic_pipeline_drf"

url_suffix = getattr(settings,"COSMIC_PIPELINE_DRF_URL_SUFFIX","cosmic_pipeline_drf")
if url_suffix.strip() != "":
    url_suffix = f"{url_suffix}/"

urlpatterns = [
    path(f"{url_suffix}", include(router.urls)),
]
