# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import os
import jinja2

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

template_path = os.path.join(PROJECT_ROOT, 'templates')

import threading
from tornado import template, web
import jinja2

class TTemplate(object):
    def __init__(self, template_instance):
        self.template_instance = template_instance

    def generate(self, **kwargs):
        return self.template_instance.render(**kwargs)

class JinjaLoader(template.BaseLoader):
    def __init__(self, root_directory, **kwargs):
        self.jinja_env = \
        jinja2.Environment(loader=jinja2.FileSystemLoader(root_directory), **kwargs)
        self.templates = {}
        self.lock = threading.RLock()

    def resolve_path(self, name, parent_path=None):
        return name

    def _create_template(self, name):
        template_instance = TTemplate(self.jinja_env.get_template(name))
        return template_instance

class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

from sqlalchemy import desc 

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        from db.models import User
        user_list = User.query.order_by(desc(User.follower)).limit(1000).all()
        self.render('index.html', a=100, user_list=user_list)



Handlers=[
    (r"/", MainHandler),
]
jinja2_loader = JinjaLoader(template_path)
settings = dict(template_loader=jinja2_loader)

application = Application(Handlers, **settings)
if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
