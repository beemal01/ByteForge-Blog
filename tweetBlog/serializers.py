from rest_framework import serializers
from .models import content

class BlogSerializers(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    featured_image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = content
        fields = ['author', 'title', 'blog_body', 'featured_image']

