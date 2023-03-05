from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class University(models.Model):
    UNIVERSITIES = (
        ("INHA", "Inha University in Tashkent"),
        ("WIUT", "Westminster University in Tashkent"),
        ("MDIST", "Management Development Institute of Singapore in Tashkent"),
        ("AMITY", "Amity Univesity in Tashkent"),
        ("AKFA", "Akfa University in Tashkent"),
    )

    name = models.CharField(max_length=255, choices=UNIVERSITIES, unique=True, verbose_name="OTM")

    class Meta:
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name


class Student(models.Model):
    DEGREES = (
        ("Bakalavr", "Bakalavr"),
        ("Magistr", "Magistr"),
        ("Phd", "PhD"),
    )

    YEAR = (
        ("Birinchi", "Birinchi"),
        ("Ikkinchi", "Ikkinchi"),
        ("Uchinchi", "Uchinchi"),
        ("To'rtinchi", "To'rtinchi"),
    )

    fish = models.CharField(max_length=255, unique=True, verbose_name="Familiya Ism Sharif")
    phone_number = PhoneNumberField(max_length=15, region="UZ", verbose_name="Telefon Raqami")
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="student")
    degree = models.CharField(max_length=255, choices=DEGREES, verbose_name="Talabalik Turi")
    year = models.CharField(max_length=255, choices=YEAR, verbose_name="Kurs")
    tuition = models.PositiveBigIntegerField(verbose_name="Kontrakt Miqdori")
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("fish", "university", "degree")

    def __str__(self):
        return self.fish


class Sponsor(models.Model):
    STATUS_CHOICES = (
        ("Yangi", "Yangi"),
        ("Moderiyatsada", "Moderiyatsada"),
        ("Tasdiqlangan", "Tasdiqlangan"),
        ("Bekor qilingan", "Bekor qilingan"),
    )

    SPONSOR = (
        ('Jismoniy shaxs', 'Jismoniy shaxs'),
        ('Yuridik shaxs', 'Yuridik shaxs'),
    )

    fish = models.CharField(max_length=255, unique=True, verbose_name="Familiya Ism Sharif")
    phone_number = PhoneNumberField(max_length=15, region="UZ", verbose_name="Telefon Raqami")
    amount = models.PositiveBigIntegerField(verbose_name="To'lov Summasi")
    type = models.CharField(max_length=255, choices=SPONSOR, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, verbose_name="Tashkilot Nomi")
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="Yangi", verbose_name="Holati")
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.company:
            return f"{self.fish} - {self.company}"
        return self.fish



class Donation(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name="sponsorship")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sponsorship")
    amount = models.PositiveBigIntegerField(verbose_name="To'lov Summasi")
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor} - {self.student}"



