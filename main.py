import requests
from PIL import Image, ImageDraw, ImageFont
import os

# 1. הגדרות ה-API (נשתמש בסוד ששמרנו קודם)
API_KEY = os.getenv('FOOTBALL_API_KEY')
URL = "https://v3.football.api-sports.io/fixtures?live=all" # דוגמה לתוצאות חיות

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

def create_post():
    # 2. משיכת נתונים מה-API
    # הערה: כאן נצטרך להתאים את המבנה לפי ה-API הספציפי שיש לך
    response = requests.get(URL, headers=headers)
    data = response.json()
    
    # נניח שאנחנו לוקחים את התוצאה הראשונה מהרשימה כדוגמה
    match = data['response'][0]
    home_team = match['teams']['home']['name']
    away_team = match['teams']['away']['name']
    score = f"{match['goals']['home']} - {match['goals']['away']}"
    text_to_print = f"{home_team} {score} {away_team}"

    # 3. עריכת התמונה
    img = Image.open("background.jpg")
    draw = ImageDraw.Draw(img)
    
    # כאן נבחר פונט (נשתמש בברירת מחדל כרגע)
    font = ImageFont.load_default()
    
    # כתיבת הטקסט במרכז התמונה (צריך לשחק עם המיקומים בהתאם לרקע שלך)
    draw.text((100, 100), text_to_print, fill="white", font=font)
    
    # שמירת התמונה המוכנה
    img.save("final_post.jpg")
    print("הפוסט נוצר בהצלחה!")

if __name__ == "__main__":
    create_post()
