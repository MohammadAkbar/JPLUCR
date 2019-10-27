from flask import Flask, render_template, url_for
from flask_navigation import Navigation
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)

nav = Navigation(app)
nav.Bar('top',[
    nav.Item('Home', 'index'),
    nav.Item('Data Visualization', 'dataVisual'),
    nav.Item('Classify Data', 'dataClassify')
])

@app.route('/')
def index():
    return render_template('index.html' , title='Homepage')

@app.route('/dataVisual')
def viewData():
    return render_template('dataVisual.html' , title='Data Visualization')
    
@app.route('/dataClassify')
def classifyData():
    return render_template('dataClassify.html', title='Data Classify')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
