from fastapi import FastAPI


app = FastAPI(debug = True)


from .routes import (post_router)


app.include_router(post_router)