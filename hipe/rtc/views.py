# Create your views here.
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.cache import cache
from collections import deque

from rtc.models import Chat

def one_tab(request):
    return render(request, 'rtc/one_tab.html')

def index(request):
    return render(request, 'rtc/index.html')

@csrf_exempt
def offer(request):
    if(request.method == 'POST'):
        # Chat.objects.update_or_create(id=1, defaults = {'offer' : request.POST['offer'], 'ans' : ''})
        cache.set('offer', request.POST['offer'])

    return JsonResponse({'offer':cache.get('offer')})

@csrf_exempt
def answer(request):

    # chat = Chat.objects.get(id=1)
    # chat.ans = request.POST['answer']
    # chat.save(update_fields=['ans'])
    cache.set('answer', request.POST['answer'])

    return JsonResponse({'answer': cache.get('answer')})


@csrf_exempt
def get_offer(request):
    # chat = Chat.objects.get(pk=1)
    # result = {}
    # if chat.offer:
    #     result = json.loads(chat.offer)
    offer = cache.get('offer')
    result = {}
    if offer is not None:
        result = json.loads(offer)
        cache.delete('offer')

    return JsonResponse(result)

@csrf_exempt
def get_answer(request):
    # chat = Chat.objects.get(pk=1)
    # result = {}
    # if chat.ans:
    #     result = json.loads(chat.ans)
    # return JsonResponse(result)
    answer = cache.get('answer')
    cache.delete('answer')
    return JsonResponse(json.loads(answer) if answer is not None else {})

@csrf_exempt
def candidate(request):
    type = request.POST['type']
    candidate = request.POST['candidate']
    num = request.POST.get('num', None)

    if candidate and num is not None :
        cache.set(type + '_candidate_' + num, candidate)

    result = {}
    response_type = 'offer_candidate_' if type == 'answer' else 'answer_candidate_'

    for i in range(50):
        cache_key = response_type + str(i)
        r = cache.get(cache_key)
        if r is not None:
            result = json.loads(r)
            cache.delete(cache_key)
            break

    return JsonResponse(result)

# Data Channel
def datachannel(request):

    return render(request, 'rtc/data_channel/index.html')