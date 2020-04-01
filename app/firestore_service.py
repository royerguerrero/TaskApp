import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate('app/task-app-272523-firebase-adminsdk-r3qu8-b1339816c6.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def get_users():
    return db.collection('users').get()


def get_user(user_id):
    return db.collection('users').document(user_id).get()


def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()


def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({ 'password': user_data.password })


def put_todo(user_id, description):
    todos_collections_ref = db.collection('users').document(user_id).collection('todos')
    todos_collections_ref.add({'description':description, 'done':False})

def delete_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()

def update_todo(user_id, todo_id, done):
    todo_ref = _get_todo_ref(user_id, todo_id)
    if done == 1:
        todo_ref.update({'done': True})
    else:
        todo_ref.update({'done': False})
        

def _get_todo_ref(user_id, todo_id):
    return db.collection('users').document(user_id).collection('todos').document(todo_id)