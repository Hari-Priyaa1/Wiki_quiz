# 🧠 WikiQuiz Pro: AI-Powered Learning

WikiQuiz Pro is a full-stack web application that transforms any Wikipedia URL into an interactive 7-question quiz using Large Language Models.

By integrating **FastAPI** for a robust backend and **Tailwind CSS** for a modern, responsive frontend, the platform provides a seamless user experience for active learning.
The core engine utilizes **BeautifulSoup4** to scrape and clean web data, which is then processed by the **Llama-3.3-70B model** via the **Groq Cloud API** to generate contextually accurate,
multiple-choice questions. To ensure data persistence and progress tracking, the system leverages a **PostgreSQL database**, managing all quiz history and user results through an asynchronous architecture.

## 🚀 Key Features
* **Instant Quiz Generation:** Enter any Wikipedia link to generate questions automatically.
* **Intelligent Scoring:** Real-time feedback on your answers.
* **History Tracking:** Saves your quiz results in a database for later review.
* **Clean UI:** Responsive design built with Tailwind CSS.

## 🛠️ Technologies Used
* **Frontend:** HTML5, Tailwind CSS, JavaScript (Fetch API).
* **Backend:** FastAPI (Python).
* **AI Engine:** Groq Cloud API (Llama 3.3 70B Model).
* **Database:** PostgreSQL.
* **Web Scraping:** BeautifulSoup4 & Requests.

## ⚙️ Setup & Installation
1. **Clone the Repo:** `git clone https://github.com/Hari-Priyaa1/Wiki_quiz.git`
2. **Environment Variables:** Create a `.env` file with your `GROQ_API_KEY` and `DB_PASSWORD`.
3. **Install Dependencies:** ```bash
   pip install fastapi uvicorn requests beautifulsoup4 psycopg2-binary python-dotenv groq


## 📸 App Preview

![Main Interface](Screenshot%202026-01-30%20003106.png)

![Quiz Results](Screenshot%202026-01-29%20232812.png)
![](Screenshot%202026-01-30%20001451.png)
![](Screenshot%202026-01-30%20001506.png)
![](Screenshot%202026-01-30%20001516.png)

![History](Screenshot%202026-01-30%20093444.png)
