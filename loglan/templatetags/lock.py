from django import template
from django.core.exceptions import ObjectDoesNotExist
from ..models import CourseTaken
register = template.Library()

@register.simple_tag
def part_lock(user, course_part):
    course_taken = CourseTaken.objects.get(
        user=user,
        course=course_part.course
    )
    # cek kalo part pertama pasti ngga dilock
    if course_part == course_part.course.course_parts.all()[0]:
        return 'unlocked'
    # cek pernah ngerjain coursenya belum
    elif not course_taken:
        # kalau belum ngerjain coursenya brarti dilock
        return 'locked'
    else:
        # kalau udah, cek course_part nya ada di course_taken.course_part.all() ngga.
        # kalau iya, unlocked
        if course_part in course_taken.course_part.all():
            return 'unlocked'
        else:
            if course_part == course_taken.last_taken_part().next_part():
                return 'unlocked'
            else:
                return 'locked'

@register.simple_tag
def quiz_lock(user, course):
    try:
        course_taken = CourseTaken.objects.get(
            user=user,
            course=course
        )
        if course_taken.is_done:
            return 'unlocked'
        else:
            return 'locked'
    except ObjectDoesNotExist:
        return 'locked'
