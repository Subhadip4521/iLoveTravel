from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from kolkata.models import KolkataPost, KolkataBlogComment
from kolkata.templatetags import kolkataextras


# Create your views here.

def kolkata(request):
    # return HttpResponse('This is kolkata page.')
    allposts= KolkataPost.objects.all()
    context= {'allposts':allposts}
    return render(request, 'kolkata/kolkata.html',context)


def blogpost(request,slug):
    # return HttpResponse(f'This is blogppost page: {slug}')
    post= KolkataPost.objects.filter(slug=slug).first()
    post.views= post.views+1
    post.save()
    
    comments= KolkataBlogComment.objects.filter(post=post, parent=None)
    replies= KolkataBlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)


    context={'post':post, 'comments':comments, 'user':request.user, 'replyDict':replyDict}
    return render(request, 'kolkata/blogpost.html', context)


def postComment(request):
    if request.method=='POST':
        comment= request.POST.get("comment")
        user= request.user
        postSno= request.POST.get("postSno")
        post= KolkataPost.objects.get(sno=postSno)
        parentSno= request.POST.get("parentSno")


        if parentSno=="":
            comment= KolkataBlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, 'Your comment has been posted successfully.')

        else:
            parent= KolkataBlogComment.objects.get(sno=parentSno)
            comment= KolkataBlogComment(comment= comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, 'Your reply has been posted successfully.')

    return redirect(f'/kolkata/{post.slug}')