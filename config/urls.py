from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("auth/", include("apps.authentication.urls")),
        path("admin-panel/", include("apps.admin_panel.urls")),
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

from config.settings.debug_toolbar.setup import DebugToolbarSetup  # noqa

urlpatterns = DebugToolbarSetup.do_urls(urlpatterns)
