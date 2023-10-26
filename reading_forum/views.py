from django.shortcuts import render, redirect
from .models import Discussion, Reply
from .forms import DiscussionForm, ReplyForm
from django.contrib.auth.decorators import login_required

def discussion_list(request):
    discussions = Discussion.objects.all()
    return render(request, 'discussion_list.html', {'discussions': discussions})

def discussion_detail(request, discussion_id):
    discussion = Discussion.objects.get(id=discussion_id)
    replies = Reply.objects.filter(discussion=discussion)
    reply_form = ReplyForm()

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.user = request.user  # Set the user as the current logged-in user
            new_reply.discussion = discussion
            new_reply.save()
            return redirect('discussion_detail', discussion_id=discussion_id)

    return render(request, 'discussion_detail.html', {'discussion': discussion, 'replies': replies, 'reply_form': reply_form})


def create_discussion(request):
    if request.method == 'POST':
        discussion_form = DiscussionForm(request.POST)
        if discussion_form.is_valid():
            new_discussion = discussion_form.save(commit=False)
            new_discussion.user = request.user  # Set the user as the current logged-in user
            new_discussion.save()
            return redirect('discussion_list')
    else:
        discussion_form = DiscussionForm()

    return render(request, 'discussion_form.html', {'discussion_form': discussion_form})


def create_reply(request, discussion_id):
    discussion = Discussion.objects.get(pk=discussion_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.discussion = discussion
            reply.user = request.user  # Atur pengguna yang membuat balasan
            reply.save()
            return redirect('discussion_detail', discussion_id=discussion_id)

    return redirect('discussion_list')

