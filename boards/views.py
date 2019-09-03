from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import NewTopicForm
from django.http import HttpResponse
from .models import Board, Topic, Post


def home(request):
    board_list = Board.objects.all()
    for board in board_list:
        post_count = 0
        for topic in board.topics.all():
            post_count += topic.posts.count()
        board.post_count = post_count

    return render(request, 'home.html', {'boards': board_list})


def board_topics(request, pk):
    board = Board.objects.get(pk=pk)
    return render(request, 'topics.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            user = User.objects.first()

            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()

            post = Post.objects.create(
                topic=topic,
                message=form.cleaned_data.get('message'),
                created_by=user
            )

            return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()

    return render(request, 'new_topic.html', {'board': board, 'form': form})
