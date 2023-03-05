from .views import UniversityView, UniversityDetailView, StudentView, StudentDetailView, SponsorView, SponsorDetailView, DonationView, DonationDetailView, SponsorDonationView, StudentDonationView, DashBoardView
from django.urls import path

urlpatterns = [
    # university urls
    path('universities', UniversityView.as_view()),
    path('universities/<str:name>', UniversityDetailView.as_view()),

    # student urls
    path('students', StudentView.as_view()),
    path('students/<int:id>', StudentDetailView.as_view()),
    path('students/<int:id>/donations', StudentDonationView.as_view()),

    # sponsor urls
    path('sponsors', SponsorView.as_view()),
    path('sponsors/<int:id>', SponsorDetailView.as_view()),
    path('sponsors/<int:id>/donations', SponsorDonationView.as_view()),

    # donation urls
    path('donations', DonationView.as_view()),
    path('donations/<int:id>', DonationDetailView.as_view()),

    # dashboard url
    path('', DashBoardView.as_view()),
]