import bottle
import json
import math

width = 0
height = 0
snake_name = 'thisisforjersnake'
jer_snake = 'Swift Snake'
taunt_count = 0

@bottle.get('/')
def index():
  return """
    <a href="https://github.com/sendwithus/battlesnake-python">
      battlesnake-python
    </a>
    """


@bottle.post('/start')
def start():
  global width, height
  data = bottle.request.json
  width = data['width']
  height = data['height']

  return json.dumps({
    "color": "#FF0000",
    "secondary_color": "#00FF00",
    "head_url": "http://placecage.com/c/100/100",
    "name": "Cage Snake",
    "taunt": "OH GOD NOT THE BEES"
    "head_type": "pixel",
    "tail_type": "pixel"
    }
  )

@bottle.post('/move')
  return json.dumps(
    {
      "move": "up",
      "taunt": "gotta go fast"
    }
  )

@bottle.post('/end')
def end():
  data = bottle.request.json

  return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
