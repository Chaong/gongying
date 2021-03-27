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
    # 添加条目
    path("new_entry/<int:topic_id>/", views.new_entry, name="new_entry"),
    # 编辑条目
    path("edit_entry/<int:entry_id>/", views.edit_entry, name="edit_entry"),
    # 广场主页
    path("squares/", views.squares, name="squares"),
    # 添加蒲公英
    path("new_dandelion/", views.new_dandelion, name="new_dandelion"),
]
