from flask import Blueprint, render_template, abort
from basa import connection
from flask import request
from psycopg2.sql import SQL, Literal

appbutton = Blueprint('appbutton', __name__)


@appbutton.get("/buttons")
def get_responce():
    query = """
	select 
    b.id,
    b.description,
    b.title,
    b.parent_id,
    coalesce(jsonb_agg(jsonb_build_object(
        'id', u.id, 'name', u.name, 'birthday', u.birthday))
            filter (where u.id is not null), '[]') as users
    from api_data.buttons b
    left join api_data.useractions ub on b.id = ub.button_id
	left join api_data.users u on u.id = ub.user_id
	group by b.id
"""

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    return result


@appbutton.post("/buttons/create")
def create_button():
    body = request.json
    description = body['description']
    title = body['title']
    query = SQL("""
insert into api_data.buttons(description, title)
values ({description}, {title})
returning id
""").format(description=Literal(description), title=Literal(title))
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()

    return result


@appbutton.put('/buttons/update')
def update_button():
    body = request.json

    id = body['id']

    description = body['description']
    title = body['title']
    query = SQL("""
update api_data.buttons
set 
  description = {description},
    title = {title}
where id = {id}
returning id
""").format(description=Literal(description), title=Literal(title), id=Literal(id))

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    if len(result) == 0:
        return '', 404

    return '', 204


@appbutton.delete('/buttons/delete')
def delete_button():
    body = request.json

    id = body['id']

    deleteButtonLinks = SQL(
        "delete from api_data.useractions where button_id = {id}").format(
            id=Literal(id))
    deleteButton = SQL("delete from api_data.buttons where id = {id} returning id").format(
        id=Literal(id))

    with connection.cursor() as cursor:
        cursor.execute(deleteButtonLinks)
        cursor.execute(deleteButton)
        result = cursor.fetchall()

    if len(result) == 0:
        return '', 404

    return '', 204
