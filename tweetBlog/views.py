from django.shortcuts import render, get_object_or_404
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from .models import content
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


@login_required(login_url="/signin/")
def createpost(request):
    return render(request, 'createPost.html')


class blogview(generics.ListCreateAPIView):
    queryset = content.objects.all()
    serializer_class = BlogSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class blogdetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = content.objects.all()
    serializer_class = BlogSerializers
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('You can only edit your own posts.')
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own posts.")
        instance.delete()


def index(request):
    posts = content.objects.all()
    return render(request, 'dashboard.html', {'posts':posts})


@login_required(login_url="/signin/")
def dashboard(request):
    posts = content.objects.all()
    return render(request, 'dashboard.html', {'posts':posts})


def inner_post(request, slug):
    post = get_object_or_404(content, slug=slug)
    return render(request, 'inner_post.html', {'post': post, 'user': request.user})


@login_required(login_url="/signin/")
def update_post(request, slug):
    post = get_object_or_404(content, slug=slug)
    return render(request, 'update_post.html', {'post':post})