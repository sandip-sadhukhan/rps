from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def game(request, id):
    context = {
        'game_id': id
    }
    return render(request, 'game.html', context)
