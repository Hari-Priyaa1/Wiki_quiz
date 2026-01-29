import os
import requests, json, re, psycopg2
from groq import Groq
from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv  # New import

# This loads the variables from your .env file
load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Using the secret password from .env
DB_PARAMS = {
    "user": "postgres", 
    "password": os.getenv("DB_PASSWORD"), 
    "host": "127.0.0.1", 
    "port": "5432", 
    "database": "wiki_quiz"
}

# Using the secret API key from .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_ID = "llama-3.3-70b-versatile"

class URLRequest(BaseModel):
    url: str

@app.post("/generate-quiz")
async def generate_quiz(req: URLRequest):
    try:
        # 1. Scrape Wikipedia
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0'}
        res = requests.get(req.url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        paragraphs = [p.text for p in soup.find_all('p') if len(p.text) > 80]
        article_text = " ".join(paragraphs[:15])

        if not article_text.strip():
            return {"error": "Could not find enough text on that Wikipedia page."}

        # 2. Call Llama 3
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert educator. Your task is to read the provided text and create a quiz based ONLY on that specific information. You must output a JSON array."
                },
                {
                    "role": "user",
                    "content": (
                        f"ARTICLE CONTENT:\n{article_text}\n\n"
                        "TASK:\nCreate exactly 7 Multiple Choice Questions based ONLY on the Article Content above.\n"
                        "Return ONLY a raw JSON array in this format:\n"
                        "[{\"question\": \"...\", \"options\": {\"A\":\"...\",\"B\":\"...\",\"C\":\"...\",\"D\":\"...\"}, "
                        "\"correct_answer\": \"A\", \"explanation\": \"...\", \"difficulty\": \"Medium\"}]"
                    )
                }
            ],
            model=MODEL_ID,
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        raw_output = chat_completion.choices[0].message.content
        data = json.loads(raw_output)
        
        quiz_data = data if isinstance(data, list) else data.get("questions", data)
        if not isinstance(quiz_data, list):
            quiz_data = [quiz_data]

        # 4. Save to Database
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO wiki_quiz_results (wiki_url, quiz_data) VALUES (%s, %s)", 
                            (req.url, json.dumps(quiz_data)))
                conn.commit()
        
        return quiz_data

    except Exception as e:
        print(f"Backend Error: {e}")
        return {"error": str(e)}

@app.get("/history")
async def get_history():
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, wiki_url, created_at, quiz_data FROM wiki_quiz_results ORDER BY created_at DESC")
            return cur.fetchall()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)