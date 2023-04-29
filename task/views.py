from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, resolve_url, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import models
from .models import ProjectToUsers, Project
from .forms import ProjectCreate, ProjectUpdateForm, ProjectDeleteForm, AddProjectMember

from django.views.generic.edit import DeleteView

from django.urls import reverse_lazy

from django.http.response import JsonResponse
from django.core import serializers
from .models import ProjectToUsers, Project, ProjectToTask, Task

from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

"トップページ"
class taskTop(LoginRequiredMixin, generic.TemplateView):
    template_name = 'task/task_top.html'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        project_user = ProjectToUsers.objects.filter(user_cd=user.pk)
        leader = Project.objects.filter(leader=user.pk, is_delete=0)

        if len(project_user) > 0:
            context['member'] = []
            for person in project_user:
                member = Project.objects.filter(project_cd=person.project_cd.pk, is_delete=0)
                context['member'].extend(member)
        else:
            context['member'] = None
  
        context['leader'] = leader if len(leader) > 0 else None

        return context

"プロジェクト作成"
class BuildProject(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectCreate
    success_url = '/task/'
    template_name = 'task/build_project.html'

    def get_initial(self):
        leader = self.request.user.pk
        return {'leader': leader,}

"プロジェクト限定"
class ProjectUserOnlyMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        is_return = True

        user = self.request.user

        l_result = Project.objects.filter(leader=user.id, project_cd=self.kwargs["pk"])
        m_result = ProjectToUsers.objects.filter(project_cd=self.kwargs["pk"], user_cd=self.request.user.pk)
        p_result = Project.objects.filter(project_cd=self.kwargs["pk"], is_delete=0)

        if len(l_result) == 0 and len(m_result) == 0:
            is_return = False

        if len(p_result) == 0:
            is_return = False

        return is_return

"プロジェクトページ"
class ProjectPage(ProjectUserOnlyMixin, generic.TemplateView):
    template_name = 'task/our_project.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        project = Project.objects.filter(project_cd=self.kwargs["pk"])
        p_user = ProjectToUsers.objects.filter(project_cd=self.kwargs["pk"])

        if len(p_user) > 0:
            context['member'] = []
            for person in p_user:
                member = User.objects.filter(pk=person.user_cd.pk)
                context['member'].extend(member)
        else:
            context['member'] = None

        context['project'] = project if len(project) > 0 else None
        context['task'] = None

        return context

"プロジェクトリーダー限定"
class ProjectLeaderOnlyMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        is_return = True

        user = self.request.user

        l_result = Project.objects.filter(leader=user.id, project_cd=self.kwargs["pk"])
        p_result = Project.objects.filter(project_cd=self.kwargs["pk"], is_delete=0)

        if len(l_result) == 0:
            is_return = False

        if len(p_result) == 0:
            is_return = False

        return is_return

"プロジェクト情報"
class ProjectDetail(ProjectUserOnlyMixin, generic.DetailView):
    model = Project
    templates_name = 'task/project_detail.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        p_user = ProjectToUsers.objects.filter(project_cd=self.kwargs["pk"])
        project = Project.objects.filter(project_cd=self.kwargs["pk"], is_delete=0)

        context['member'] = p_user if len(p_user) > 0 else None

        context['project'] = project if len(project) > 0 else None

        return context

"プロジェクト更新ページ"
class ProjectUpdate(ProjectUserOnlyMixin, generic.UpdateView):
    model = Project
    template_name = 'task/project_update.html'
    form_class = ProjectUpdateForm

    def get_success_url(self):
        return resolve_url('task:our_project_detail', pk=self.kwargs["pk"])

"プロジェクト削除ページ"
class ProjectDelete(ProjectLeaderOnlyMixin, generic.UpdateView):
    model = Project
    template_name = 'task/project_delete.html'
    form_class = ProjectDeleteForm

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        p_user = ProjectToUsers.objects.filter(project_cd=self.kwargs["pk"])
        project = Project.objects.filter(project_cd=self.kwargs["pk"], is_delete=0)

        if len(p_user) > 0:
            context['member'] =[]
            for person in p_user:
                member = User.objects.filter(pk=person.user_cd.pk)
                context['member'].extend(member)
        else:
            context['member'] = None

        context['project'] = project if len(project) > 0 else None

        return context

    def get_initial(self):
        return {'is_delete': True,}

    def get_success_url(self):
        return resolve_url('task:task_top')

"プロジェクトメンバー追加"


"プロジェクトメンバー更新"
class UpdateProjectMember(ProjectUserOnlyMixin, generic.CreateView):
    model = ProjectToUsers
    templates_name = "task/projecttousers_form.html"
    form_class = AddProjectMember

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        p_user = ProjectToUsers.objects.filter(project_cd=self.kwargs["pk"])
        project = Project.objects.filter(project_cd=self.kwargs["pk"], is_delete=0)

        context['member'] = p_user if len(p_user) > 0 else None

        context['project'] = project if len(project) > 0 else None

        return context

    def get_success_url(self):
        return resolve_url('task:projecttousers_form', pk=self.kwargs["pk"])

    def get_initial(self):
        pc = self.kwargs["pk"]
        return {'project_cd': pc,}

"プロジェクトメンバー削除"
class ProjectDeleteMember(ProjectLeaderOnlyMixin, generic.DeleteView):
    model = ProjectToUsers
    success_url = reverse_lazy('task:projecttousers_form')

    def post(self, request, *args, **kwargs):
        delete_ids = request.POST.getlist('delete_ids')
        if delete_ids:
            ProjectToUsers.objects.filter(id__in=delete_ids).delete()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        return super().form_valid(form)

"タスク追加"
class AddTaskForAjax():

    def ajax_response(self, *args, **kwargs):
        taskName = self.POST['taskName']

        if self.POST['user'] != "":
            user = User.objects.get(pk=self.POST['user'])
        else:
            user = None

        if user == None:
            userName = self.POST['userName'] if self.POST['userName'] != "" else None
        else:
            userName =  None

        details = self.POST['details'] if self.POST['details'] != "" else None
        startDate = self.POST['startDate'] if self.POST['startDate'] != "" else None
        endDate = self.POST['endDate'] if self.POST['endDate'] != "" else None
        priolity = self.POST['priolity'] if self.POST['priolity'] != "" else None

        task = Task.objects.create(
            task_name=taskName, user=user,
            user_name=userName, details=details,
            start_date=startDate, end_date=endDate,
            priolity=priolity
        )

        projectCd = kwargs['pk']

        project = Project.objects.get(project_cd=projectCd)

        result = ProjectToTask.objects.create(
            project_cd=project, task_cd=task
        )

        projectTask = ManupilateDataBase.getProjectTask(projectCd)
 
        json_serializer = serializers.get_serializer("json")()
        taskData = json_serializer.serialize(projectTask, ensure_ascii=False)

        return JsonResponse({"taskdata" : taskData})
  

" DB操作クラス "
class ManupilateDataBase():
    
    def getJoinProject(joinCd):
        p_user = ProjectToUsers.objects.filter(user_cd=joinCd)

        if len(p_user) > 0:
            result = []
            for p in p_user:
                member = Project.objects.filter(project_cd=p.project_cd.pk, is_delete=0)
                result.extend(member)

        else:
            result = None

        return result

    def getProjectTask(projectCd):
        p_task = ProjectToTask.objects.filter(project_cd=projectCd)

        if len(p_task) > 0:
                task = Task.objects.filter(projecttotask__project_cd=projectCd)
                return task if task.exists() else None

    def getProjectMember(memberCd):
        p_user =  ProjectToUsers.objects.filter(project_cd=memberCd)

        if len(p_user) > 0:
            result = []
            for person in p_user:
                member = User.objects.filter(pk=person.user_cd.pk)
                result.extend(member)
        else:
            result = None

        return result

    def getTaskInfo(taskCd):
        task = Task.objects.filter(task_cd=taskCd)

        if len(task) > 0:
            return task
        else:
            return None

    def getUserInfo(userCd):
        user = User.objects.filter(use_cd=userCd)

        if len(user) > 0:
            return user
        else:
            return None

"プロジェクトタスク情報取得"
class getProjectTaskInfoAjax():

    @csrf_exempt
    def ajax_response(self, *args, **kwargs):
        task_cd = self.POST['task_cd']

        projectTask = ManupilateDataBase.getTaskInfo(task_cd)

        if (projectTask[0].user != None):
            projectTask[0].user_name = projectTask[0].user.username

        json_serializer = serializers.get_serializer("json")()
        taskData = json_serializer.serialize(projectTask, ensure_ascii=False)

        return JsonResponse({"taskdata" : taskData})
