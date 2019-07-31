from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

from .models import Words
from .serializers import WordSerializer

# Create your views here.


def home(request):
    return render(request, 'wordsearchapi/index.html', {})


@api_view(['GET'])
def get_word(request):

    # get details of a word
    if request.method == 'GET':
        if 'word' in request.GET:
            search_string = request.GET['word']
            print("search_string: ", search_string)
            word_search = get_object_or_404(Words, word=search_string)
            print("word_search: ", word_search)
            serializer = WordSerializer(word_search)
            print("serializer: ", serializer.data)
            return Response(serializer.data)
        else:
            return HttpResponse("Use the following endpoint to search for word: <br/> GET /search?word=&lt;input&gt;")
