from django.contrib import admin
from .models import UserProfile, UserActivationKey, Course, CoursePart, CourseTaken, Quiz, QuizPart, QuizPartAnswer, QuizTaken

# Register your models here.
class UserProfileAdmim(admin.ModelAdmin):
    list_display = ['user',]
    list_per_page = 25
admin.site.register(UserProfile, UserProfileAdmim)

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
    list_display = ['number', 'course','course_part_name','course_content','course_example','course_example_answer_key','course_point']
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
    list_display = ['number','quiz','course_part','quiz_part_name','quiz_content','quiz_answer_key','quiz_point']
    search_fields = ['quiz_part_name']
    list_filter = ['quiz',]
    list_per_page = 25
admin.site.register(QuizPart, QuizPartAdmin)

class QuizPartAnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_part','text_answer','image_answer']
    list_filter = ['quiz_part',]
    list_per_page = 25
admin.site.register(QuizPartAnswer, QuizPartAnswerAdmin)

class QuizTakenAdmin(admin.ModelAdmin):
    list_display = ['user','quiz',]
    search_fields = ['user']
    list_per_page = 25
admin.site.register(QuizTaken, QuizTakenAdmin)
