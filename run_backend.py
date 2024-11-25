from uvicorn import run as start

from server import app


if __name__ == "__main__":
    start("run_backend:app")