from .serializers import UniversitySerializer, StudentSerializer, SponsorSerializer, DonationSerializer
from .filters import DonationFilter, SponsorFilter, StudentFilter
from .models import University, Student, Sponsor, Donation

from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count


class UniversityView(generics.ListCreateAPIView):
    queryset = University.objects.all().order_by('name')
    serializer_class = UniversitySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name']

class UniversityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UniversitySerializer
    queryset = University.objects.all()
    lookup_field = 'name'


class StudentView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['university', 'degree', 'year']
    filterset_class = StudentFilter

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'

class StudentDonationView(generics.ListAPIView):
    serializer_class = DonationSerializer

    def get_queryset(self):
        student = get_object_or_404(Student, pk=self.kwargs.get('id'))
        return student.sponsorship.all()


class SponsorView(generics.ListCreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['type', 'status']
    filterset_class = SponsorFilter

class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    lookup_field = 'id'

class SponsorDonationView(generics.ListAPIView):
    serializer_class = DonationSerializer

    def get_queryset(self):
        sponsor = get_object_or_404(Sponsor, pk=self.kwargs.get('id'))
        return sponsor.sponsorship.all()


class DonationView(generics.ListCreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['sponsor', 'student']
    filterset_class = DonationFilter

class DonationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    lookup_field = 'id'


class DashBoardView(APIView):
    def get(self, request):
        amount_paid = Donation.objects.all().aggregate(Sum('amount', default=0))['amount__sum']
        amount_asked = Student.objects.all().aggregate(Sum('tuition', default=0))['tuition__sum']
        amount_to_pay = amount_asked - amount_paid

        sponsors_stats = Sponsor.objects.extra({'date_created': "date(date_created)"}).values('date_created').annotate(number=Count('id')).values_list('number', 'date_created')
        students_stats = Student.objects.extra({'date_created': "date(date_created)"}).values('date_created').annotate(number=Count('id')).values_list('number', 'date_created')

        data = {
            "To'langan Summa": amount_paid,
            "So'ralgan Summa": amount_asked,
            "To'lanishi Kerak Summa": amount_to_pay,
            "Sponsor Stats": sponsors_stats,
            "Student Stats": students_stats,
        }
        return Response(data=data)