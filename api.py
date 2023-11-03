import openai
import requests  
openai.api_key = "Empty if you don't use embeddings, otherwise your hugginface token"
openai.api_base = "http://127.0.0.1:1337/v1"
import json , csv , pandas as pd

def main():
    text = "text.json"
    # read the text from the file
    with open(text, 'r',encoding='utf-8') as f:
        text = f.read()

    # Include the text in the ChatGPT API request
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Act as a proofreading and verifying CV (Curriculum Vitae) texts. I will provide you with CV-format texts for review. After reviewing, please verify whether the text is indeed a CV. If it's not a CV, kindly ask me to provide a valid CV text. After verification, create a JSON file with well-structured data for easy readability. Let's begin with the provided text: '{text}'",
            },
           ],
        stream=True,
    )



    if isinstance(chat_completion, dict):
        # not stream
        print(chat_completion.choices[0].message.content)
    else:
        # stream
        content_list = []
        for token in chat_completion:
            content = token["choices"][0]["delta"].get("content")
            if content != None:
                content_list.append(content)
                print(content, end="", flush=True)
        print()
        print("".join(content_list))
        

        filename = "output.json"
        # Save the text to the JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("".join(content_list))
    
if __name__ == "__main__":
    main()
