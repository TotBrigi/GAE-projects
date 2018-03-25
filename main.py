#!/usr/bin/env python
import os
import jinja2
import webapp2
import random

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("lottery.html")

class ResultHandler(BaseHandler):
    def get(self):
        numbers = generate_lottery_numbers(8)
        return self.render_template("secondpage.html", params={"numbers": numbers})

def generate_lottery_numbers(quantity):
    lottery = []

    while True:
        if len(lottery) == quantity:
           break
        lottery_numbers = random.randint(1, 100)

        if lottery_numbers not in lottery:
            lottery.append(lottery_numbers)

    return lottery

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/lottery', ResultHandler),
], debug=True)