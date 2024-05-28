from fastapi import FastAPI, HTTPException, Form
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

users_db = {}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Change this to your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root_test():
    return {"message": "Hello World"}

@app.post("/api/v1/signup")
def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    if email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(password)
    users_db[email] = {
        "username": username,
        "email": email,
        "password": hashed_password
    }
    return {"message": "User registered successfully", "user": username, "email": email}

@app.post("/api/v1/login")
def login(email: str = Form(...), password: str = Form(...)):
    user = users_db.get(email)
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    return {"message": "Login successful", "user": user["username"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
