#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal=Animal.query.filter(Animal.id==id).first()
    response_body=f'''
    <ul>{animal.name}</ul>
    <ul>{animal.species}</ul>
    <ul>{animal.zookeeper.name}</ul>
    <ul>{animal.enclosure.environment}</ul>
'''
    response=make_response(response_body,200)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper=Zookeeper.query.filter(Zookeeper.id==id).first()
    response_body=f'''
<ul>{zookeeper.name}</ul>
<ul>{zookeeper.birthday}</ul>

'''
    animals=[animal for animal in zookeeper.animals]
    if not animals:
        response_body += f'<h2>Has not been assigned any animals at this time.</h2>'
    else:
        for animal in animals:
             response_body +=f'<h2>Takes care of {animal.name}</h2>'
    response=make_response(response_body,200)
    return response
@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure=Enclosure.query.filter(Enclosure.id==id).first()
    response_body=f'''
<ul>{enclosure.environment}</ul>
<ul>{enclosure.open_to_visitors}
<ul>{enclosure.animals}</ul>
'''
    response=make_response(response_body,200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
