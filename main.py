from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import nh3
# now=datetime.datetime.now()


app = Flask(__name__)
app.config['SECRET_KEY'] ='YOUR_SECRET_KEY'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body=CKEditorField('Blog Content', validators=[DataRequired()])
    submit = SubmitField("Submit Post")

@app.route('/')
def get_all_posts():
    posts=db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>", methods=['GET', 'POST'])
def show_post(index):
    posts=BlogPost.query.get(index)        
    return render_template("post.html", post=posts)


@app.route('/new-post', methods=['POST', 'GET'])
def new_post():
    form=CreatePostForm()
    
    if form.validate_on_submit():
        new_post=BlogPost(
        title=form.title.data,
        subtitle=form.subtitle.data,
        author=form.author.data,
        img_url=form.img_url.data,
        body=nh3.clean(form.body.data),
        date=date.today().strftime("%B %d, %Y")
        # date=f"{now.month} {now.day}, {now.year}",    
        )

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts', ))
    return render_template('make-post.html', form=form, head='New Post')

            

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/edit-post/<post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    post=BlogPost.query.get(post_id)
    form=CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        img_url=post.img_url,
        body=post.body
    )

    if form.validate_on_submit():
        post.title=form.title.data
        post.subtitle=form.subtitle.data
        post.author=form.author.data
        post.img_url=form.img_url.data
        post.body=form.body.data
        db.session.commit()
        print('validated')
        return redirect(url_for('show_post',index=post.id, post=form))
    return render_template('make-post.html', form=form, head="Edit Post")

@app.route("/delete/<post_id>", )
def delete_post(post_id):
    post_to_delete=BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts',))
    

if __name__ == "__main__":
    
    # app.run(debug=True)
    
    app.run(host='0.0.0.0', port=5000)