from flask import Flask, redirect, jsonify, request

from Database import Connect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect('/database')


@app.route('/database', methods=['GET', 'POST', 'DELETE'])
def database():
    if request.method == 'GET':
        conn = Connect()
        result = conn.get_dbs(request.args.get('type'), request.args.get('user'))
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': result
        })
    elif request.method == 'POST':
        conn = Connect()
        data = request.get_json(silent=True)
        t = data['type']
        db = conn.id_generator()
        pwd = data['password']
        conn.create(t, db, db, pwd)
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': {
                'opera': 'create',
                'type': t,
                'database': db,
                'username': db,
                'password': pwd
            }
        })
    elif request.method == 'DELETE':
        conn = Connect()
        data = request.get_json(silent=True)
        t = data['type']
        db = data['database']
        conn.drop(t, db)
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': {
                'opera': 'drop',
                'type': t,
                'database': db
            }
        })


if __name__ == '__main__':
    app.run()
