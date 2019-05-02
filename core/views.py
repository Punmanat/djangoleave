from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, redirect

# Create your views here.
from djangoleave import settings
from .models import Dayoff
from .forms import DayoffForm
#check group
def is_employee(user):
    return user.groups.filter(name='employee').exists()

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['employee', 'manager']).exists()

def is_manager(user):
    return user.groups.filter(name='manager').exists()

@login_required()
@user_passes_test(is_in_multiple_groups)
def dashboard(req):
    dayoff = Dayoff.objects.filter(create_by=req.user).order_by('date_start')
    context = {
        'dayoff':dayoff
    }
    return render(req, 'core/dashboard.html', context)


@login_required()
@user_passes_test(is_employee, is_manager)
def request(req):
    context = {}
    if req.method == 'POST':
        form = DayoffForm(req.POST)
        if form.is_valid():
            Dayoff.objects.create(
                create_by=req.user,
                reason=form.cleaned_data.get('reason'),
                type=form.cleaned_data.get('type'),
                date_start=form.cleaned_data.get('date_start'),
                end_date=form.cleaned_data.get('end_date')

            )
            context['success'] = 'ส่งแบบฟอร์มสำเร็จ'
    else:
        form = DayoffForm()
    context['form'] = form
    return render(req, 'core/request.html', context)


#Login
def _login(req):
    context = {}
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        groupname = ""
        user = authenticate(req, username=username, password=password)
        if(user):
            groupname = user.groups.get()
        print(groupname)

        if user and str(groupname) == 'employee':
            login(req, user)
            next_url = req.POST.get('next_url')  # hidden field input name
            if next_url:
                return redirect(next_url)
            else:
                return redirect('dashboard')
        elif user and str(groupname) == 'manager':
            login(req, user)
            next_url = req.POST.get('next_url')  # hidden field input name
            if next_url:
                return redirect(next_url)
            else:
                return redirect('/admin/core/dayoff/')
        else:
            error = 'Wrong username or password'
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password'

    next_url = req.GET.get('next')
    if next_url:
        print(next_url)
        context['next_url'] = next_url

    return render(req, 'core/login.html', context=context)

#Logout
def _logout(req):
    logout(req)
    return redirect('login')





