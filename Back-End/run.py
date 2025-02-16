import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",  # Allows external access
        port=8000,
        reload=True  # Enable auto-reload during development
    ) 