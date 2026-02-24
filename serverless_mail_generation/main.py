from fastapi import FastAPI
from serverless_mail_generation.routes import auth, billing, chats, users

app = FastAPI(
    title="My API",
    description="API documentation using Swagger UI",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(billing.router)
app.include_router(chats.router)
app.include_router(users.router)