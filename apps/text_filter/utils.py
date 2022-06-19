from apps.text_filter.models import BadWord


def check_text_for_bad_words(text: str):
    lower_text = text.lower()
    for bad_word in BadWord.objects.all():
        if bad_word.text in lower_text:
            return True
    return False
