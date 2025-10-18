# 🚀 HNG13 Backend Stage 0 : Dynamic Profile Endpoint (FastAPI)

## 👤 Author
**Name:** Segun Oladimeji  
**Email:** you@example.com  
**Stack:** Python/FastAPI  

---

## 🧾 Overview
This project is my submission for **HNG13 Backend Stage 0**.  
It implements a **FastAPI** endpoint that returns my profile information along with a **dynamic cat fact** fetched from the [Cat Facts API](https://catfact.ninja/fact).

---

## 📍 Endpoint
### `GET /me`

#### ✅ Example Response
```json
{
  "status": "success",
  "user": {
    "email": "you@example.com",
    "name": "Segun Oladimeji",
    "stack": "Python/FastAPI"
  },
  "timestamp": "2025-10-17T12:34:56.789Z",
  "fact": "Cats sleep 70% of their lives."
}
 
```
hng13-backend-stage0

___
⚙️ Setup Instructions
___
1️⃣ Clone & Install
git clone https://github.com/<your-username>/hng13-backend-stage0.git
cd hng13-backend-stage0
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

___ 

2️⃣ Configure Environment

Create a .env file or set Railway variables:
USER_EMAIL=you@example.com
USER_NAME=Segun Oladimeji
USER_STACK=Python/FastAPI
PORT=8000
___

3️⃣ Run Locally
uvicorn main:app --host 0.0.0.0 --port 3000
Visit http://127.0.0.1:3000/me
