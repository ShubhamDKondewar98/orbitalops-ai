
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI


app = FastAPI(title="OrbitalOps AI")

@app.get("/health")
def health_check():
    return {"status": "ok am here  to test at run time  "}

