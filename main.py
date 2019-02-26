from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blogpost')

@app.route('/blogpost')
def blog():
    blog_id = request.args.get('id')
    if blog_id == None:
        posts = Blog.query.all()
        return render_template('Blogpost.html', posts=posts, title='Build-a-blog')
    else:
        post = Blog.query.get(blog_id)
        return render_template('Blog.html', post=post, title='Blog Entry')


@app.route('/new-post', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_name = request.form['blog-name']
        blog_body = request.form['blog-text']
        new_post = Blog(blog_name, blog_body)
        db.session.add(new_post)
        db.session.commit()
    
        return redirect('/blogpost?id={}'.format(new_post.id))  
    else:
        return render_template('new_post.html', title="build a blog", 
        blog=blog)



if __name__ == '__main__':
    app.run()
