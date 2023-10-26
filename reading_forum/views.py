from django.shortcuts import render, redirect
from .models import Discussion, Reply
from .forms import DiscussionForm, ReplyForm

def discussion_list(request):
    discussions = Discussion.objects.all()
    return render(request, 'forum_page.html', {'discussions': discussions})

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
            return redirect('forum_detail', discussion_id=discussion_id)

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
