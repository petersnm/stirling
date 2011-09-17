import logging
from methane import App

default = App('default')
foo = App('foo')
default.bind('^/foo/', foo)

@foo.url('')
def foodex(req):
    return "Foo~"

@default.url('^/$')
def index(req):
    return "It works!"

@default.url('^/fbgm/$')
def fbgm(req):
    return "Fuck bitches, get money."

@default.url('^/sup/(?P<name>.+?)$')
def sup(req, name):
    return "Sup %s?" % (name, )
