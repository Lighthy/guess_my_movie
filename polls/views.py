import random

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import pandas as pd
import os
from django.conf import settings
from process.find_movie import get_most_related_movie
import json


def index(request):
    context = {
        'desc': '',
    }
    return render(request, 'polls/index.html', context)


def find(request):
    context = {}
    return render(request, 'polls/index.html', context)


def find_movie(request):
    data = request.POST.get('desc', False)
    genre = request.POST.get('genre', False)
    result = get_most_related_movie(data, genre).to_json(orient="records")
    json_result = json.loads(result)
    print(json_result)
    return JsonResponse(json_result, safe=False)
