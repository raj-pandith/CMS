"""
Routes and views for the flask application.
"""
import logging
import uuid

import msal
from flask import render_template, flash, redirect, request, session, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from FlaskWebProject import app
from FlaskWebProject.forms import LoginForm, PostForm
from FlaskWebProject.models import User, Post
from config import Config

LOGIN_SUCCEEDED_ = "login succeeded "

TOKEN_CACHE = "token_cache"

imageSourceUrl = 'https://' + app.config['BLOB_ACCOUNT'] \
                 + '.blob.core.windows.net/' \
                 + app.config['BLOB_CONTAINER'] + '/'


@app.route('/')
@app.route('/home')
@login_required
def home():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.all()
    app.logger.log(logging.INFO, "Entered home")
    return render_template(
        'index.html',
        title='Home Page',
        posts=posts
    )


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm(request.form)
    if form.validate_on_submit():
        post = Post()
        post.save_changes(form, request.files['image_path'], current_user.id, new=True)
        return redirect(url_for('home'))

    app.logger.log(logging.INFO, "New Post")

    return render_template(
        'post.html',
        title='Create Post',
        imageSource=imageSourceUrl,
        form=form
    )


@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get(int(id))
    form = PostForm(formdata=request.form, obj=post)
    if form.validate_on_submit():
        post.save_changes(form, request.files['image_path'], current_user.id)
        return redirect(url_for('home'))

    app.logger.log(logging.INFO, "Entered post id:" + str(id))

    return render_template(
        'post.html',
        title='Edit Post',
        imageSource=imageSourceUrl,
        form=form
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.warning("Login attempt")
    if current_user.is_authenticated:
        app.logger.warning("User is authenticated")
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        app.logger.warning(LOGIN_SUCCEEDED_ + user.username)
        if user is None or not user.check_password(form.password.data):
            app.logger.error("Invalid password")
            flash('Invalid username or password')
            return redirect(url_for('login'))
        app.logger.warning(LOGIN_SUCCEEDED_ + user.username)
        login_user(user, remember=form.remember_me.data)
        app.logger.warning(LOGIN_SUCCEEDED_ + user.username)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        app.logger.warning(LOGIN_SUCCEEDED_ + user.username)
        return redirect(next_page)
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(scopes=Config.SCOPE, state=session["state"])
    app.logger.warning(LOGIN_SUCCEEDED_)
    return render_template('login.html', title='Sign In', form=form, auth_url=auth_url)


@app.route(Config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    app.logger.info(LOGIN_SUCCEEDED_)
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("home"))  # No-OP. Goes back to Index page
    if "error" in request.args:  # Authentication/Authorization failure
        return render_template("auth_error.html", result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        # DONE: Acquire a token from a built msal app, along with the appropriate redirect URI
        result = _build_msal_app(cache, ).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=Config.SCOPE,
            redirect_uri=url_for('authorized', _external=True, _scheme='https')
        )
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        # Note: In a real app, we'd use the 'name' property from session["user"] below
        # Here, we'll use the admin username for anyone who is authenticated by MS
        user = User.query.filter_by(username="admin").first()
        login_user(user)
        _save_cache(cache)
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    logout_user()
    if session.get("user"):  # Used MS Login
        # Wipe out user and its token cache from session
        session.clear()
        # Also logout from your tenant's web session
        return redirect(
            Config.AUTHORITY + "/oauth2/v2.0/logout" +
            "?post_logout_redirect_uri=" + url_for("login", _external=True))
    app.logger.info("logout succeeded")
    return redirect(url_for('login'))


def _load_cache():
    # Done: Load the cache from `msal`, if it exists
    cache = msal.SerializableTokenCache()
    if session.get(TOKEN_CACHE):
        cache.deserialize(session[TOKEN_CACHE])
    return cache


def _save_cache(cache):
    # Done: Save the cache, if it has changed
    if cache.has_state_changed:
        session[TOKEN_CACHE] = cache.serialize()


def _build_msal_app(cache=None, authority=None):
    # Done: Return a ConfidentialClientApplication
    return msal.ConfidentialClientApplication(Config.CLIENT_ID,
                                              authority=authority or Config.AUTHORITY,
                                              client_credential=Config.CLIENT_SECRET,
                                              token_cache=cache)


def _build_auth_url(authority=None, scopes=None, state=None):
    # DONE: Return the full Auth Request URL with appropriate Redirect URI
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for('authorized', _external=True, _scheme='https')
    )
