from flask import Flask, render_template #追加
from flask import request

app = Flask(__name__)

@app.route('/')
def hello():
    name = "shoki"
    #return name
    return render_template('hello.html', title='flask test', name=name) #変更

@app.route('/post', methods=['POST']) #Methodを明示する必要あり
def hellopost():
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = "no name."
    return render_template('hello.html', title='flask test', name=name) 

## おまじない
if __name__ == "__main__":
    app.run(debug=True)