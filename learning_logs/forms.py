from django import forms
from .models import Topic, Article, Dandelion


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title", "description", "public"]
        labels = {"title": "主题的名称", "description": "主题的描述", "public": "公开主题"}
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]
        labels = {"title": "文章的名称", "content": "文章的内容"}
        widgets = {"content": forms.Textarea()}


class DandelionForm(forms.ModelForm):
    class Meta:
        model = Dandelion
        fields = ["content"]
        labels = {"content": ""}
        widgets = {"content": forms.Textarea(attrs={"rows": 3, "placeholder": "送你一支蒲公英，飘在那四季如春的天涯 ~"})}
