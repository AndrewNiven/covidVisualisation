from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def hey():
    return render_template("hello.html")

@app.route('/graph')
def hi():

    return render_template("image.html", file ="static/images/covid-visualisation.gif")

# def create_figure():
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     xs = range(100)
#     ys = [random.randint(1, 50) for x in xs]
#     axis.plot(xs, ys)
#     return fig

# app.run()