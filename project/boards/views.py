# from django.http import HttpResponse
from django.shortcuts import render

from boards.models import Board


def home(request):
    # import Board model and list all existing boards
    boards = Board.objects.all()
    # boards_names = list()
    #
    # for board in boards:
    #     boards_names.append(board.name)
    #
    # names = '<br>'.join(boards_names)
    #
    # return HttpResponse(names)
    return render(request, 'home.html', {'boards': boards})
