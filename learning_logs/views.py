from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q
from .models import Topic, Entry, Dandelion
from .forms import TopicForm, EntryForm, DandelionForm


def check_topic_owner(topic, request):
    """ 检查当前主题的作者是否为当前登录的用户 """
    if topic.owner != request.user and topic.public is False:
        raise Http404


# Create your views here.
def index(request):
    """ 学习笔记的主页 """
    topics = Topic.objects.filter(public=True).order_by("-date_added")
    context = {"topics": topics}
    return render(request, "learning_logs/index.html", context)


def topics(request):
    """ 显示所有的主题 """
    if request.user.is_authenticated:
        topics = Topic.objects.filter(Q(owner=request.user) | Q(public=True)).order_by("-date_added")
    else:
        topics = Topic.objects.filter(public=True).order_by("-date_added")
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


def topic(request, topic_id):
    """ 显示特定主题及其所有的条目 """
    topic = get_object_or_404(Topic, id=topic_id)

    check_topic_owner(topic, request)

    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """ 添加新主题 """
    if request.method != "POST":
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST 提交的数据：对数据进行处理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("learning_logs:topics")

    # 显示空表单或指出表单数据无效
    context = {"form": form, "type": "new"}
    return render(request, "learning_logs/topic_new_edit.html", context)


@login_required
def edit_topic(request, topic_id):
    """ 编辑主题 """
    topic = get_object_or_404(Topic, id=topic_id)

    # 判断该主题作者是否为当前用户
    if topic.owner != request.user:
        raise Http404
    check_topic_owner(topic, request)

    if request.method != "POST":
        # 初次请求：使用当前条目填充表单
        form = TopicForm(instance=topic)
    else:
        # POST 提交的数据：对数据进行处理
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/topic_new_edit.html", context)


@login_required
def new_entry(request, topic_id):
    """ 添加新条目 """
    topic = get_object_or_404(Topic, id=topic_id)

    # 判断该主题作者是否为当前用户
    if topic.owner != request.user:
        raise Http404
    check_topic_owner(topic, request)

    if request.method != "POST":
        # 未提交数据，创建一个空表单
        form = EntryForm()
    else:
        # POST 提交的数据：对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    # 显示空表单或指出表单数据无效
    context = {"topic": topic, "form": form, "type": "new"}
    return render(request, "learning_logs/entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """ 编辑条目 """
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    # 判断该主题作者是否为当前用户
    if topic.owner != request.user:
        raise Http404
    check_topic_owner(topic, request)

    if request.method != "POST":
        # 初次请求：使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST 提交的数据：对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/entry.html", context)


def squares(request):
    """ 广场主页 """
    form = DandelionForm()
    dandelions = Dandelion.objects.order_by("-date_added")
    context = {"dandelions": dandelions, "form": form}
    return render(request, "learning_logs/squares.html", context)


@login_required
def new_dandelion(request):
    """ 添加蒲公英 """
    if request.method != "POST":
        # 未提交数据：创建一个新表单
        form = DandelionForm()
    else:
        # POST 提交的数据：对数据进行处理
        form = DandelionForm(data=request.POST)
        if form.is_valid():
            new_dandelions = form.save(commit=False)
            new_dandelions.owner = request.user
            new_dandelions.save()
            return redirect("learning_logs:squares")

    # 显示空表单或指出表单数据无效
    context = {"form": form}
    return render(request, "learning_logs/squares.html", context)
