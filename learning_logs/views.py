from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Topic, Article, Dandelion
from .forms import TopicForm, ArticleForm, DandelionForm


def check_topic_owner(topic, request):
    """ 检查当前主题的作者是否为当前登录的用户 """
    if topic.owner != request.user and topic.public is False:
        raise Http404


def index(request):
    """ 学习笔记的主页 """
    articles = Article.objects.filter(topic__public=True).order_by("-date_added")
    print(articles)
    context = {"articles": articles}
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

    articles = topic.article_set.order_by("-date_added")
    context = {"topic": topic, "articles": articles}
    return render(request, "learning_logs/topic.html", context)


def article(request, article_id):
    """ 显示文章详情 """
    article = get_object_or_404(Article, id=article_id)
    topic = article.topic

    check_topic_owner(topic, request)

    context = {"article": article, "topic": topic}
    return render(request, "learning_logs/article.html", context)


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
    return render(request, "learning_logs/topic_ne.html", context)


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
    return render(request, "learning_logs/topic_ne.html", context)


@login_required
def new_article(request, topic_id):
    """ 添加文章 """
    topic = get_object_or_404(Topic, id=topic_id)

    # 判断该主题作者是否为当前用户
    if topic.owner != request.user:
        raise Http404
    check_topic_owner(topic, request)

    if request.method != "POST":
        # 未提交数据，创建一个空表单
        form = ArticleForm()
    else:
        # POST 提交的数据：对数据进行处理
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.topic = topic
            article.save()
            return redirect("learning_logs:article", article_id=article.id)

    # 显示空表单或指出表单数据无效
    context = {"topic": topic, "form": form, "type": "new"}
    return render(request, "learning_logs/article_ne.html", context)


@login_required
def edit_article(request, article_id):
    """ 编辑文章 """
    article = get_object_or_404(Article, id=article_id)
    topic = article.topic

    # 判断该主题作者是否为当前用户
    if topic.owner != request.user:
        raise Http404
    check_topic_owner(topic, request)

    if request.method != "POST":
        # 初次请求：使用当前条目填充表单
        form = ArticleForm(instance=article)
    else:
        # POST 提交的数据：对数据进行处理
        form = ArticleForm(instance=article, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:article", article_id=article_id)

    context = {"article": article, "topic": topic, "form": form}
    return render(request, "learning_logs/article_ne.html", context)


def squares(request):
    """ 广场主页 """
    form = DandelionForm()
    dandelions = Dandelion.objects.filter(delete=False).order_by("-date_added")
    context = {"dandelions": dandelions, "form": form}
    return render(request, "learning_logs/squares.html", context)


@login_required
def new_dandelion(request):
    """ 添加蒲公英 """
    if request.method == "POST":
        # POST 提交的数据：对数据进行处理
        form = DandelionForm(data=request.POST)
        if form.is_valid():
            new_dandelions = form.save(commit=False)
            new_dandelions.owner = request.user
            new_dandelions.save()
            return redirect("learning_logs:squares")


@login_required
def delete_dandelion(request, dandelion_id):
    """ 删除蒲公英 """
    dandelion = get_object_or_404(Dandelion, id=dandelion_id)
    if dandelion.owner != request.user:
        raise Http404
    else:
        dandelion.delete = True
        dandelion.save()
        return redirect("learning_logs:squares")


def user(request, user_id):
    """ 用户主页 """
    users = get_object_or_404(User, id=user_id)
    context = {"users": users}
    return render(request, "learning_logs/user.html", context)
