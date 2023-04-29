from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django import forms
from .models import Project, ProjectToUsers

User = get_user_model()

"プロジェクト作成"
class ProjectCreate(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'name', 'leader',
            'start_date', 'end_date',
            'details'
       )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['leader'].widget.attrs['hidden'] = 'true'
        self.fields['start_date'].widget.input_type = "date"
        self.fields['end_date'].widget.input_type="date"

"プロジェクト更新"
class ProjectUpdateForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'name',
            'start_date', 'end_date',
            'details'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['start_date'].widget.input_type = "date"
        self.fields['end_date'].widget.input_type="date"

"プロジェクト削除"
class ProjectDeleteForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'is_delete',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_delete'].widget.attrs['hidden'] = 'true'

"メンバー追加"
class AddProjectMember(forms.ModelForm):

    class Meta:
        model = ProjectToUsers
        fields = (
            'project_cd',
            'user_cd'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        where = []

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['project_cd'].widget.attrs['hidden'] = 'true'

        leader = Project.objects.filter(project_cd=self.initial["project_cd"])
        in_member = ProjectToUsers.objects.filter(project_cd=self.initial["project_cd"])
        staff = User.objects.filter(is_staff=1)
        non_active = User.objects.filter(is_active=0)

        where.append(leader[0].leader_id)
        for in_men in in_member:
            where.append(in_men.user_cd_id)

        for s in staff:
            where.append(s.pk)

        for non in non_active:
            where.append(non.pk)

        result = User.objects.exclude(pk__in=where)

        self.fields['user_cd'].queryset = result
