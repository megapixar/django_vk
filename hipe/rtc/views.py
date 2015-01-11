# Create your views here.
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from rtc.models import Chat


def index(request):

    return render(request, 'rtc/index.html')

offer_data = {}
@csrf_exempt
def offer(request):
    if(request.method == 'POST'):
        Chat.objects.update_or_create(id=1, defaults = {'offer' : request.POST['offer'], 'answer' : ''})
    return JsonResponse({'offer':request.POST['offer']})

@csrf_exempt
def answer(request):
    if(request.method == 'POST'):
        Chat.objects.update_or_create(id=1, defaults = {'answer' : request.POST['answer']})
    return JsonResponse({'answer':request.POST['answer']})


@csrf_exempt
def get_offer(request):
    chat = Chat.objects.get(pk=1)
    result = {}
    if chat.offer:
        result = json.loads(chat.offer)

    return JsonResponse(result)


def get_answer(request):
    chat = Chat.objects.get(pk=1)
    result = {}
    if chat.answer:
        result = json.loads(chat.answer)

    return JsonResponse(result)

@csrf_exempt
def candidate(request):
    type = request.POST['type']
    Chat.objects.update_or_create(id=1, defaults = {type + '_candidate' : request.POST['candidate'], 'answer' : ''})
    chat = Chat.objects.get(pk=1)
    result = {}
    response_type = 'offer_candidate'
    if type == 'offer':
        response_type = 'answer_candidate'

    if getattr(chat, response_type):
        result = json.loads(getattr(chat, response_type))

    return JsonResponse(result)