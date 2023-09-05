from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///todo_db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(100),nullable=False)
    desc=db.Column(db.String(200),nullable=False)
    date=db.Column(db.DateTime,default=datetime.now())

    def __repr__(self)->str:
        return f"{self.sno} - {self.task}"

with app.app_context():
    db.create_all()

@app.route("/",methods=["GET","POST"])
def web():
    if request.method=="POST":
        task=request.form["task"]
        desc=request.form["desc"]
        todo=Todo(task=task,desc=desc)
        db.session.add(todo)
        db.session.commit()
    all_todo=Todo.query.all()
    return render_template("index.html",all_todo=all_todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>",methods=["GET","POST"])
def update(sno):
    if request.method=="POST":
        task=request.form["task"]
        desc=request.form["desc"]
        todo=Todo.query.filter_by(sno=sno).first()
        todo.task=task
        todo.desc=desc 
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")



if __name__=="__main__":
    app.run(debug=True)