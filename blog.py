from flask import Flask,render_template,request,url_for,session,redirect
import sqlite3
import re

app=Flask(__name__)
app.secret_key="random string"


@app.route('/login')
def login():
    if 'email' in session:
        return redirect(url_for('update'))
    else:
        return render_template('login.html')


@app.route('/update')
def update():
    if 'email' in session:
        return render_template('update.html')
    return redirect(url_for('login'))

@app.route('/validate',methods=['post'])
def validate():
    email=request.form['nm']
    password=request.form['pass']

    if (email=='asd@gmail.com' and password=='12345'):
        session['email']=email
        return render_template('update.html')
    else:
        return redirect("wrong password")

@app.route('/search',methods=['POST','GET'])
def search():
    res = request.form['searchTxt']
    a = re.compile(str(res),re.IGNORECASE)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM blog")
    search = cur.fetchall()
    rows = []
    for i in search:
        b=a.findall(i[1])
        for j in b:
            rows.append(i)

    return  render_template('home.html',rows=rows)


@app.route('/addrec' , methods=['POST','GET'])
def addrec():
    if request.method=='POST':
        try:
            Title = request.form['title']
            Image = request.form['image']
            URLs = request.form['urls']
            Panda=request.form['Panda']
            Content = request.form['content']

            with sqlite3.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("INSERT INTO blog(Title,Image,URLs,Panda,Content)VALUES (?,?,?,?,?)",(Title,Image,URLs,Panda,Content))

                con.commit()
                msg="Post successfully added"
        except Exception as e:
            con.rollback()
            msg=str(e)
            return str(e)

        finally:
            return render_template('update.html',msg=msg)
            con.close()


@app.route('/')
def home():
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row

    cur=con.cursor()
    cur.execute("select * from blog order by id desc")

    rows=cur.fetchall()
    return render_template('home.html',rows=rows)

@app.route('/tag/<tagname>')
def tag(tagname):
    con=sqlite3.connect("database.db")
    cur=con.cursor()
    cur.execute("SELECT * FROM blog WHERE Panda=?;",(tagname,))
    rows=cur.fetchall()
    return render_template('home.html',rows=rows)
    # return str(tagname)

@app.route('/delete/<int:id>')
def delete(id):
    con=sqlite3.connect("database.db")
    cur=con.cursor()
    cur.execute("DELETE FROM blog WHERE id=?;",(id,))
    con.commit()
    return redirect(url_for("home"))

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect(url_for('home'))

@app.route('/blog/<int:id>')
def blog(id):
    con=sqlite3.connect("database.db")
    cur=con.cursor()
    cur.execute("SELECT * FROM blog WHERE id=?;",(id,))
    rows=cur.fetchone()
    con.commit()
    return render_template('blog.html', rows=rows)


if __name__ =='__main__':
 app.run(debug=True)