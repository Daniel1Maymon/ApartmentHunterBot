import os
import tiktoken
from openai import OpenAI
import json

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def extract_info(post_text):
    messages = [    
    {
        "role": "user",
        "content": """
            You are a smart real estate agent. Return answers in JSON format. If the post offers an apartment for rent, return the following information:

            rooms (number of rooms, can be a float)
            size (area in square meters, integer)
            price (price in NIS, integer)
            city (city name in Hebrew)
            address (street name in Hebrew; if missing, return null)
            phone (phone number; if missing, return null)
            If the post does not offer an apartment for rent, return false.
            If the city is not mentioned, guess it based on the area.
            
            if post is about anything except offer for an apartment for rent, return {"result": "False"}
        """
    },
    {
        "role": "user",
        "content": f'Post: {post_text}'
    }
]
    
    # Get the encoding 
    enc = tiktoken.encoding_for_model("gpt-4")    
    tokens = enc.encode(json.dumps(messages))
    token_count = len(tokens)

    print(f"\nNumber of tokens: {token_count}\n")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=messages,
        max_tokens=150
    )
    
    result = response.choices[0].message.content
    
    tokens = enc.encode(json.dumps(result))
    total_token =  token_count + len(tokens)

    print(f"\nNumber of TOTAL tokens: {total_token}\n")
    return result

# דוגמה לפוסט נדל"ן
post_text1 = """ 
        היי לכולם
        אני ובן הזוג שלי מחפשים דירה/יחידת דיור
        עד 4200 ש״ח, כניסה בסביבות דצמבר
        עדיפות למרוהטת 
        תודה מראש
"""

post_text2 = """
להשכרה דירת 3 חדרים בשכונת תל גנים המבוקשת בגבעתיים 
 דירה מרווחת, מוארת ונעימה בגודל של כ- 70 מ"ר, עם פרקט ומזגנים בחדרים.
 בקרבת גנים, בתי"ס ומרכזי קניות, עם יציאות מעולות לת"א. 
 כניסה מיידית!
 שכ"ד: 5,200 ש"ח לחודש.
 לפרטים ותיאום ביקור:
 נאוה - 052-3901736 
"""

post_text3 = """
מחפשים דירה משוכרת 7000₪? 
 מחיר לדירה חדשה 2.790.000 ש"ח
 למכירה בבלעדיות בשכונת נגבה דירת 4 חדרים קומה 1 עורפית 84 מטר 
 מרפסת שמש 10 מטר אחרי פינוי בינוי! 
 שוכרים שרוצים להישאר! 
 לפרטים נוספים שלומי מאנה 
 053-439-4187
 המתווך החזק
"""

post_text4 = """
    אתה הראש אתה השם 
    תזכורת קטנה 
    לכל מי ששכח לרגע שיש מנהיג לעולם 
"""

if __name__ == "__main__":
    examples = []
    examples.append(post_text1)
    examples.append(post_text2)
    examples.append(post_text3)
    examples.append(post_text4)


    for i in range(len(examples)):
        print("-----")
        print(f"Example: {examples[i]}\n")
        extracted_info = extract_info(examples[i])
        print(f"extracted_info = \n{extracted_info}")

    extracted_info_in_json = json.loads(extracted_info)
# print(extracted_info_in_json)