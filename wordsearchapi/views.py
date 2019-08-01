from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models.functions import Length
import time



from .models import Words
from .serializers import WordSerializer

# Create your views here.


def home(request):
    return render(request, 'wordsearchapi/index.html', {})


def search_results(search_string):
    word = Words.objects.filter(word=search_string)[:1]
    if word:
        limit = 24
    else:
        limit = 25
    wordlist_start = Words.objects.filter(word__startswith=search_string).order_by('-usage_count', 'word', Length('word'))[:limit]
    wordlist = word.union(wordlist_start)
    count = len(wordlist)
    if count < 25:
        limit = 25 - count + 1
        wordlist_contains = Words.objects.filter(word__icontains=search_string).order_by('-usage_count', Length('word'))[:limit]
        wordlist = wordlist_start.union(wordlist_contains)
    return wordlist


@api_view(['GET'])
def get_word(request):

    # get details of a word
    if request.method == 'GET':
        if 'word' in request.GET:
            search_string = request.GET['word']
            print("building search results...")
            start_time = time.time()
            word_list = search_results(search_string)
            print(time.time() - start_time)
            serializer = WordSerializer(word_list, many=True)
            return Response(serializer.data)
        else:
            return HttpResponse("Use the following endpoint to search for word: <br/> GET /search?word=&lt;input&gt;")
