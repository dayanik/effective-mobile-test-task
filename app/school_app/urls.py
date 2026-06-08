from django.urls import path

from school_app import views

urlpatterns = [
    path("subjects/", views.SubjectView.as_view()),
    path("graduates/", views.GraduateView.as_view()),
]
