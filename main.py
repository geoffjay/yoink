import os
import pathlib

import uvicorn

cwd = pathlib.Path(__file__).parent.resolve()


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
        access_log=True,
        log_level=log_level,
        log_config=str(pathlib.Path(cwd, "logging.yaml")),
    )
