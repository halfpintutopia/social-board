# from django.http import HttpResponse
# from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from boards.forms import NewTopicForm, PostForm
from boards.models import Board, Post, Topic


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


def board_topics(request, pk):
    # To show a 404 Page Not found rather than 500 Internal Server Error page
    # try:
    #     board = Board.objects.get(pk=pk)
    # except Board.DoesNotExist:
    #     raise Http404

    # Refactored to:
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    # TODO: get the currently logged in user
    # user = User.objects.first()

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            # Redirect to the created topic page
            # IMPORTANT: using topic.pk because a `topic` is an object (Topic Model Instance) and assessing the pk property of the Topic model instance.
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)

    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    # board__pk
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})


# A new view protected by @login_required
@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            # IMPORTANT: using topic_pk as referring to the keyword argument of the function.
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
