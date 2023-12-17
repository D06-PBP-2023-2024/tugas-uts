from django.shortcuts import render, redirect
from .models import Discussion, Reply
from .forms import DiscussionForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json


from django.db.models import Count

@csrf_exempt
def discussion_list(request):
    filter_by = request.GET.get('filter_by', 'all')  # Ambil parameter 'filter_by' dari URL

    if filter_by == 'replies':
        discussions = Discussion.objects.annotate(num_replies=Count('reply')).filter(num_replies__gt=0)
    elif filter_by == 'noreplies':
        discussions = Discussion.objects.annotate(num_replies=Count('reply')).filter(num_replies=0)
    else:
        discussions = Discussion.objects.all()  # default

    return render(request, 'discussion_list.html', {'discussions': discussions, 'filter_by': filter_by})


@csrf_exempt
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

    return render(request, 'discussion_detail.html', {'discussion': discussion, 'replies': replies, 'reply_form': reply_form, 'discussion_id': discussion_id})

@csrf_exempt
@login_required(login_url='user:login')
def create_discussion(request):
    if request.method == 'POST':
        discussion_form = DiscussionForm(request.POST)
        if discussion_form.is_valid():
            new_discussion = discussion_form.save(commit=False)
            new_discussion.user = request.user  
            new_discussion.save()
            return redirect('reading_forum:discussion_list')
    else:
        discussion_form = DiscussionForm()

    return render(request, 'discussion_form.html', {'discussion_form': discussion_form})

@csrf_exempt
def create_discussion_flutter(request):
    if request.method == 'POST':
        discussion_form = DiscussionForm(request.POST)
        if discussion_form.is_valid():
            new_discussion = discussion_form.save(commit=False)
            new_discussion.user = request.user  
            new_discussion.save()
            response_data = {'success': 'Discussion created successfully.'}
            return JsonResponse(response_data)
    


@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
def reply_form_by_AJAX(request, discussion_id):
    if request.method == 'POST' and request.is_ajax():
        discussion = Discussion.objects.get(pk=discussion_id)
        reply_form = ReplyForm(request.POST)

        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.user = request.user
            new_reply.discussion = discussion
            new_reply.save()
            response_data = {'success': 'Reply saved successfully.'}
            return JsonResponse(response_data)

        errors = reply_form.errors.as_json()
        response_data = {'errors': errors}
        return JsonResponse(response_data, status=400)

    return JsonResponse({'error': 'Invalid request.'}, status=400)

def discussion_detail_json(request, discussion_id):
    discussion = Discussion.objects.get(id=discussion_id)
    replies = Reply.objects.filter(discussion=discussion)
    model_data = {
        "pk": discussion.pk,
        "title": discussion.title,
        "created_at": discussion.created_at.strftime("%d %B %Y %H:%M"), # "20 November 2020 20:00
        "content": discussion.content,
        "user": discussion.user.username,
        "replies": []
        }
    for item in replies:
        temp = {
            "pk": item.pk,
            "created_at": item.created_at.strftime("%d %B %Y %H:%M"),
            "content": item.content,
            "user": item.user.username,
        }
        model_data["replies"].append(temp)

    json_data = json.dumps(model_data)
    return HttpResponse(json_data, content_type="application/json")

def discussion_list_json(request):
    filter_by = request.GET.get('filter_by', 'all')

    if filter_by == 'replies':
        discussions = Discussion.objects.annotate(num_replies=Count('replies')).filter(num_replies__gt=0)
    elif filter_by == 'noreplies':
        discussions = Discussion.objects.annotate(num_replies=Count('replies')).filter(num_replies=0)
    else:
        discussions = Discussion.objects.all()

    discussions_list = [
        {
            'id': discussion.id,
            'title': discussion.title,
            'content': discussion.content,
            'created_at': discussion.created_at.strftime("%d %B %Y %H:%M"),
            'user': discussion.user.username,
            'num_replies': discussion.num_replies  
        }
        for discussion in discussions
    ]

    response_data = {'discussions': discussions_list, 'filter_by': filter_by}
    return JsonResponse(response_data, safe=False)