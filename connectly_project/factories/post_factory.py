import factory
from posts.models import Post
from django.contrib.auth import get_user_model
from connectly_project.factories.user_factory import UserFactory  # ✅ Direct import

User = get_user_model()

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence")
    content = factory.Faker("paragraph")
    post_type = "text"
    metadata = {}

    author = factory.SubFactory(UserFactory)  # ✅ Use direct import

class PostCreator:
    @staticmethod
    def create_post(post_type, title, content='', metadata=None, author=None):
        if metadata is None:
            metadata = {}

        if not author:
            # Ensure a valid author exists
            author = User.objects.filter(is_active=True).first()
            if not author:
                author = User.objects.create_user(
                    username="defaultuser",
                    password="password",
                    email="default@email.com"
                )

        if post_type not in [choice[0] for choice in Post.PostTypes.choices]:  
            raise ValueError("Invalid post type")

        post = Post.objects.create(
            title=title,
            content=content,
            post_type=post_type,
            metadata=metadata,
            author=author
        )
        return post
