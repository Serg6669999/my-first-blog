from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def post_list(request):
    return render(request, 'blog/post_list.html', {})
# Create your views here.
