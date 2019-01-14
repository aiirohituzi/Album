# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from photo.models import Photo
from photo.models import Images
import json
import os
from django.conf import settings
from django.db.models import Q
from django.http import QueryDict

from photo.forms import PhotoForm
from photo.forms import ImageForm

from django.contrib.auth import authenticate

from django.contrib.auth import login

from rest_framework.authtoken.models import Token

from Crypto.Hash import SHA256
import time
import random
from photo.models import Key
from photo.forms import KeyForm

import datetime
from django.utils import timezone


def getPhoto(request):
    data = []
    
    for item in Photo.objects.all().order_by('-created'):
        data.append({
            'id': item.id,
            'title': item.title,
            'content': item.content,
            'created': str(item.created),
        })

    print("Get - Photo")
    data = json.dumps(data, indent=4)
    print(data)
    
    return HttpResponse(data, content_type = "application/json")

def getImage(request):
    data = []
    
    for item in Images.objects.all():
        data.append({
            'id': item.id,
            'photoId': item.photoId.id,
            'image': str(item.image),
            'created': str(item.created),
        })

    print(data)
    print("Get - Image")
    data = json.dumps(data, indent=4)
    print(data)
    
    return HttpResponse(data, content_type = "application/json")

def getRecentPhoto(request):
    data = []

    if (Photo.objects.all().count() > 3):
        for item in Photo.objects.all().order_by('-created')[:3]:
            data.append({
                'id': item.id,
                'title': item.title,
                'content': item.content,
                'created': str(item.created),
            })
    else:
        for item in Photo.objects.all().order_by('-created'):
            data.append({
                'id': item.id,
                'title': item.title,
                'content': item.content,
                'created': str(item.created),
            })

    print("Get - Recent Photo")
    data = json.dumps(data, indent=4)
    print(data)
    
    return HttpResponse(data, content_type = "application/json")

@csrf_exempt
def uploadPhoto(request):
    result = False

    token = request.POST['Token']
    title = request.POST['title']
    content = request.POST['content']

    photoForm = PhotoForm(request.POST)

    if not tokenCheck(token):
        return HttpResponse('Unauthorized', status=401)

    if photoForm.is_valid():
        photo_obj = photoForm.save(commit=False)
        photo_obj.save()

        print("Post - Photo upload request : Upload success")
        result = True
        
    else:
        print("Post - Photo upload request : Upload error")

    return HttpResponse(result)

@csrf_exempt
def uploadImage(request):
    result = False

    token = request.POST['Token']
    photoId = request.POST.get('photoId', False)
    fileCheck = request.FILES.get('image', False)

    if not tokenCheck(token):
        return HttpResponse('Unauthorized', status=401)

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

        print("Post - Image Upload Request : Upload success")
        result = True
    else:
        print("Post - Image Upload Request : Upload error")

    return HttpResponse(result)


@csrf_exempt
def deletePhoto(request):

    token = request.POST['Token']
    photoId = request.POST['photoId']

    result = False
    log = ''

    if not tokenCheck(token):
        return HttpResponse('Unauthorized', status=401)

    try:
        row = Photo.objects.get(id=photoId)
    except Photo.DoesNotExist:
        print("Post - Delete Photo Request : [Failed]No Photo matches the given query.")
        return HttpResponse(result)
    
    if row != None:
        log += 'Post - Delete Photo Request : photo ' + str(row.id) + ' delete success'

        isEmpty = False
        try:
            img_obj = Images.objects.filter(photoId=row.id)
        except Images.DoesNotExist:
            isEmpty = True

        if(not isEmpty):        # have image
            for img_row in img_obj:
                file_path = os.path.join(settings.FILES_DIR, str(img_row.image))
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(str(img_row.image) + "image delete")
                else:
                    print("image delete error")
                    return HttpResponse(result)
        else:
            print("not image")


        row.delete()
        print(log)
        result = True
    else:
        print("Post - Delete Photo Request : Delete error")

    return HttpResponse(result)


@csrf_exempt
def deleteSelectedPhoto(request):

    token = request.POST['Token']
    photoIdSet = request.POST['photoIdSet'].split(',')
    print(photoIdSet)

    result = False
    log = ''

    if not tokenCheck(token):
        return HttpResponse('Unauthorized', status=401)


    for photoId in photoIdSet:
        print(photoId)
        try:
            row = Photo.objects.get(id=photoId)
        except Photo.DoesNotExist:
            print("Post - Delete Photo " + photoId + " Request : [Failed]No Photo matches the given query.")
            return HttpResponse(result)
        
        if row != None:
            log += 'Post - Delete Photo Request : photo ' + str(row.id) + ' delete success'

            isEmpty = False
            try:
                img_obj = Images.objects.filter(photoId=row.id)
            except Images.DoesNotExist:
                isEmpty = True

            if(not isEmpty):        # have image
                for img_row in img_obj:
                    file_path = os.path.join(settings.FILES_DIR, str(img_row.image))
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(str(img_row.image) + "image delete")
                    else:
                        print("image delete error")
                        return HttpResponse(result)
            else:
                print("not image")


            row.delete()
            print(log)
            result = True
        else:
            print("Post - Delete Photo Request : Delete error")

    return HttpResponse(result)



