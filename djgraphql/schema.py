import graphene
import graphapp.schema


class Query(graphapp.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
