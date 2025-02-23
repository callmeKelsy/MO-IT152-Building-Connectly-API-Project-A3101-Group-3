import factory
from posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence")
    content = factory.Faker("paragraph")
    post_type = "text"
    metadata = {}

    author = factory.SubFactory("connectly_project.factories.user_factory.UserFactory")

class PostCreator:
    @staticmethod
    def create_post(post_type, title, content='', metadata=None, author=None):
        if metadata is None:
            metadata = {}

        if not author:
            author = User.objects.first() or User.objects.create(username="defaultuser", password="password")

        if post_type not in dict(Post.POST_TYPES):
            raise ValueError("Invalid post type")

        post = Post.objects.create(
            title=title,
            content=content,
            post_type=post_type,
            metadata=metadata,
            author=author
        )
        return post
