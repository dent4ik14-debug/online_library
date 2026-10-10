from django.shortcuts import render

def index(request):
    context = {
        'title': 'Домашня Сторінка'
    }
    return render(request, 'online_library/index.html', context)