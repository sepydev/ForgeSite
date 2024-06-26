from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView

from apps.core.models import WebsitePage


class AdminPanelView(LoginRequiredMixin, ListView):
    model = WebsitePage
    template_name = "admin_panel/admin_panel.html"
    context_object_name = "website_pages"

    def get_queryset(self):
        return WebsitePage.objects.all()


def website_pages_change(request, pk):
    website_page = WebsitePage.objects.get(pk=pk)
    html = render_to_string(
        "admin_panel/website_pages_change.html", {"website_page": website_page}
    )
    return HttpResponse(html)
