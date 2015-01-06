from urllib import urlencode
import urllib2
from urlparse import urlparse
from django import forms
import json
from django.http.response import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render, redirect
from auth_vk import AuthVk
# from imgs import files
from models import Token
# Create your views here.

class ContactForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

def index(request):

    if request.method == 'GET':
        form = ContactForm()
        return render(request, 'index.html', {
            'form' : form,
        })
    elif request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            auth = AuthVk()
            # Token.objects.all().iterator()
            t, created = Token.objects.get_or_create(id = 1)
            t.token = auth.autorisation(form.cleaned_data['email'], form.cleaned_data['password'])
            t.save()

        return JsonResponse({'route': '/upload'})


class UploadForm(forms.Form):
    photo = forms.FileField()


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # param = {
            #     'gid' : 76955586,
            #     'access_token' : Token.objects.reverse()[0].token,
            #     'v' : 5.25
            # }
            # _url = "https://api.vk.com/method/%s?%s" % ('photos.getWallUploadServer', urlencode(param))
            # upload_params = json.loads(urllib2.urlopen(_url).read())
            res_upload = urllib2.urlopen(upload_params['response']['upload_url'], request.body).read()
            # return HttpResponse(upload_params['response']['upload_url'])
            # res_upload = json.loads(res_upload)
            # # print request.FILES['photo']
            #
            # _data_to_save = {
            #     'access_token': param['access_token'],
            #     'photo': res_upload['photo'],
            #     'server': res_upload['server'],
            #     'hash': res_upload['hash'],
            #     'group_id': 76955586,
            #     'photos_list': '201955485'
            # }
            #
            # _url_to_save = "https://api.vk.com/method/%s" % ('photos.saveWallPhoto',)
            # res = urllib2.urlopen(_url_to_save, urlencode(_data_to_save)).read()

            return HttpResponse(123)
            # action_link = json.loads(urllib2.urlopen(url).read())['response']['upload_url']
            # response = files.send_files(
            #     action_link,
            #     request.FILES,
            # )
            # print  response
            # res = json.loads(urllib2.urlopen(action_link + '?%s' % (urlencode(p),)).read())
            #
            # return render(request, 'upload.html', {
            #     'form' : form,
            #     'response' : res,
            # })
            # handle_uploaded_file(request.FILES['file'])
            # return HttpResponseRedirect('/success/url/')
    else:
        # param = {
        #     'gid' : 76955586,
        #     'access_token' : Token.objects.reverse()[0].token,
        #     'v' : 5.27
        # }
        # _url = "https://api.vk.com/method/%s?%s" % ('photos.getWallUploadServer', urlencode(param))
        param = {
            'owner_id' : -76955586,
            'access_token' : Token.objects.reverse()[0].token,
        }
        _url = "https://api.vk.com/method/%s?%s" % ('photos.getOwnerPhotoUploadServer', urlencode(param))
        upload_url = json.loads(urllib2.urlopen(_url).read())['response']['upload_url']
        form = UploadForm()

        # form.photo
        return render(request, 'upload.html', {
            'form' : form,
            'upload_url' : upload_url,
            })