@csrf_exempt
def searchPhoto(request):
    data = []
    
    category = request.GET.get('category', 'title')
    keyword = request.GET.get('keyword', False)
    date = request.GET.get('date', 'all')

    if keyword == 'null':
        keyword = False

    start = None
    if date == 'week':
        td = datetime.timedelta(days=7)
        start = timezone.now() - td
    elif date == 'month':
        td = datetime.timedelta(days=30)
        start = timezone.now() - td
    elif date == 'year':
        td = datetime.timedelta(days=365)
        start = timezone.now() - td    
    
    end = timezone.now() + datetime.timedelta(days=1)
    # print(start)
    # print(end)
    if keyword:
        if category == 'title':
            if date == 'all':
                queryset = Photo.objects.filter(title__icontains=keyword).order_by('-created')
            else:
                queryset = Photo.objects.filter(Q(title__icontains=keyword) & Q(created__range=[start, end])).order_by('-created')
        elif category == 'content':
            if date == 'all':
                queryset = Photo.objects.filter(content__icontains=keyword).order_by('-created')
            else:
                queryset = Photo.objects.filter(Q(content__icontains=keyword) & Q(created__range=[start, end])).order_by('-created')
        elif category == 'all':
            if date == 'all':
                queryset = Photo.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by('-created')
            else:
                queryset = Photo.objects.filter((Q(title__icontains=keyword) | Q(content__icontains=keyword)) & Q(created__range=[start, end])).order_by('-created')

    else:
        if date == 'all':
            queryset = Photo.objects.all().order_by('-created')
        else:
            queryset = Photo.objects.filter(created__range=[start, end]).order_by('-created')
    

    if queryset.exists():
        for row in queryset:
            data.append({'id': row.id, 'title': row.title, 'content': row.content, 'created': str(row.created)})

        data = json.dumps(data, indent=4)
    else:
        data = False
    print(data)
    print("Get - Search Photo")
    return HttpResponse(data, content_type = "application/json")



@csrf_exempt
def updatePhoto(request):
    token = request.POST['Token']
    photoId = request.POST['photoId']
    title = request.POST['title']
    content = request.POST['content']
    fileCheck = request.FILES.get('image', False)

    result = False
    log = ''

    if not tokenCheck(token):
        return HttpResponse('Unauthorized', status=401)
        
    try:
        row = Photo.objects.get(id=photoId)
    except Photo.DoesNotExist:
        print("Post - Update Photo Request : [Failed]No Photo matches the given query.")
        return HttpResponse(result)

    if row != None:
        row.title = title
        row.content = content

        try:
            img_obj = Images.objects.filter(photoId=photoId)
        except Images.DoesNotExist:
            print(" - [ERROR] This photo have not image.")
            return HttpResponse(result)

        if(fileCheck):    # image re-upload
            for img_row in img_obj:
                file_path = os.path.join(settings.FILES_DIR, str(img_row.image))
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    print("image delete error")
                    return HttpResponse(result)
                img_row.delete()

        row.save()
        log += 'Post - Update Photo Request : photo ' + str(row.id) + ' Update success'
        print(log)
        result = True
    else:
        print("Post - Update Photo Request : Update error")

    return HttpResponse(result)



@csrf_exempt
def signIn(request):
    print('Admin Login Request...')
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)

    user = authenticate(username=username, password=password)

    if user is not None:
        key = str(random.randrange(1000000000, 10000000000)) + str(time.strftime("%d/%m/%Y"))
        token = str(Token.objects.get(user__username='admin')) + key

        # print(key)
        # print(token)

        try:
            key_obj = Key.objects.get(name=username)
        except Key.DoesNotExist:
            dict = {'name': username, 'key': key}
            qdict = QueryDict('', mutable=True)
            qdict.update(dict)

            keyForm = KeyForm(qdict)
            key_obj = keyForm.save(commit=False)
            key_obj.save()

        key_obj.key = key
        key_obj.save()


        hash = SHA256.new(data=token.encode())
        # print(hash.digest())
        return HttpResponse(str(hash.digest()))
    else:
        return HttpResponse(False)


# def userCheck(username, password):
#     user = authenticate(username=username, password=password)

#     print(user)
#     if user is not None:
#         return True
#     else:
#         return False


def tokenCheck(token):
    tokenA = str(Token.objects.get(user__username='admin')) + str(Key.objects.get(name='admin').key)
    # print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    # print(Key.objects.get(name='admin').key)
    # print(tokenA)

    hash = SHA256.new(data=tokenA.encode())
    tokenA_hash = str(hash.digest())

    # print(token)
    # print(tokenA_hash)
    # print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    
    if token == tokenA_hash:
        return True
    else:
        return False