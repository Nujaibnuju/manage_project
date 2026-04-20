from django.shortcuts import render,redirect
from .models import User, Project,Task
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404

# Create your views here.


def index(request):

    return render(request,'index.html')


def get_register(request):

    success = ""

    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        role     = request.POST.get('role')

        
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists!")

        
        user = User.objects.create_user(
            username = username,
            email    = email,
            password = password,
            role     = role,
            is_active = False,
        )

        success = "Registration successfully completed!"

    return render(request, 'register.html',{'success':success})


def get_login(request):

    invalids = ""

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)

            if user.role == 'admin':

                return redirect('admin_dashboard')

            elif user.role == 'student':
                return redirect('developer_dashboard')

        else:

            invalids = "username and password Invalid" 



    return render(request,'login.html',{'invalids':invalids})


def project_add(request):

    msg = ""

    if request.method == 'POST':
        name        = request.POST.get('name')
        description = request.POST.get('description')
       


        Project.objects.create(
            name        = name,
            description = description,
            created_by  = request.user,
        )

        msg = "Project added successfully"

    return render(request,'project_add.html',{'mag':msg})



def task_add(request):

    projects = Project.objects.all()

    developers = User.objects.filter(role='developer')

    if request.method == 'POST':

        title          = request.POST.get('title')
        description    = request.POST.get('description')
        status         = request.POST.get('status')
        project_id     = request.POST.get('project')
        assigned_to_id = request.POST.get('assigned_to')
        due_date       = request.POST.get('due_date')


        Task.objects.create(
            title          = title,
            description    = description,
            status         = status,
            project_id     = project_id,
            assigned_to_id = assigned_to_id,
            due_date       = due_date
        
        )



    return render(request,'task_add.html',{
        'projects': projects,
        'developers': developers,
    })




def task_list(request):

    task = Task.objects.all().order_by('-id')

    return render(request,'task_list.html',{'task':task}) 


def user_list(request):

    users = User.objects.all()

    return render(request,'user_list.html',{'users':users})



def admin_dashboard(request):

    project_count = Project.objects.count() 

    project_list  = Project.objects.all()


    return render(request,'admin_dashboard.html',{
        'projects':project_list,
        'project_count':project_count,
        
        })


def developer_dashboard(request):

    tasks           = Task.objects.filter(assigned_to=request.user)

    task_count      = Task.objects.count()

    completed_count = Task.objects.filter(status='done').count()

    pending_count   = Task.objects.filter(status='in_progress').count()

    projects        = Project.objects.filter(tasks__assigned_to=request.user).distinct()


    return render(request, 'developer_dashboard.html', {
        'task_list': tasks,
        'task_count': task_count,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'list_project':projects,
    })


def update_task_status(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if task.assigned_to == request.user:

        if request.method == "POST":
            new_status    = request.POST.get('status')
            task.status   = new_status
            task.save()

    return redirect('developer_dashboard')


def user_logout(request):
    logout(request)
    return redirect('get_login') 