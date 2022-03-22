# 后台管理的form
from django import forms

"""和前端用户的输入(form表单)不一样"""


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
