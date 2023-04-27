from django.shortcuts import render
from django.http import FileResponse
import psycopg2
from django import forms


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'