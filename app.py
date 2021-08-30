
from flask import Flask, render_template, request, redirect, url_for,session,jsonify
from datetime import datetime
from flask_session import Session
from model import *
from sqlalchemy import and_



app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
url="postgresql://wglgundawjelqj:e9d1544596fffeadc069bf27eb34ec4fa810d4d76772664261eac0e37c303c03@ec2-107-20-153-39.compute-1.amazonaws.com:5432/d47b6lteda8844"
app.config["SQLALCHEMY_DATABASE_URI"] = url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def first():
    db.create_all()

with app.app_context():
    first()


@app.route("/")
def home():
    session.pop('username',None)
    return render_template("home.html")




@app.route("/login",methods=["GET", "POST"])
def login():
    if(request.method=="POST"):
        email=request.form.get("email")
        password=request.form.get("password")
        users=User.query.all()
        print(email,password)
        print(users)

        for user in users:
            e=user.email
            pwd=user.password
            u=user.username
            print(e,pwd)
            if(email==e) and(password==pwd):
                session['username']=u
                print(u)
                return render_template("searchbook.html")
            
        error="Invalid username and password"
        return render_template("login.html",error=error)
    else:
        return render_template("login.html")
    # return redirect(url_for('hello'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if(request.method=="POST"):
        uname = request.form.get("uname")
        email = request.form.get("email")
        password = request.form.get("password")
        # hashed_password = generate_password_hash(form.password.data, method='sha256')
        time=datetime.now()
        users=User.query.all()
        
        for user in users:
            u=user.username
            e=user.email
            if(email==e) or (uname==u):
                d="username or email is already Registered"
                # (return render_template("register.html",error=d)  )
                
        # print(uname,email,password)
        row=User(username=uname,email=email,password=password,timestamp=time)
        db.session.add(row)
        db.session.commit()

        return render_template("register.html",uname=uname)
    else:
        error="Invalid Username or password"
        return render_template("register.html",error=error)

@app.route('/admin')
def admin():
    return render_template("admin.html",users=User.query.all())

@app.route("/api/search",methods=["POST"])
def search():
    data=request.json
    s=request.form.get("search")
    s=data["search"]
    print(s)

    usr_isbn=Books.query.filter(Books.isbn.ilike('%'+s+'%')).all()
    usr_title=Books.query.filter(Books.title.ilike('%'+s+'%')).all()
    usr_author=Books.query.filter(Books.author.ilike('%'+s+'%')).all()
    usr_year=Books.query.filter(Books.year.ilike('%'+s+'%')).all()
    print(usr_isbn)

    
    books=usr_isbn+usr_title+usr_author+usr_year
    isbns=[]
    titles=[]
    authors=[]
    years=[]
    for i in books:
        isbns.append(i.isbn)
        titles.append(i.title)
        authors.append(i.author)
        years.append(i.year)
        
    dict={
        "isbns":isbns,
        "titles":titles,
        "authors":authors,
        "years":years
    }

    # return render_template('searchbook.html',books=books)
    return jsonify(dict),200

@app.route('/rr/<isbn>',methods=['GET',"POST"])
def rr(isbn):
    a="rr.html"
    usr_isbn=Books.query.filter(Books.isbn==isbn).first()
    print("Entered into rr")
    if request.method=="POST":
        print("POst request")
        if('reviewsubmit' in request.form):
            print("review submitted")
            review=request.form.get("reviewdata")
            rating=request.form.get("ratingdata")
            name=session['username']
            print(name)
            print(rating)
            print(review)
            data=Review(isbn=isbn,name=name,review=review,rating=rating)
            db.session.add(data)
            db.session.commit()
            r=Review.query.filter(Review.isbn==isbn)
            print(r)
            
            return render_template(a,book=usr_isbn,reviews=r)

        if "rsubmit" in request.form:
            print("Book added to shelf")
            usr_isbn=Books.query.filter(Books.isbn==isbn).first()
            print(usr_isbn.title)
            name=session['username']
            t=usr_isbn.title
            i=usr_isbn.isbn
            a=usr_isbn.author
            y=usr_isbn.year
            print(t)
            s=Shelf(name=name,isbn=i,title=t,author=a,year=y)
            print(s)
            db.session.add(s)
            db.session.commit()
            # return render_template("rr.html")
            r=Review.query.filter(Review.isbn==isbn)
            print(r)
            return render_template(a,book=usr_isbn,reviews=r)
        
        # r=Review.query.filter(Review.isbn==isbn)
        # print(r)
        # return render_template("rr.html",book=usr_isbn,reviews=r)
    else:
        print("Get")
        r=Review.query.filter(Review.isbn==isbn)

        return render_template("rr.html",book=usr_isbn,reviews=r)

@app.route('/bookshelf',methods=["GET","POST"])
def bookshelf():
    
    n=session["username"]

    if 'delete' in  request.form:
        n=request.form.get("name")
        i=request.form.get("isbn")
        t=request.form.get("title")
        a=request.form.get("author")
        y=request.form.get("year")

        print(n)
        Shelf.query.filter(Shelf.isbn== i,Shelf.name==n).delete()
        db.session.commit()

    return render_template("bookshelf.html",users=Shelf.query.filter(Shelf.name==n).all())

# @app.route('/bookdata/<isbn>',methods=['POST'])
# def shelf(isbn):
@app.route("/api/book", methods=["POST"])
def apiBook():
    data = request.json
    isbn = data["isbn"]
    bookObj = Books.query.filter_by(isbn=isbn).first()
    list = Review.query.filter_by(isbn=isbn).all()
    dict = {}
    if len(list) == 0:
        dict["users"] = ["-"]
        dict["ratings"] = [0]
        dict["reviews"] = ["-"]
        return jsonify(dict), 200
    users = []
    ratings = []
    reviews = []
    for i in list:
        users.append(i.name)
        ratings.append(i.rating)
        reviews.append(i.review)
    dict = {
        "users" : users,
        "ratings" : ratings,
        "reviews" : reviews
    }
    return jsonify(dict), 200

    
@app.route("/api/submit_review", methods=["POST"])
def apiSubmitReview():
  data = request.json
  user = data["user"]
  isbn = data["isbn"]
  rating = data["rating"]
  review = data["review"]
  obj = Review.query.filter(and_(Review.isbn == isbn, Review.name == user)).first()
  if obj is not None:
    return jsonify({"Message":"Already reviewed for this book"})
  else:
    reviewObj = Review(isbn=isbn, name=user, rating=rating, review=review)
    db.session.add(reviewObj)
    db.session.flush()
    db.session.commit()
    return jsonify({"Message":"Successfully Reviewed"})
    

