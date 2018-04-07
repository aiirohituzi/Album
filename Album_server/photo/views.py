from django.shortcuts import render
from django.http import HttpResponse

from photo.models import photo
import json
from django.db.models import Q

# Create your views here.
def getPhoto(request):
    data = []
    
    for item in photo.objects.all():
        data.append({
            'id': item.id,
            'title': item.title,
            'content': item.content,
            'path': item.path,
            'created_at': item.created_at,
        })

    print("Get - Photo")
    data = json.dumps(data, indent=4)
    print(data)
    
    return HttpResponse(data, content_type = "application/json")