import os
import uvicorn

__DEV__ = os.getenv("ENV_NAME") == "dev"
port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("app.app:app", port=port, reload=__DEV__)
