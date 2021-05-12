import datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

# Create your views here.
def charge(in_time, out_time):
    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    diff = out_time - in_time

    return diff.seconds/60*0.25
