from flask import render_template
from requests import get


from .. import app

@app.get("/post/<int:post_id>")
def post_info(post_id):
    response = get(f"http://127.0.0.1:8000/post/info/{post_id}")
    if response.status_code == 200:
        post = response.json()
        print("*" * 80)
        print(post)
        return render_template("info.html", post=post, post_id=post_id)
    else:
        return f"Error {response.status_code}"