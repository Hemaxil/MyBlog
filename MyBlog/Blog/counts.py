import re
import datetime
import math
from django.utils.html import strip_tags

def count_words(html_string):
    word_string=strip_tags(html_string)
    count=len(re.findall(r'\w+',word_string))
    return count


#readtime ---1 min---200 words
#1word---60sec/200

def get_read_time(html_string):
    count=count_words(html_string)
    read_time_min=math.ceil((1.0/200)*count)
    readtime=str(datetime.timedelta(minutes=read_time_min))
    return readtime
