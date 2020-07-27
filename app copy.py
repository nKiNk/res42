from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/print")
def print():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.1.143',9100))
        s.send((chr(27)+'i'+'a'+'3').encode())
        s.send(b'^FF')
    return ('printed')
'''
f_socket.send(('^ON'+'Text2'+chr(0)).encode())
f_socket.send(('^DI'+chr(6)+chr(0)+'mkang').encode())

printjob.template_mode()
printjob.template_init()
printjob.choose_template(<template_number>)
printjob.select_and_insert(<field_name>, <data>)
printjob.select_and_insert(<field_name2>, <data2>)
printjob.select_and_insert(<field_name3>, <data3>)
printjob.template_print()
'''


if __name__=='__main__':
    app.run(host='0.0.0.0')
