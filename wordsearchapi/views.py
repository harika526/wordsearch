from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import time


from .models import Words
from .serializers import WordSerializer

# Create your views here.


def home(request):
    return render(request, 'wordsearchapi/index.html', {})


def search_results(search_string):
    """ Queries the database for results, passes the queryset to serializer and returns the result """

    # initialize empty list to store the serialized result
    result = []

    # obtain exact match to search string
    word = Words.objects.filter(word=search_string).values("word")
    result.extend(WordSerializer(word, many=True).data)

    # if an exact match is found remaining 24 results should be queried, else 25 results should be queried
    if result:
        limit = 24
    else:
        limit = 25

    # pattern to match words staring with search string and not exact match
    pattern = r'^{}.+'.format(search_string)
    wordlist_start = Words.objects.filter(word__iregex=pattern).values("word")[:limit]
    result.extend(WordSerializer(wordlist_start, many=True).data)
    count = len(result)

    # if results are less than 25 then query the words containing search
    # string in middle to fill the remaining count, else not required
    if count < 25:
        limit = 25 - count + 1
        pattern = r'.+{}.*'.format(search_string)
        wordlist_contains = Words.objects.filter(word__iregex=pattern).values("word")[:limit]
        result.extend(WordSerializer(wordlist_contains, many=True).data)

    return result


@api_view(['GET'])
def get_word(request):

    # get details of a word
    if request.method == 'GET':
        if 'word' in request.GET:
            search_string = request.GET['word']
            print("building search results...")
            start_time = time.time()

            # call search_results() function to get the results
            word_list = search_results(search_string)
            print(time.time() - start_time)
            return Response(word_list)
        else:
            return HttpResponse("Use the following endpoint to search for word: <br/> GET /search?word=&lt;input&gt;")
