from django.urls import path
from .import views

urlpatterns = [
    path('index/',views.index),
    path('',views.get_register, name='get_register'),
    path('get_login/',views.get_login, name='get_login'),
    path('admin_dashboard/,',views.admin_dashboard, name='admin_dashboard'),
    path('developer_dashboard/',views.developer_dashboard, name= 'developer_dashboard'),
    path('project_add/',views.project_add, name= 'project_add'),
    path('task_add/',views.task_add, name= 'task_add'),
    path('task_list/',views.task_list, name= 'task_list'),
    path('user_list/',views.user_list, name= 'user_list'),
    path('task/update/<int:task_id>/', views.update_task_status, name='update_task_status'),
    path('user_logout/',views.user_logout, name='user_logout'),
]