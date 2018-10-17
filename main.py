# azrael - Jason Tung and <<<NAME>>>
# SoftDev1 pd8
# P00 -- <<<FILL THIS OUT>>>
# <<YEAR-MON-DAY>>

from flask import Flask
app = Flask(__name__)

acct_stack = {}

@app.route('/')
def hello_world():
    return

if __name__ == "__main__":
    app.debug = True
    app.run()
