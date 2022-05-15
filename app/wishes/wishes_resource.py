from flask import jsonify
from flask_restful import Resource, abort, reqparse
from ..database import db
from .wish import Wish

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('image', required=False, type=str)
parser.add_argument('link', required=False, type=str)
parser.add_argument('description', required=False, type=str)
parser.add_argument('is_private', required=True, type=bool)


def get_wish_or_abort(wishes_id):
    wish = db.session.query(Wish).get(wishes_id)
    if not wish:
        abort(404, message=f"Wish {wishes_id} not found")
    return wish


class WishesResource(Resource):
    def get(self, wishes_id):
        wish = get_wish_or_abort(wishes_id)
        return jsonify({'wishes': wish.to_dict(
            only=('id', 'title', 'user_id', 'image', 'link', 'description'))})

    def delete(self, wishes_id):
        wish = get_wish_or_abort(wishes_id)
        db.session.delete(wish)
        db.session.commit()
        return jsonify({'success': 'OK'})


class WishesListResource(Resource):
    def get(self):
        wishes = db.session.query(Wish).all()
        return jsonify({'wishes': [item.to_dict(
            only=('id', 'title', 'user_id', 'image', 'link', 'description')) for item in wishes]})

    def post(self):
        args = parser.parse_args()
        wishes = Wish(
            title=args['title'],
            user_id=args['user_id'],
            image=args['image'],
            link=args['link'],
            description=args['description'],
            is_private=args['is_private']
        )
        db.session.add(wishes)
        db.session.commit()
        return jsonify({'success': 'OK'})
