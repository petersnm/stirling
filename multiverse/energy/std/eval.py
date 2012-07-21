import importlib

def do_eval(entity, *a):
    entity.send(str(eval(' '.join(a))) + '\n')
