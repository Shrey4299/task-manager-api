from django.urls import path
from .views import TaskList, TaskDetail, TaskSearch, UserTaskDetails, UserTaskList

urlpatterns = [
    path('task/', TaskList.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('tasks/', UserTaskList.as_view(), name='user-task-list'),
    path('tasks/<int:task_id>/', UserTaskDetails.as_view(), name='user-task-details'),
    path('tasks/search/', TaskSearch.as_view(), name='task-search'),


]
