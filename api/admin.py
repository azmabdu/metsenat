from django.contrib import admin
from .models import University, Student, Sponsor, Donation

admin.site.register(University)
admin.site.register(Student)
admin.site.register(Sponsor)
admin.site.register(Donation)
