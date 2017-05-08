from django import template
from django.core.exceptions import ObjectDoesNotExist

from ..models import CourseTaken, Course
register = template.Library()

@register.assignment_tag
def last_taken_part(user, course):
    course_taken, created = CourseTaken.objects.get_or_create(
        user=user,
        course=course
    )
    if created:
        course_taken.course_part.add(course.course_parts.all()[0])

    try:
        if course_taken.last_taken_part():
            return course_taken.last_taken_part().next_part()
        else:
            return course_taken.course.course_parts.all()[0]

    except ObjectDoesNotExist:
        return course_taken.course.course_parts.all()[0]

@register.simple_tag
def user_course_point_per_level(user, course_id):
    point = 0
    course = Course.objects.get(id=course_id)
    course_taken = CourseTaken.objects.get(user=user, course=course)
    for course_part in course_taken.course_part.all():
        point += course_part.course_point
    return point