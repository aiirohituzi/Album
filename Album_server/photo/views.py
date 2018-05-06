from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from photo.models import Photo
import json
from django.db.models import Q
from django.http import QueryDict

from photo.forms import PhotoForm
from photo.forms import ImageForm

def getPhoto(request):
    data = []
    
    for item in Photo.objects.all():
        data.append({
            'id': item.id,
            'title': item.title,
            'content': item.content,
            'created': item.created,
        })

    print("Get - Photo")
    data = json.dumps(data, indent=4)
    print(data)
    
    return HttpResponse(data, content_type = "application/json")

def getImage(request):
    data = []
    
    for item in Photo.objects.all():
        data.append({
            'id': item.id,
            'photoId': item.photoId,
            'image': item.image,
            'created': item.created,
        })

    print("Get - Image")
    data = json.dumps(data, indent=4)
    print(data)
    
    return HttpResponse(data, content_type = "application/json")

@csrf_exempt
def uploadPhoto(request):
    result = False

    title = request.POST['title']
    content = request.POST['content']

    photoForm = PhotoForm(request.POST)

    if photoForm.is_valid():
        photo_obj = photoForm.save(commit=False)
        photo_obj.save()

        print("Photo upload request : Upload success")
        result = True
        
    else:
        print("Photo upload request : Upload error")

    return HttpResponse(result)

@csrf_exempt
def uploadImage(request):
    result = False

    # print(request.FILES)
    # print(request.POST)

    photoId = request.POST.get('photoId', False)
    fileCheck = request.FILES.get('image', False)

    if fileCheck:
        if photoId:      # update
            dict = {'photoId': photoId}
        else:           # new upload
            recentUpload = Photo.objects.all().last()
            dict = {'photoId': recentUpload.id,}
            
        qdict = QueryDict('', mutable=True)
        qdict.update(dict)

        imageForm = ImageForm(qdict, request.FILES)

        img_obj = imageForm.save(commit=False)
        img_obj.save()

        print("Image Upload Request : Upload success")
        result = True
    else:
        print("Image Upload Request : Upload error")

    return HttpResponse(result)