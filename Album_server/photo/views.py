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
            recentUpload = Posting.objects.all().last()
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