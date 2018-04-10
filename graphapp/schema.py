import datetime
import graphene
from graphene_django.types import DjangoObjectType
from graphapp.models import Author


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


class CreateAuthor(graphene.ClientIDMutation):
    author = graphene.Field(AuthorType)
    class Input:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        author = Author(
            first_name=input.get('first_name'),
            last_name=input.get('last_name'),
            email = input.get('email'),
            create_at = datetime.datetime.now(),
        )
        author.save()
        return CreateAuthor(author=author)


class UpdateAuthor(graphene.ClientIDMutation):
    author = graphene.Field(AuthorType)
    class Input:
        id = graphene.Int()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        author = Author.objects.get(pk=input.get('id'))
        if input.get('first_name'):
            author.first_name = input.get('first_name')
        if input.get('last_name'):
            author.last_name = input.get('last_name')
        if input.get('email'):
            author.email = input.get('email')
        author.save()
        return UpdateAuthor(author=author)


class AuthorMutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()


class Query(graphene.ObjectType):
    all_authors = graphene.List(AuthorType)
    author = graphene.Field(AuthorType, id=graphene.Int())

    def resolve_all_authors(self, info, **kwargs):
        return Author.objects.all()
    
    def resolve_author(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Author.objects.get(pk=id)
        return None
