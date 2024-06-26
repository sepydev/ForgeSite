from django.urls import path

from . import views

app_name = "admin_panel"
urlpatterns = [
    path("", views.AdminPanelView.as_view(), name="index"),
    path(
        "website-pages/<int:pk>/",
        views.website_pages_change,
        name="website_pages_change",
    ),
]
