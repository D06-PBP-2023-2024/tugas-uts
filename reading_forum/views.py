from django.shortcuts import render, redirect
from .models import Discussion, Reply
from .forms import DiscussionForm, ReplyForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .models import Discussion, Reply
from .forms import DiscussionForm, ReplyForm
from django.contrib.auth.decorators import login_required

from django.db.models import Count

def discussion_list(request):
    filter_by = request.GET.get('filter_by', 'all')  # Ambil parameter 'filter_by' dari URL

    if filter_by == 'replies':
        discussions = Discussion.objects.annotate(num_replies=Count('reply')).filter(num_replies__gt=0)
    elif filter_by == 'noreplies':
        discussions = Discussion.objects.annotate(num_replies=Count('reply')).filter(num_replies=0)
    else:
        discussions = Discussion.objects.all()  # default

    return render(request, 'discussion_list.html', {'discussions': discussions, 'filter_by': filter_by})


def discussion_detail(request, discussion_id):
    discussion = Discussion.objects.get(id=discussion_id)
    replies = Reply.objects.filter(discussion=discussion)
    reply_form = ReplyForm()

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.user = request.user  
            new_reply.discussion = discussion
            new_reply.save()
            return redirect('discussion_detail', discussion_id=discussion_id)

    return render(request, 'discussion_detail.html', {'discussion': discussion, 'replies': replies, 'reply_form': reply_form})

@login_required(login_url='user:login')
def create_discussion(request):
    if request.method == 'POST':
        discussion_form = DiscussionForm(request.POST)
        if discussion_form.is_valid():
            new_discussion = discussion_form.save(commit=False)
            new_discussion.user = request.user  
            new_discussion.save()
            return redirect('discussion_list')
    else:
        discussion_form = DiscussionForm()

    return render(request, 'discussion_form.html', {'discussion_form': discussion_form})

@login_required(login_url='user:login')
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

def reply_form(request, discussion_id):
    discussion = Discussion.objects.get(pk=discussion_id)
    reply_form = ReplyForm()

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.user = request.user
            new_reply.discussion = discussion
            new_reply.save()
            return redirect('reading_forum:discussion_detail', discussion_id=discussion_id)
    
    context = {
        'discussion': discussion,
        'reply_form': reply_form,
    }
    return render(request, 'reply_form.html', context)
