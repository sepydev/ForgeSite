from django.shortcuts import render


def index(request):
    return render(request, "admin_panel/index.html")
