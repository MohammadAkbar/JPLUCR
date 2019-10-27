from flask import Flask, render_template, url_for
from flask_navigation import Navigation
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)

nav = Navigation(app)
nav.Bar('top',[
    nav.Item('Home', 'index'),
    nav.Item('View Dataset', 'viewData'),
    nav.Item('Classify Data', 'classifyData')
])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/viewData')
def viewData(id):
    return render_template('news.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
