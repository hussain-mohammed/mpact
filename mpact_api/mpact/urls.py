from django.urls import path

from . import views

urlpatterns = [
    path("login", views.Login.as_view()),
    path("logout", views.Logout.as_view()),
    path("send", views.SendMessage.as_view()),
    path("dialogs", views.Dialog.as_view()),
]
