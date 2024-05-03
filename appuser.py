from flask import Flask
from flask import request
from psycopg2.sql import SQL, Literal
from dotenv import load_dotenv
import os
from appbutton import appbutton
from basa import connection

load_dotenv()

app = Flask(__name__)
app.json.ensure_ascii = False
app.register_blueprint(appbutton)


@app.get("/users")
def get_responce():
    query = """
	select
	  u.id,
	  u.name,
	  u.birthday,
	  coalesce(jsonb_agg(jsonb_build_object(
	    'id', b.id, 'description', b.description, 'title', b.title))
	      filter (where b.id is not null), '[]') as buttons
	from api_data.users u
	left join api_data.useractions ub on u.id = ub.user_id
	left join api_data.buttons b on b.id = ub.button_id
	group by u.id
"""

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    return result


@app.post('/users/create')
def create_user():
    body = request.json

    name = body['name']
    birthday = body['birthday']

    query = SQL("""
insert into api_data.users(name, birthday)
values ({name}, {birthday})
returning id
""").format(name=Literal(name), birthday=Literal(birthday))

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()

    return result


@app.put('/users/update')
def update_user():
    body = request.json

    id = body['id']

    name = body['name']
    birthday = body['birthday']
    query = SQL("""
update api_data.users
set 
  name = {name},
    birthday = {birthday}
where id = {id}
returning id
""").format(name=Literal(name), birthday=Literal(birthday), id=Literal(id))

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    if len(result) == 0:
        return '', 404

    return '', 204


@app.delete('/users/delete')
def delete_user():
    body = request.json

    id = body['id']

    deleteUserLinks = SQL(
        "delete from api_data.useractions where user_id = {id}").format(
            id=Literal(id))
    deleteUser = SQL("delete from api_data.users where id = {id} returning id").format(
        id=Literal(id))

    with connection.cursor() as cursor:
        cursor.execute(deleteUserLinks)
        cursor.execute(deleteUser)
        result = cursor.fetchall()

    if len(result) == 0:
        return '', 404

    return '', 204


if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_PORT'))
