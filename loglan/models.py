from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class UserActivationKey(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

class Course(models.Model):
    course_name = models.CharField(max_length=30)
    course_description = models.TextField()
    course_slug = models.SlugField(max_length=50, null=True)

    def __str__(self):
        return self.course_name

class CoursePart(models.Model):
    number = models.IntegerField(null=True)
    course = models.ForeignKey(Course, related_name='course_parts')
    course_part_name = models.CharField(max_length=30)
    content = models.TextField()
    quiz_example = models.TextField()
    answer_key_example = models.TextField()
    course_point = models.IntegerField()

    class Meta:
        ordering = ('number', )

    def __str__(self):
        return self.course_part_name

    def next_part(self):
        course_parts = CoursePart.objects.filter(course=self.course)
        try:
            next_part = course_parts.filter(number__gt=self.number).order_by('number')[0]
            return next_part
        except IndexError:
            return None

    def previous_part(self):
        course_parts = CoursePart.objects.filter(course=self.course)
        try:
            next_part = course_parts.filter(number__lt=self.number).order_by('-number')[0]
            return next_part
        except IndexError:
            return None

class CourseTaken(models.Model):
    user = models.OneToOneField(User, related_name='course_taken')
    course = models.ForeignKey(Course, related_name='course_takens')
    course_part = models.ManyToManyField(CoursePart, related_name='course_takens_part')
    is_done = models.BooleanField(default=False)
    #Method point course (Akumulasi poin dari course part)

    def __str__(self):
        return self.user.username

class Quiz(models.Model):
    course = models.OneToOneField(Course, related_name='quiz')

    def __str__(self):
        return self.course.course_name

class QuizPart(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='quiz_parts')
    course_part_name = models.ForeignKey(CoursePart, related_name='quiz_parts_course')
    quiz_part_name = models.CharField(max_length=30)
    quiz_challenge = models.TextField()
    answer_key_challenge = models.TextField()

    def __str__(self):
        return self.quiz_part_name

class QuizTaken(models.Model):
    user = models.OneToOneField(User, related_name='quiz_taken')
    quiz = models.ForeignKey(Quiz, related_name='quiz_takens')
    quiz_part_random = models.ManyToManyField(QuizPart, related_name='quiz_takens_random')
    quiz_part_is_completed = models.ManyToManyField(QuizPart, related_name='quiz_takens_is_completed')
    quiz_part_is_true = models.ManyToManyField(QuizPart, related_name='quiz_takens_is_true')
    quiz_point = models.IntegerField()

    def __str__(self):
        return self.user.username

class TotalScore(models.Model):
    user = models.OneToOneField(User, related_name='total_score')
    total_score = models.IntegerField()

    def __str__(self):
        return self.user.username
