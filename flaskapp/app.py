from flask import Flask, render_template, url_for, Navigation

app = Flask(__name__)
nav = Navigation(app)
nav.Bar('top',[
    nav.Item('Home', 'index'),
    nav.Item('View Dataset', 'viewData' , {'id':1}),
])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/viewData/<int:id>')
def viewData(id):
    return render_template('news.html', id = id)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
