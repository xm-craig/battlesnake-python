import bottle
import json


@bottle.get('/')
def index():
    return """
        <a href="https://github.com/sendwithus/battlesnake-python">
            battlesnake-python
        </a>
    """


@bottle.post('/start')
def start():
    data = bottle.request.json

    return json.dumps({
        'name': 'aspkickers',
        'color': '#00ffff',
        'head_url': 'woody.png',
        'taunt': 'There\'s a snake in my boot!'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json
    print data["snakes"][0]["coords"]
    print data["food"]
    
    return json.dumps({
        'move': 'right',
        'taunt': 'battlesnake-python!'
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
