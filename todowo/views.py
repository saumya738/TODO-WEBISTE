from django.shortcuts import render,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect
from .models import Todo
from .forms import TodoForm



def home(request):
    return render(request, 'todowo/home.html')




def signupuser(request):
    if request.method=="GET":
        return render(request,'todowo/signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('/current/',{'user':user})

            except IntegrityError:
                return render(request, 'todowo/signupuser.html',{'error':"Username Already Exist",'form':UserCreationForm()})


        else:
            return render(request,'todowo/signupuser.html',{'error':"Password Didn't match",'form':UserCreationForm()})





def loginuser(request):
    if request.method=="GET":
        return render(request,'todowo/loginuser.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todowo/loginuser.html',{'form':AuthenticationForm(),'error':"Username/Password dosen't match"})

        else:
            login(request, user)
            return redirect('/create/',{'user':user})





def currenttodos(request):
        todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
        if request.method=='GET':
            return render(request, 'todowo/currenttodos.html',{'todos':todos,'form':TodoForm()})
        else:
            try:
                form = TodoForm(request.POST)
                newtodo = form.save(commit=False)
                newtodo.user = request.user
                newtodo.save()
                return redirect('/current/')

            except ValueError:
                return render(request,'todowo/createtodo.html',{'form':TodoForm(),'error':'Bad Data Input'})





def logoutuser(request):
    if request.method=="POST":
        logout(request)
        return redirect('home')
    elif request.method=="GET":
        logout(request)
        return redirect('home')
    else:
        logout(request)
        return redirect('home')



def createtodo(request):
    if request.method=='GET':
        return render(request,'todowo/createtodo.html',{'form':TodoForm()})

    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('/current/')

        except ValueError:
            return render(request,'todowo/createtodo.html',{'form':TodoForm(),'error':'Bad Data Input'})





def viewtodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method=="GET":
        form = TodoForm(instance=todo)
        return render(request,'todowo/viewtodo.html',{'todo':todo,'form':form})
    else:
        try:
            form = TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todowo/viewtodo.html',{'todo':todo,'form':form,'error':"Bad Information"})
