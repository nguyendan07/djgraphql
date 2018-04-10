import datetime
import graphene
from graphene_django.types import DjangoObjectType
from graphapp.models import Author


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


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
