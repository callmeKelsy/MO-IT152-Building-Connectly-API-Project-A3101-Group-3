from rest_framework import serializers
from .models import User, Post, Comment  


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for User model, excluding sensitive fields """
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 


class PostSerializer(serializers.ModelSerializer):
    """ Serializer for Post model, including related comments """
    
    comments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    """ Serializer for Comment model with validation """
    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']

    def validate_post(self, value):
        """ Validate if post exists before allowing comment creation """
        if not Post.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Post not found.")
        return value

    def validate_author(self, value):
        """ Validate if author exists before assigning comment """
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Author not found.")
        return value
