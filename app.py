from flask import Flask , render_template , request , redirect , jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class TODO(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    content = db.Column(db.String(200) , nullable = False)
    # date_created = db.Column(db.DateTime , default = datetime.now(datetime.astimezone.utc))
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}: {self.content}>'





@app.route('/' , methods =['POST' , 'GET'])
def index():
    if request.method == 'POST':
        task = request.form.get('content')
        new_t =  TODO(content = task)
        try :
            db.session.add(new_t)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return jsonify({
                "Error" : "Error while Updating record" , 
                "details" : f"{e}"
            })
    else :
        tasks = TODO.query.order_by(TODO.date_created).all()

        return render_template('index.html' , tasks = tasks)
        

@app.route('/del/<int:id>')
def delete(id):
    task_to_del = TODO.query.get_or_404(id)
    try : 
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect('/')
    except Exception as e :
        return jsonify({
            "Error" : "Issue while deleting...",
            "details" : f"{e}"
        })
    

@app.route('/update/<int:id>' , methods = ['POST' , 'GET'])
def update(id):
    task = TODO.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['utask']
        try : 
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return jsonify({
                "Error" : "Issue while Updating TASK....",
                "details" : f"{e}"
            })
    else :
        return render_template('base.html' , task = task)



if __name__ == '__main__':
    app.run(debug=True)