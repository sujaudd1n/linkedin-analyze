import sys
import json
from dotenv import load_dotenv
from linkedin_api import Linkedin

def main():
    setup()

    username = sys.argv[1]
    post_urn = sys.argv[2]
    post_text = get_post_text()

    post_features = get_post_features(post_text)
    post_engagement = get_post_engagement(post_text)

    print(username, post_text)
    #profile_info = get_profile_info(username)

def setup():
    load_dotenv()
    user_email = os.environ.get("USER_EMAIL")
    user_password = os.environ.get("USER_PASSWORD")
    client = Linkedin(user_email, user_password)

def get_profile_info(username):
    profile = client.get_profile(username)

def get_post_text():
    texts = []
    while True:
        try:
            text = input()
            texts.append(text)
        except EOFError:
            return '\n'.join(texts)

def get_post_features(post_text):
    prompt = """
    Given the linkedin post text inside ```, output a JSON object
    with the following fields and data type:

    tone_and_style: Overall tone and style of the post.
    target_audience: Target audience of the post.
    cta: All the call to action in the post.
    bias: Is there any bias? If no, put None
    misinformation: Is there any misinformation? If no, put None
    """

if __name__ == "__main__":
    main()
