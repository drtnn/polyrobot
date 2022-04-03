import re
from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Union, Dict, List

from django.db import transaction
from django.db.models import QuerySet
from ics import Calendar, Event
from rest_framework.exceptions import ValidationError

from apps.mospolytech.models import Group, Student
from apps.schedule.constants import WEEKDAYS, RU_MONTHS_TO_EN
from apps.schedule.models import ScheduledLesson, Lesson, LessonPlace, LessonTeacher, LessonType, LessonRoom, \
    ScheduledLessonNote


def change_month_on_en(raw_datetime):
    month = raw_datetime.split(' ')[1]
    return raw_datetime.replace(month, RU_MONTHS_TO_EN[month])


def get_nearest_date(raw_date: str) -> date:
    raw_date = change_month_on_en(raw_date)
    now = datetime.now()
    curr_year = datetime.now().year
    date_list = {
        datetime.strptime(f'{raw_date} {curr_year - 1}', '%d %b %Y'),
        datetime.strptime(f'{raw_date} {curr_year}', '%d %b %Y'),
        datetime.strptime(f'{raw_date} {curr_year + 1}', '%d %b %Y'),
    }

    return min(date_list, key=lambda x: abs(x - now)).date()


def schedule_repeated_lessons(
        repeated_lessons: Dict[str, list], first_date: date, last_date: date
) -> list:
    schedule_lessons = []
    today = first_date

    while today <= last_date:
        for weekday, lessons in repeated_lessons.items():
            if today.weekday() == weekday:
                for index, lesson_dict in enumerate(lessons):
                    raw_time = lesson_dict["time"].split(" - ")[0].replace(" ", "")
                    raw_datetime = f'{today.strftime("%Y-%m-%d")} {raw_time} +0300'
                    date_object = datetime.strptime(raw_datetime[:-6], '%Y-%m-%d %H:%M').date()
                    if lesson_dict['from_date'] <= date_object <= lesson_dict['to_date']:
                        schedule_lessons.append(ScheduledLesson(lesson=lesson_dict['lesson'], datetime=raw_datetime))
        today += timedelta(days=1)

    return schedule_lessons


def save_lesson_place(lesson: dict) -> LessonPlace:
    room_ids = [LessonRoom.objects.get_or_create(number=room)[0].id for room in lesson['rooms']]
    if room_ids:
        lesson_place = LessonPlace.objects.filter(title=lesson['place'], link=lesson['link'],
                                                  rooms__in=room_ids).distinct().first()
    else:
        lesson_place = LessonPlace.objects.get_or_none(title=lesson['place'], link=lesson['link'],
                                                       rooms__isnull=True)

    if not lesson_place:
        lesson_place = LessonPlace.objects.create(title=lesson['place'], link=lesson['link'])
        lesson_place.rooms.add(*[room_id for room_id in room_ids])

    return lesson_place


def save_schedule(group: Group, schedule: Union[Dict, List]):
    if schedule and isinstance(schedule, dict):
        scheduled_lessons = []
        repeated_lessons = defaultdict(list)
        first_date = date.today()
        last_date = date.today()

        for raw_date, lessons in schedule.items():
            lessons_list = lessons['lessons']

            for lesson in lessons_list:
                name = lesson['name'].split(' (')
                title, type = name[0], name[1][:-1]

                lesson_teachers = [LessonTeacher.objects.get_or_create(full_name=teacher)[0].id for teacher in
                                   lesson['teachers']]
                lesson_place = save_lesson_place(lesson)
                lesson_type, _ = LessonType.objects.get_or_create(title=type)

                lesson_object = Lesson.objects.filter(title=title, group=group, type=lesson_type, place=lesson_place,
                                                      teachers__in=lesson_teachers).first()

                if not lesson_object:
                    lesson_object = Lesson.objects.create(title=title, group=group, type=lesson_type,
                                                          place=lesson_place)
                    lesson_object.teachers.add(*lesson_teachers)

                if re.fullmatch(r'\d{4}-\d\d-\d\d', raw_date):
                    # Not repeated lessons
                    raw_datetime = f'{raw_date} {lesson["timeInterval"].split(" - ")[0].replace(" ", "")} +0300'
                    scheduled_lessons.append(ScheduledLesson(lesson=lesson_object, datetime=raw_datetime))
                elif re.fullmatch(r'\d\d \w{3}', lesson['dateInterval']):
                    # Not repeated lessons
                    scheduled_lessons.append(
                        ScheduledLesson(lesson=lesson_object, datetime=get_nearest_date(lesson['dateInterval']))
                    )
                else:
                    # Repeated lessons
                    weekday = WEEKDAYS[raw_date]
                    raw_dates = lesson['dateInterval'].split(' - ')
                    from_date, to_date = get_nearest_date(raw_dates[0]), get_nearest_date(raw_dates[1])
                    first_date = from_date if from_date < first_date else first_date
                    last_date = to_date if to_date > last_date else last_date

                    repeated_lessons[weekday].append({'from_date': from_date, 'to_date': to_date,
                                                      'time': lesson["timeInterval"], 'lesson': lesson_object})

        scheduled_lessons += schedule_repeated_lessons(repeated_lessons, first_date, last_date)

        ScheduledLesson.objects.bulk_create(scheduled_lessons)
        Lesson.objects.filter(scheduledlesson__isnull=True).delete()
        LessonPlace.objects.filter(lesson__isnull=True).delete()
        LessonType.objects.filter(lesson__isnull=True).delete()
        LessonTeacher.objects.filter(lessons__isnull=True).delete()
        LessonRoom.objects.filter(lessons__isnull=True).delete()


@transaction.atomic
def update_schedule():
    note_dict = [
        {'lesson_id': note.scheduled_lesson.lesson.id, 'datetime': note.scheduled_lesson.datetime, 'note': note}
        for note in ScheduledLessonNote.objects.all()
    ]
    ScheduledLesson.objects.all().delete()

    group_users = defaultdict(list)
    for student in Student.objects.all():
        group_users[student.group.number].append(student.user)

    groups = {group.number: group for group in Group.objects.filter(number__in=group_users.keys())}

    for group_number, group in groups.items():
        for actual_user in group_users.pop(group_number):
            try:
                schedule = actual_user.schedule(is_session=False)
                session_schedule = actual_user.schedule(is_session=True)
            except ValidationError:
                continue
            else:
                if isinstance(schedule, dict) and schedule.get('status') != 'error':
                    save_schedule(group, schedule)
                if isinstance(session_schedule, dict) and session_schedule.get('status') != 'error':
                    save_schedule(group, session_schedule)
                break

    for note in note_dict:
        note_object = note['note']
        scheduled_lesson = ScheduledLesson.objects.get_or_none(lesson__id=note['lesson_id'], datetime=note['datetime'])
        if scheduled_lesson:
            note_object.scheduled_lesson = scheduled_lesson
            note_object.save()
        else:
            note_object.delete()


def export_scheduled_lessons(scheduled_lessons: QuerySet[ScheduledLesson]) -> Calendar:
    calendar = Calendar()

    for scheduled_lesson in scheduled_lessons:
        lesson = scheduled_lesson.lesson
        calendar.events.add(
            Event(
                name=lesson.title,
                begin=scheduled_lesson.datetime,
                end=scheduled_lesson.end_datetime,
                description='\n'.join([lesson.type.title, lesson.teachers_str if lesson.teachers.exists() else '']),
                created=datetime.now(),
                location=lesson.place.title,
                url=lesson.place.link,
                categories='Расписание МосПолитеха',
                organizer='Робот Политеха'
            )
        )
    return calendar
