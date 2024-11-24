import graphene

class InstagramPost(graphene.ObjectType):
    success = graphene.Boolean()
    data = graphene.String()
    message = graphene.String()
    translated_caption = graphene.String()
    cleaned_caption = graphene.String()
    keywords = graphene.List(graphene.String)
    masked_caption = graphene.String()
    
    