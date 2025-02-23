from rest_framework import serializers
from .models import User, Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)  # ✅ Only return author ID

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'post_type', 'author', 'metadata']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)  # ✅ Auto-assign author ID
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())   # ✅ Auto-assign post ID

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'created_at']

    def create(self, validated_data):
        """ ✅ Auto-assign post from view """
        post = self.context.get('post')  # ✅ Correct context retrieval
        if not post:
            raise serializers.ValidationError({"post": "This field is required."})

        # Create the comment with the post auto-assigned
        return Comment.objects.create(post=post, **validated_data)
