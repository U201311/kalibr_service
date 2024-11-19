from fastapi import FastAPI, File, UploadFile, HTTPException, Form, APIRouter   
from routers import kalibr_service 
from config.config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

origins = [
    "http://localhost:3000",
    # 你可以添加更多的允许源
]

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(kalibr_service.router, prefix="/kalib", tags=["search"])



@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the API"}


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}
    

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level    
    )