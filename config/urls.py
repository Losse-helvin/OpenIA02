from django.contrib import admin
from django.urls import path
from leads import views

urlpatterns = [path("admin/", admin.site.urls), path("", views.home, name="home"), path("api/chat", views.chat, name="chat"), path("api/consent", views.consent, name="consent"), path("api/status", views.status, name="status"), path("api/reset", views.reset, name="reset")]
