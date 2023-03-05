from .exceptions import UniversityNotFound, CompanyNotProvided, InsufficientAmount, ExcessiveAmount
from .models import University, Student, Sponsor, Donation

from rest_framework import serializers, status

from django.shortcuts import get_object_or_404
from django.db.models import Sum


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name']

class StudentSerializer(serializers.ModelSerializer):
    university = serializers.StringRelatedField(read_only=True)
    university_name = serializers.CharField(write_only=True)
    amount_received = serializers.SerializerMethodField(method_name="get_amount_received", read_only=True)
    open = serializers.SerializerMethodField(method_name="get_open", read_only=True)

    def get_open(self, student):
        """
         Agar Kontrakt Summasi Qoplangan Bo'lsa: False
         Yo'ki: True
        """
        if self.get_amount_received(student) >= student.tuition:
            return False
        return True

    def get_amount_received(self, student):
        """
         Yeg'ilgan Summani Hisoblash
        """
        return student.sponsorship.all().aggregate(Sum('amount', default=0))['amount__sum']

    def create(self, validated_data):
        """
         Create Metodini Override Qilish
        """
        university_name = validated_data.get('university_name').upper()
        university = University.objects.filter(name=university_name)
        if university.exists():
            validated_data.pop('university_name')
            validated_data['university_id'] = university[0].id
        else:
            raise UniversityNotFound

        student = Student.objects.create(**validated_data)
        student.save()
        return student

    def update(self, instance, validated_data):
        """
         Update Metodini Override Qilish
        """
        university_name = validated_data.get('university_name').upper()
        university = University.objects.filter(name=university_name)

        if university.exists():
            validated_data.pop('university_name')
            validated_data['university_id'] = university[0].id
        else:
            raise UniversityNotFound
        
        return super().update(instance=instance, validated_data=validated_data)

    class Meta:
        model = Student
        fields = ['id', 'fish', 'phone_number', 'university', 'university_name', 'degree', 'year', 'tuition', 'amount_received', 'open']



class SponsorSerializer(serializers.ModelSerializer):
    amount_spent = serializers.SerializerMethodField(method_name="get_amount_spent")

    def get_amount_spent(self, sponsor):
         return sponsor.sponsorship.all().aggregate(Sum('amount', default=0))['amount__sum']

    def create(self, validated_data):
        """
         Create Metodini Override Qilish
        """
        type = validated_data['type']
        company = validated_data['company']

        if type == 'Yuridik shaxs' and len(company.strip()) == 0:
            raise CompanyNotProvided

        sponsor = Sponsor.objects.create(**validated_data)
        sponsor.save()
        return sponsor

    def update(self, instance, validated_data):
        """
         Update Metodini Override Qilish
        """
        type = validated_data.get('type')
        company = validated_data.get('company')

        if type == 'Yuridik shaxs' and len(company.strip()) == 0:
            raise CompanyNotProvided

        return super().update(instance=instance, validated_data=validated_data)

    class Meta:
        model = Sponsor
        fields = ['id', 'type', 'fish', 'phone_number', 'amount', 'company', 'amount_spent', 'status']


class DonationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    sponsor = SponsorSerializer(read_only=True)
    sponsor_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        """
         Create Metodini Override Qilish
        """
        amount = validated_data.get('amount')

        student = get_object_or_404(Student, pk=validated_data.get('student_id'))
        sponsor = get_object_or_404(Sponsor, pk=validated_data.get('sponsor_id'))

        amount_sponsor_gave = sponsor.sponsorship.all().aggregate(Sum('amount', default=0))['amount__sum']
        amount_student_received = student.sponsorship.all().aggregate(Sum('amount', default=0))['amount__sum']
        sponsor_balance = sponsor.amount - amount_sponsor_gave

        if sponsor_balance >= amount:
            if amount_student_received + amount <= student.tuition:
                return Donation.objects.create(**validated_data)
            else:
                raise ExcessiveAmount
        else:
            raise InsufficientAmount

    def update(self, donation, validated_data):
        """
         Update Metodini Override Qilish
        """
        student = donation.student
        sponsor = get_object_or_404(Sponsor, id=validated_data.get('sponsor_id'))

        amount = validated_data.get('amount')
        amount_sponson_gave = sponsor.sponsorship.exclude(id=donation.id).aggregate(Sum('amount', default=0))['amount__sum']
        amount_student_received = student.sponsorship.exclude(id=donation.id).aggregate(Sum('amount', default=0))['amount__sum']

        sponsor_balance = sponsor.amount - amount_sponson_gave

        if amount <= sponsor_balance:
            if student.tuition <= amount + amount_student_received:
                donation.amount = amount
                donation.sponsor = sponsor
                donation.save()
                return donation
            else:
                ExcessiveAmount
        else:
            raise InsufficientAmount

    class Meta:
        model = Donation
        fields = ['id', 'sponsor', 'sponsor_id', 'student', 'student_id', 'amount', 'date_created']
