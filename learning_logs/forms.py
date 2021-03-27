from django import forms
from .models import Topic, Entry, Dandelion


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title", "description", "public"]
        labels = {"title": "", "description": "", "public": "公开主题"}
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "名称"}),
            "description": forms.Textarea(attrs={"placeholder": "描述"})
        }


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["title", "content"]
        labels = {"title": "", "content": ""}
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "标题"}),
            "content": forms.Textarea(attrs={"placeholder": "内容"})
        }


class DandelionForm(forms.ModelForm):
    class Meta:
        model = Dandelion
        fields = ["content"]
        labels = {"content": ""}
        widgets = {"content": forms.Textarea(attrs={"rows": 3, "placeholder": "送你一支蒲公英，飘在那四季如春的天涯 ~"})}
