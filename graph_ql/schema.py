import graphene
from types import InstagramPost
from services.instagram import fetch_instagram_post
from utils.translation import detect_translate_caption
from utils.data_privacy import mask_personal_data
from services.data_processing import process_caption
from services.aws_s3 import process_latest_post
#tried implementing graphql, but due to issues in version compatibilty, faced a lot of issues in implementing. dropping the idea as we are crunch in time
class Query(graphene.ObjectType):
    fetch_post = graphene.Field(InstagramPost, user_id=graphene.String(required=True))
    
    def resolve_fetched_post(self, info, user_id):
        try:
            posts = fetch_instagram_post(user_id)
            upload_status, message = process_latest_post()
            
            if upload_status:
                translated_caption = detect_translate_caption()
                cleaned_caption, keywords = process_caption(translated_caption)
                mask_caption = mask_personal_data(cleaned_caption)
                
                
                return InstagramPost(
                    success=True,
                    data=str(posts),
                    message = "Fetched data successfully",
                    translated_caption = translated_caption,
                    cleaned_caption = cleaned_caption,
                    keywords=keywords,
                    mask_caption=mask_caption
                    
                )
            else:
                return InstagramPost(
                    success=False,
                    data=str(posts),
                    message=message
                )
        except Exception as e:
            return InstagramPost(success=False,message=str(e))
        
schema = graphene.Schema(query=Query)