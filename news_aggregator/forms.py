from django import forms
from .models import Category, Topic, Keyword, APISetting, RSSFeed

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'category']

class KeywordForm(forms.Form):
    keywords = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Enter keywords separated by commas'
        }),
        help_text="Enter keywords separated by commas"
    )
    topic = forms.ModelChoiceField(queryset=Topic.objects.all())

class APISettingForm(forms.ModelForm):
    class Meta:
        model = APISetting
        fields = ['name', 'api_key', 'is_active']
        widgets = {
            'api_key': forms.PasswordInput(),
        }

class RSSFeedForm(forms.ModelForm):
    class Meta:
        model = RSSFeed
        fields = ['name', 'url', 'category', 'is_active']
