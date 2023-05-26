"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "whatever123456"

connect_db(app)

@app.route('/')
def show_cupcakes():
    return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    all_cakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cakes)


@app.route('/api/cupcakes/<int:id>')
def get_todo(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_cake():

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]



    new_cake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cake)
    db.session.commit()
    res_json = jsonify(cupcake=new_cake.serialize())
    return (res_json, 201)



@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cake(id):
    cake = Cupcake.query.get_or_404(id)
    cake.flavor = request.json.get('flavor', cake.flavor)
    cake.size = request.json.get('size', cake.size)
    db.session.commit()
    return jsonify(cupcake=cake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cake(id):
    cake = Cupcake.query.get_or_404(id)
    db.session.delete(cake)
    db.session.commit()
    return jsonify(message="deleted")