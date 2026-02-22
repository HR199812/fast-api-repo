from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(
    title="My API",
    description="API documentation using Swagger UI",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/secure")
def secure_route(token: str = Depends(oauth2_scheme)):
    return {"token": token}