from django.contrib import admin
from .models import UserActivationKey, Course, CoursePart, CourseTaken, Quiz, QuizPart, QuizTaken, TotalScore

# Register your models here.
class UserActivationKeyAdmim(admin.ModelAdmin):
    list_display = ['user','activation_key','key_expires']
    search_fields = ['user']
    list_per_page = 25
admin.site.register(UserActivationKey, UserActivationKeyAdmim)

class CourseAdmin(admin.ModelAdmin):
     list_display = ['course_name','course_description']
     search_fields = ['course_name']
     list_per_page = 25
admin.site.register(Course, CourseAdmin)

class CoursePartAdmin(admin.ModelAdmin):
    list_display = ['number', 'course','course_part_name','content','quiz_example','answer_key_example','course_point']
    search_fields = ['course']
    list_filter = ['course',]
    list_per_page = 25
admin.site.register(CoursePart, CoursePartAdmin)

class CourseTakenAdmin(admin.ModelAdmin):
    list_display = ['user','course','is_done']
    search_fields = ['user']
    list_per_page = 25
admin.site.register(CourseTaken, CourseTakenAdmin)

class QuizAdmin(admin.ModelAdmin):
    list_display = ['course']
    search_fields = ['course']
    list_per_page = 25
admin.site.register(Quiz, QuizAdmin)

class QuizPartAdmin(admin.ModelAdmin):
    list_display = ['quiz','course_part_name','quiz_part_name','quiz_challenge','answer_key_challenge']
    search_fields = ['quiz_part_name']
    list_per_page = 25
    
admin.site.register(QuizPart, QuizPartAdmin)

class QuizTakenAdmin(admin.ModelAdmin):
    list_display = ['user','quiz','quiz_point']
    search_fields = ['user']
    list_per_page = 25
admin.site.register(QuizTaken, QuizTakenAdmin)

class TotalScoreAdmin(admin.ModelAdmin):
    list_display = ['user','total_score']
    search_fields = ['user']
    list_per_page = 25
admin.site.register(TotalScore, TotalScoreAdmin)
