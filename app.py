from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def Is_This_Abuse():
    return render_template('Is_This_Abuse.html')
if __name__ == '__main__':
    app.run(debug=True)
