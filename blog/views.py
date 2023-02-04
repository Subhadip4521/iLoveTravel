from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from blog.models import Post, BlogComment
from blog.templatetags import extras

# Create your views here.

def bloghome(request):
    # return HttpResponse('This is bloghome page.')
    allposts= Post.objects.all()
    # print(allposts)
    context= {'allposts':allposts}
    return render(request, 'blog/bloghome.html',context)

def blogpost(request,slug):
    # return HttpResponse(f'This is blogppost page: {slug}')
    post= Post.objects.filter(slug=slug).first()
    post.views= post.views+1
    post.save()
    
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)


    context={'post':post, 'comments':comments, 'user':request.user, 'replyDict':replyDict}
    return render(request, 'blog/blogpost.html', context)


def postComment(request):
    if request.method=='POST':
        comment= request.POST.get("comment")
        user= request.user
        postSno= request.POST.get("postSno")
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get("parentSno")


        if parentSno=="":
            comment= BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, 'Your comment has been posted successfully.')

        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment= BlogComment(comment= comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, 'Your reply has been posted successfully.')

    return redirect(f'/blog/{post.slug}')
