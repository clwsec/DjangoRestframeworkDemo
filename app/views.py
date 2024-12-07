from rest_framework import viewsets
from rest_framework.response import Response
from .models import get_post_model

class PostViewSet(viewsets.ViewSet):
    def list(self, request, region=None):
        PostModel = get_post_model(region)
        print(region)
        if not PostModel:
            return Response({'error': 'Invalid region'}, status=400)
        
        posts = PostModel.objects.all().values()
        return Response(list(posts))

    def create(self, request, region=None):
        PostModel = get_post_model(region)
        if not PostModel:
            return Response({'error': 'Invalid region'}, status=400)
        
        title = request.data.get('title')
        content = request.data.get('content')
        post = PostModel.objects.create(title=title, content=content)
        return Response({'id': post.id, 'title': post.title, 'content': post.content})

    def retrieve(self, request, pk=None, region=None):
        PostModel = get_post_model(region)
        if not PostModel:
            return Response({'error': 'Invalid region'}, status=400)
        
        post = PostModel.objects.filter(id=pk).first()
        if not post:
            return Response({'error': 'Post not found'}, status=404)
        
        return Response({'id': post.id, 'title': post.title, 'content': post.content})

    def update(self, request, pk=None, region=None):
        PostModel = get_post_model(region)
        if not PostModel:
            return Response({'error': 'Invalid region'}, status=400)
        
        post = PostModel.objects.filter(id=pk).first()
        if not post:
            return Response({'error': 'Post not found'}, status=404)
        
        post.title = request.data.get('title', post.title)
        post.content = request.data.get('content', post.content)
        post.save()
        return Response({'id': post.id, 'title': post.title, 'content': post.content})

    def destroy(self, request, pk=None, region=None):
        PostModel = get_post_model(region)
        if not PostModel:
            return Response({'error': 'Invalid region'}, status=400)
        
        post = PostModel.objects.filter(id=pk).first()
        if not post:
            return Response({'error': 'Post not found'}, status=404)
        
        post.delete()
        return Response({'success': True})