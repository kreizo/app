from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient(host='mongodb',port=27017, username='root', password='pass',authSource="admin")
db = client.mytododb
tasks_collection = db.tasks

@app.route('/')
def index():
    tasks = tasks_collection.find()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')
    if task_name:
        tasks_collection.insert_one({'name': task_name})
    return redirect(url_for('index'))

@app.route('/delete_task/<task_id>', methods=['GET'])
def delete_task(task_id):
    tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('index'))

@app.route('/delete_task_by_name', methods=['POST'])
def delete_task_by_name():
    task_name = request.form.get('task_name')  # Get task name from the form
    if task_name:
        # Find and delete the task by name
        result = tasks_collection.delete_one({'name': task_name})
        if result.deleted_count > 0:
            print(f"Task '{task_name}' deleted successfully.")
        else:
            print(f"Task '{task_name}' not found.")
    else:
        print("No task name provided.")
    return redirect(url_for('index'))




















if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

