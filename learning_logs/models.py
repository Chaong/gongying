from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """ 用户学习的主题 """
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=80)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    delete = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """ 返回模型的字符串表示 """
        return self.title


class Entry(models.Model):
    """ 学到的有关某个主题的具体知识 """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField()
    delete = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        """ 返回模型的字符串表示 """
        if len(self.content) > 50:
            return f"{self.content[:50]}..."
        else:
            return self.content


class Dandelion(models.Model):
    """ 广场模块的短信息 """
    content = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    delete = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """ 返回模型的字符串表示 """
        if len(self.content) > 50:
            return f"{self.content[:50]}..."
        else:
            return self.content
