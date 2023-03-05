from .models import Donation, Sponsor, Student
import django_filters as filters

class DonationFilter(filters.FilterSet):
    class Meta:
        model = Donation
        fields = {
            'amount': ['gt', 'lt'],
        }

class SponsorFilter(filters.FilterSet):
    class Meta:
        model = Sponsor
        fields = {
            'amount': ['gt', 'lt']
        }

class StudentFilter(filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'tuition': ['gt', 'lt']
        }