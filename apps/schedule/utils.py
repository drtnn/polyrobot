import re
from datetime import datetime
from typing import Union, Dict, List

from rest_framework.exceptions import ValidationError

from apps.mospolytech.models import Group, Student
from apps.schedule.models import ScheduledLesson, Lesson, LessonPlace, LessonTeacher, LessonType, LessonRoom

SLEEP_TIME = 60 * 60


def save_lesson_place(lesson: dict):
    rooms = [LessonRoom.objects.get_or_create(number=room) for room in lesson['rooms']]
    if lesson['rooms']:
        lesson_place = LessonPlace.objects.get_or_none(title=lesson['place'], link=lesson['link'],
                                                       rooms__in=lesson['rooms'])
    else:
        lesson_place = LessonPlace.objects.get_or_none(title=lesson['place'], link=lesson['link'])
    if not lesson_place:
        lesson_place = LessonPlace.objects.create(title=lesson['place'], link=lesson['link'])

    for room in rooms:
        lesson_place.rooms.add(room)

    return lesson_place


def save_schedule(group: Group, schedule: Union[Dict, List]):
    if schedule and isinstance(schedule, dict):
        scheduled_lessons = []
        for date, lessons in schedule.items():
            lessons_list = lessons['lessons']

            for lesson in lessons_list:
                name = lesson['name'].split(' (')
                title, type = name[0], name[1][:-1]

                lesson_teachers = [LessonTeacher.objects.get_or_create(full_name=teacher)[0].id for teacher in
                                   lesson['teachers']]
                lesson_place = save_lesson_place(lesson)
                lesson_type, _ = LessonType.objects.get_or_create(title=type)

                lesson_object = Lesson.objects.get_or_none(title=title, group=group, type=lesson_type,
                                                           place=lesson_place, teachers__in=lesson_teachers)

                if not lesson_object:
                    lesson_object = Lesson.objects.create(title=title, group=group, type=lesson_type,
                                                          place=lesson_place)
                    lesson_object.teachers.add(*lesson_teachers)

                if re.fullmatch(r'\d{4}-\d\d-\d\d', date):
                    # Not repeated lessons
                    raw_datetime = f'{date} {lesson["timeInterval"].split(" - ")[0].replace(" ", "")}'
                    datetime_object = datetime.strptime(raw_datetime, '%Y-%m-%d %H:%M')
                    if datetime_object >= datetime.now():
                        scheduled_lessons.append(ScheduledLesson(lesson=lesson_object, datetime=datetime_object))
                else:
                    # Repeated lessons
                    # TODO: Реализовать функционал сохранения семестрового расписания
                    pass

        ScheduledLesson.objects.bulk_create(scheduled_lessons)
        Lesson.objects.filter(scheduledlesson__isnull=True).delete()
        LessonPlace.objects.filter(lesson__isnull=True).delete()
        LessonType.objects.filter(lesson__isnull=True).delete()
        LessonTeacher.objects.filter(lessons__isnull=True).delete()
        LessonRoom.objects.filter(lessons__isnull=True).delete()


def update_schedule():
    ScheduledLesson.objects.filter(datetime__lt=datetime.now()).delete()

    group_users = {}
    for student in Student.objects.all():
        if student.group.number in group_users:
            group_users[student.group.number].append(student.user)
        else:
            group_users[student.group.number] = [student.user]

    groups = {group.number: group for group in Group.objects.filter(student__group__number__in=group_users.keys())}

    for group_number, group in groups.items():
        for actual_user in group_users.pop(group_number):
            try:
                schedule = actual_user.schedule(is_session=False)
                session_schedule = actual_user.schedule(is_session=True)
            except ValidationError:
                continue
            else:
                save_schedule(group, schedule)
                save_schedule(group, session_schedule)
                break
