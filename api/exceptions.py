from rest_framework.exceptions import APIException

class UniversityNotFound(APIException):
    status_code = 404
    default_detail = 'Universitet Mavjud Emas'
    default_code = 'universitet_mavjud_emas'

class CompanyNotProvided(APIException):
    status_code = 400
    default_detail = 'Companiya Nomini Kiriting'
    default_code = 'companiya_kiritilmadi'

class InsufficientAmount(APIException):
    status_code = 400
    default_detail = 'Mablag\' Yetarli Emas'
    default_code = 'mablag\'_yetarli_emas'

class ExcessiveAmount(APIException):
    status_code = 400
    default_detail =  'Mablag\' Ortiqcha'
    default_code = 'mablag\'_ortiqcha'
