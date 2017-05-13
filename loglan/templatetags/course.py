from django import template
from django.core.exceptions import ObjectDoesNotExist

from ..models import CourseTaken, Course, CoursePart
register = template.Library()

@register.assignment_tag
def last_taken_part(user, course):
    try:
        course_taken = CourseTaken.objects.get(
            user=user,
            course=course
        )
        total = course_taken.course_part.all().count()
        # cek kalau part terakhir ngga usah di next
        if course_taken.last_taken_part().number == total:
            return course_taken.last_taken_part()
        elif course_taken.last_taken_part():
            return course_taken.last_taken_part().next_part()
        else:
            return course_taken.course.course_parts.all()[0]

    except:
        return course.course_parts.all()[0]

@register.simple_tag
def user_course_point_per_level(user, course_id):
    point = 0
    course = Course.objects.get(id=course_id)
    course_taken = CourseTaken.objects.get(user=user, course=course)
    for course_part in course_taken.course_part.all():
        point += course_part.course_point
    return point

@register.simple_tag
def user_course_progress_per_level(user, course_id):
    try:
        course = Course.objects.get(id=course_id)
        course_part = CoursePart.objects.filter(course=course).count()
        course_taken = CourseTaken.objects.get(user=user, course=course)
        total_taken = 0
        for course_part_user in course_taken.course_part.all():
            total_taken += 1

        progress = float(total_taken)/float(course_part)*100

        return progress

    except:
        progress = ''
