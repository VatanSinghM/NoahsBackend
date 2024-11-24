from flask import Flask,jsonify
# from flask_graphql import GraphQLView
# from graph_ql.schema import schema
from services.aws_s3 import process_latest_post
from services.instagram import fetch_instagram_comments,fetch_instagram_dms,fetch_instagram_post
from utils.translation import detect_translate_caption
from services.data_processing import process_caption
from utils.data_privacy import mask_personal_data

from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# app.add_url_rule(
#     "/graphql",
#     view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
# )

@app.route("/fetch-posts/<user_id>", methods=["GET"])
def fetch_post_route(user_id):
    print("Received request for fetch-posts with user_id:", user_id)
    try:
        posts = fetch_instagram_post(user_id)
        upload_status, message = process_latest_post()

        if upload_status:
            translated_caption = detect_translate_caption()
            cleaned_caption, keywords = process_caption(translated_caption)
            masked_caption = mask_personal_data(cleaned_caption)
            return jsonify({
                "success": True, 
                "data": posts, 
                "message": "Uploaded to S3 successfully",
                "translated_caption": translated_caption,
                "cleaned_caption": cleaned_caption,
                "keywords": keywords,
                "masked_caption": masked_caption,
            }), 200
        else:
            return jsonify({"success": False, "data": posts, "error": message}), 500

    except Exception as e:
        return jsonify({"success":False,"error": str(e)}),500
    
    
@app.route("/access-langchain", methods=["GET"])
def generate_text_langchain():
    try:
        print("Received request for LLM")
        from utils.large_language_model import forming_caption, generate_seo_caption
        
        final_caption = forming_caption()
        if final_caption:
            optimized_caption = generate_seo_caption(final_caption)
            if optimized_caption:
                return jsonify({
                    "success": True, 
                    "optimized_caption": optimized_caption
                }), 200
            else:
                return jsonify({"success": False, "error": "Error in generating SEO optimized caption"}), 500
        else:
            return jsonify({"success": False, "error": "Error in forming caption"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": f"Error in generating Langchain response {e}"}), 500


@app.route("/fetch-dms/<user_id>", methods=["GET"])
def fetch_dms_route(user_id):
    try:
        dms = fetch_instagram_dms(user_id)
        return jsonify({"success":True,"data":dms}),200
    except Exception as e:
        return jsonify({"success":False,"error":str(e)}),500
    

@app.route("/fetch-comments/<user_id>",methods=["GET"])
def fetch_comment_route(user_id):
    try:
        comments = fetch_instagram_comments(user_id)
        return jsonify({"success":True,"data":comments}),200
    except Exception as e:
        return jsonify({"success":False,"error":str(e)}),500
    
    

# testing 
# @app.route("/translate-latest-caption", methods=["GET"])
# def translate_latest_caption_route():
#     try:
#         translated_caption = detect_translate_caption()
#         if translated_caption:
#             return jsonify({"success": True, "translated_caption": translated_caption}), 200
#         else:
#             return jsonify({"success": False, "error": "No caption or translation failed"}), 500
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

    
    
if __name__ == "__main__":
    app.run(debug=True)