import sys
import os
import json
from dotenv import load_dotenv
from linkedin_api import Linkedin
from google import genai
from pydantic import BaseModel
from typing import Dict, List

def main():
    try:
        username = sys.argv[1]
    except:
        username = None
    post_text = get_post_text()
    #post_urn = sys.argv[2]

    print("Fetching data...\n")
    post_features = get_post_features(post_text)
    profile_info = get_profile_info(username)
    res = get_result_and_actions(post_text, post_features, profile_info)
    #post_engagement = get_post_engagement(post_text)

    result = res.get("result")
    actions = res.get("actions")

    print("=====================================")
    for key, values in post_features.items():
        print(key)
        if type(values) is str:
            print(values)
            continue
        for val in values:
            print(f"\t{val}")
        print()
 
    print(f"Result: {result}\n")
    print("Actions:")
    for action in actions:
        print(action)

def get_profile_info(username):
    try:
        linkedin_client = Linkedin(user_email, user_password)
        profile = linkedin_client.get_profile(username)
        return profile
    except:
        return None

def get_post_text():
    texts = []
    while True:
        try:
            text = input()
            texts.append(text)
        except EOFError:
            return '\n'.join(texts)

def get_post_features(post_text):
    class PostFeature(BaseModel):
        summary: str
        target_audience: list[str]
        cta: list[str]
        tone_and_style: list[str]
        emotional_appeal: list[str]
        bias: list[str]
        misinformation: list[str]

    prompt = f"""
    Given the linkedin post text inside ```, output a JSON object
    with the following fields and data type:

    TEXT: ```
    {post_text}
    ```
    summary: Overall summary of the post.
    tone_and_style: Overall tone and style of the post.
    target_audience: Target audience of the post.
    cta: All the call to action in the post.
    bias: Is there any bias? If no, put None
    misinformation: Is there any misinformation? If no, put None
    emotional_appeal: Analyze how the post appeals to emotions.
    """

    return get_llm_response(prompt, PostFeature)

def get_result_and_actions(post_text, post_features, profile_info):
    class ActionsList(BaseModel):
        action: list[str]

    class ResultAction(BaseModel):
        result: str
        actions: list[str]

    prompt = f"""
    Given the linkedin post text, post_features and the author of the
    post, determine if the post is postive or negative and give a short summary.
    After that, list actions a reader should take based on CTA in the post_features.

    The actions should be very clear and should give the user step by step
    guide. The actions should give the user examples of things that need to 
    be done, such as the action is to build some project, give example of project
    to build that match the requirements. First, give the description of the action and then explain
    all the steps.

    If there is not CTA, just write there is no call to action.

    POST TEXT: ```
    {post_text}
    ```

    POST_FEATURES: ```
    {post_features}
    ```

    AUTHOR_INFORMATION: ```
    {profile_info}
    ```
    """
    return get_llm_response(prompt, ResultAction)

def get_llm_response(prompt, schema):
    response = gemini_client.models.generate_content(
    model='gemini-2.0-flash',
    contents=prompt,
    config={
        'response_mime_type': 'application/json',
        'response_schema': schema
        },
    )

    return json.loads(response.text)



if __name__ == "__main__":
    load_dotenv()
    user_email = os.environ.get("USER_EMAIL")
    user_password = os.environ.get("USER_PASSWORD")
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    gemini_client = genai.Client(api_key=gemini_api_key)
    main()
