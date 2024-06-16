from django.shortcuts import render,redirect
from .forms import SignupForm,PostForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required,permission_required
from .models import Post
from django.contrib.auth.models import Group,User
from django.http import HttpResponse
# Create your views here.

@login_required(login_url='/login')

def home(request):
    posts=Post.objects.all()
    try:
        if request.method=="POST":
            postid=request.POST.get('post-id')
            userid=request.POST.get('user-id')
            unbanid=request.POST.get('unban-user-id')
            banned=Group.objects.get(name='banned')
            
            if postid:
                post=Post.objects.get(id=postid)
                if post.author==request.user or request.user.has_perm('myapp.delete_post'):
                    post.delete()

            if userid is not None:
                user=User.objects.get(id=userid)
                grpnames=user.groups.all()

                for grp in grpnames:
                    user.groups.remove(grp)

                user.groups.add(banned)
                user.save()
                
            if unbanid is not None:
                default=Group.objects.get(name="default")
                user=User.objects.get(id=unbanid)
                user.groups.remove(banned)
                user.groups.add(default)
                user.save()

    except:
        return HttpResponse('Cannot perform operation')

    return render(request,'home.html',{'posts':posts,'banned_group':Group.objects.get(name"banned")})

def signup(request):
    form=SignupForm()
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid:
            user=form.save()
            login(request,user)
            return redirect(home)
    else:
        form=SignupForm()
    return render(request,'signup.html',{'form':form})

@permission_required('myapp.add_post',login_url='/forbidden')
def createpost(request):
    form=PostForm()
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid:
            user=form.save(commit=False)
            user.author=request.user
            user.save()
            return redirect(home)
    else:
        form=PostForm()
    return render(request,'createpost.html',{'form':form})

@permission_required('myapp.change_post',login_url='/forbidden')
def updatepost(request,pk):
    post=Post.objects.get(id=pk)
    form=PostForm(instance=post)
    if request.method=="POST":
        form=PostForm(request.POST,instance=post)
        if form.is_valid:
            form.save()
            return redirect(home)
    return render(request,'updatepost.html',{'form':form})

def forbidden(request):
    return render(request,'forbidden.html',{})
