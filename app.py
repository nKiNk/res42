from flask import Flask, render_template, session, request
app = Flask(__name__)
app.secret_key = 'app secret key'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/print", methods=['GET'])
def print():
    from brother import BrotherPrint
    import socket
    import json
    from datetime import datetime

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('10.19.247.192',9100))
        printjob = BrotherPrint(s)
        printjob.template_mode()
        printjob.template_init()
        printjob.select_and_insert("id", request.args.get('login','F'))
        printjob.select_and_insert("date", datetime.today().strftime("%Y/%m/%d"))
        printjob.select_and_insert("reserved1", request.args.get('9','F'))
        printjob.select_and_insert("reserved2", request.args.get('14','F'))
        printjob.select_and_insert("reserved3", request.args.get('19','F'))
        printjob.template_print()
    return ('printed')
        
if __name__=='__main__':
    app.run(host='0.0.0.0')
