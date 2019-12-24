# -*- coding: utf-8 -*-
from flask import Flask
import os
from blog.settings import config
from blog.blueprints.blog import blog_bp
from blog.extensions import db, bootstrap
from blog.models import Category, Post
import click

def create_app(config_name = None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('blog')
    app.config.from_object(config[config_name])

    #执行注册函数
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)


    return app

#注册扩展的函数
def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)

#注册蓝本的函数
def register_blueprints(app):
    app.register_blueprint(blog_bp)

#注册并定义flask命令
def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you."""
        pass

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    def forge(category, post):
        """Generate fake data."""
        from blog.fakes import fake_categories, fake_posts

        db.drop_all()
        db.create_all()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Done.')
