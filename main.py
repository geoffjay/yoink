import os

import uvicorn

if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = os.getenv("APP_PORT", 8000)
    log_level = os.getenv("LOG_LEVEL", "info")
    uvicorn.run(
        "yoink.app:app",
        host=host,
        port=port,
        workers=5,
        reload=True,
        log_level=log_level,
    )
