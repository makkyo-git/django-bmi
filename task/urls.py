from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    path('', views.taskTop.as_view(), name='task_top'),
    path('build_project/', views.BuildProject.as_view(), name='build_project'),
    path('ProjectPage/<int:pk>/', views.ProjectPage.as_view(), name='our_project'),
    path('ProjectPage/<int:pk>/detail', views.ProjectDetail.as_view(), name='our_project_detail'),
    path('ProjectPage/<int:pk>/update', views.ProjectUpdate.as_view(), name='our_project_update'),
    path('ProjectPage/<int:pk>/delete', views.ProjectDelete.as_view(), name='our_project_delete'),
    path('ProjectPage/<int:pk>/projecttousers_form', views.UpdateProjectMember.as_view(), name='projecttousers_form'),
    path('ProjectPage/<int:pk>/delete_member', views.ProjectDeleteMember.as_view(), name='our_project_delete_member'),
    path('ProjectPage/<int:pk>/AATask', views.AddTaskForAjax.ajax_response, name='add_task'),
    path('ajax/getProjectTaskInfo',views.getProjectTaskInfoAjax.ajax_response, name='getPJTask')
]
