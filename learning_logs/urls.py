""" 定义 learning_logs 的 URL 模式 """


from django.urls import path
from . import views


app_name = "learning_logs"
urlpatterns = [
    # 主页
    path("", views.index, name="index"),
    # 显示所有主题
    path("topics/", views.topics, name="topics"),
    # 特定主题的详细页面
    path("topics/<int:topic_id>/", views.topic, name="topic"),
    # 添加主题
    path("new_topic/", views.new_topic, name="new_topic"),
    # 编辑主题
    path("edit_topic/<int:topic_id>/", views.edit_topic, name="edit_topic"),
    # 文章详情
    path("article/<int:article_id>/", views.article, name="article"),
    # 添加文章
    path("new_article/<int:topic_id>/", views.new_article, name="new_article"),
    # 编辑文章
    path("edit_article/<int:article_id>/", views.edit_article, name="edit_article"),
    # 广场主页
    path("squares/", views.squares, name="squares"),
    # 添加蒲公英
    path("new_dandelion/", views.new_dandelion, name="new_dandelion"),
    # 删除蒲公英
    path("delete_dandelion/<int:dandelion_id>/", views.delete_dandelion, name="delete_dandelion"),
    # 用户主页
    path("user/<int:user_id>/", views.user, name="user"),
]
