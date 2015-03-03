import bottle
import json
import math

width = 0
height = 0
snake_name = 'fusnake'

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
    'name': snake_name,
    'color': '#00DDDDDD',
    'head_url': 'https://raw.githubusercontent.com/jerath/battlesnake-python/master/app/finger.png',
    'taunt': ':>'
  })


@bottle.post('/move')
def move():

  data = bottle.request.json

  print data['food']
  print data['snakes'] 
  print '=================='

  # find out about snake
  for snake in data['snakes']:
    if snake['name'] == snake_name:
      head = snake['coords'][0]
      break
 
  board = data['board']
  safe_squares = find_safe_square(board, head)

  print safe_squares
  # if data['turn'] < 40:
    # find closest food
  
  food = data['food']
  closest_food = find_closest(food, head)
  print 'closest_food', closest_food
  # go to closest food
  # ie. find my closest adjacent square and if it's safe, move there.
  best_move = find_closest(safe_squares,closest_food)
  print 'best_move', best_move

  # else: 
  #   move = safe_sq[0]

  best_move = convert_coord_to_move(best_move, head)
  print 'best move', best_move

  return json.dumps({
    'move': best_move,
    'taunt': 'My anaconda don\'t.'
  })

def find_closest_food(food, head):
  temp_closest = food[0]
  temp_min_dist = pow(20,2)
  for f in food:
    a = abs(f[1] - head[1])
    b = abs(f[0] - head[0])
    distance = math.sqrt( pow(a, 2) + pow(b, 2))
    if distance < temp_min_dist:
      temp_min_dist = distance
      temp_closest = f
  return temp_closest

def find_closest(choices, coord):
  temp_closest = choices[0]
  temp_min_dist = pow(width,2)
  for c in choices:
    a = abs(c[1] - coord[1])
    b = abs(c[0] - coord[0])
    distance = math.sqrt( pow(a, 2) + pow(b, 2))
    if distance < temp_min_dist:
      temp_min_dist = distance
      temp_closest = c
  return temp_closest

def find_safe_square(board, head):
  global width, height
  x = head[0]
  y = head[1]


  left = [x-1, y]
  right = [y, x+1]
  up = [x, y-1]
  down = [x, y+1]

  directions = [left, right, up, down]
  
  safe_sq = []

  for direction in directions:
    if direction[0] < (width - 1) and direction[0] >=0:
      if direction[1] < (height - 1) and direction[1] >= 0:
        if board[direction[0]][direction[1]]['snake'] is None:
          safe_sq.append(direction)
  return safe_sq

def convert_coord_to_move(best_move, head):
  x = head[0]
  y = head[1]

  left = [x-1, y]
  right = [y, x+1]
  up = [x, y-1]
  down = [x, y+1]

  if best_move == left:
    return 'left'
  elif best_move == right:
    return 'right'
  elif best_move == up:
    return 'up'
  elif best_move == down:
    return 'down'
  else:
    print 'you fucked up'

@bottle.post('/end')
def end():
  data = bottle.request.json

  return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
