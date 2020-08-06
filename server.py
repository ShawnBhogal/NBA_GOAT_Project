from flask import Flask 
from flask import render_template
from prompts import user_prompt

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', len=len(user_prompt), value=user_prompt)

if __name__ == '__main__':
    app.run(debug=True)