from flask import Flask, render_template, session
app = Flask(__name__)
app.secret_key = 'app secret key'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/print")
def print():
    from brother import BrotherPrint
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.1.143',9100))
        printjob = BrotherPrint(s)
        printjob.template_mode()
        printjob.template_init()
        printjob.select_and_insert("id", "dall")
        printjob.select_and_insert("date", "2020/08/30")
        printjob.select_and_insert("reserved1", "O")
        printjob.select_and_insert("reserved2", "O")
        printjob.select_and_insert("reserved3", "O")
        printjob.template_print()
    return ('printed')
        
if __name__=='__main__':
    app.run(host='0.0.0.0')
