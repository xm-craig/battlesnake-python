import bottle
import json
import math

width = 0
height = 0
snake_name = 'thisisforjersnake'
life = 100
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
    'name': snake_name,
    'color': '#00DDDDDD',
    'head_url': 'https://raw.githubusercontent.com/jerath/battlesnake-python/master/app/finger.png',
    'taunt': ':>'
  })


@bottle.post('/move')
def move():
  global life

  data = bottle.request.json

  print data['food']
  print data['snakes'] 
  print '=================='

  snake_heads = []
  jer_here = False

  smallest_snake_length = width * height
  # find out about snake head
  for snake in data['snakes']:
    if snake['name'] == snake_name:
      head = snake['coords'][0]
      my_data = snake
      my_length = len(snake['coords'])
    # find jer
    elif snake['name'] == jer_snake:
      jer_data = snake
      jer_length = len(snake['coords'])
      jer_here = True
    # find some other target snake
    elif len(snake['coords']) < smallest_snake_length:
      target_sname_name = snake['name']
      target_snake_data = snake
      target_snake_length = len(snake['coords'])

  
  board = data['board']
  food = data['food']

  safe_squares = find_safe_square(board, head)
  print 'safe_squares', safe_squares

  
  # if hungry, find food.
  if life < 40:
    closest_food = find_closest(food, head)

    taunt_count = 0

    # another snake could be going for the same food
    if not safe_food_square(board, closest_food):
      safe_squares.remove(closest_food)

    best_move = find_closest(safe_squares,closest_food)

  # if jer here and longer than jer, follow jer.
  elif jer_here and my_length > jer_length:
    jers_butt = find_follow_move(jer_data)
    best_move = find_closest(safe_squares, jers_butt)

    if taunt_count < 7:
      taunt_count += 1
    else: 
      taunt_count = 1

  # if jer not here, follow shortest snake if i'm bigger
  elif my_length > target_snake_length:
    print 'i\'m coming for you', target_sname_name
    target_butt = find_follow_move(target_snake_data)
    best_move = find_closest(safe_squares, target_butt)

    if taunt_count < 7:
      taunt_count += 1
    else: 
      taunt_count = 1

  # chase my own tail.
  else:
    closest_food = find_closest(food, head)

    taunt_count = 0

    # another snake could be going for the same food
    if not safe_food_square(board, closest_food):
      safe_squares.remove(closest_food)

    best_move = find_closest(safe_squares,closest_food)


  print 'best_move', best_move

  # Keep track of how hungry the snake is.
  if best_move in food:
    life = 100
  else: 
    life = life - 1

  # convert best move from coordinates into a string
  best_move = convert_coord_to_move(best_move, head)
  print 'best move', best_move


  if taunt_count == 1:
    taunt = 'MY ANACONDA'
  elif taunt_count == 2:
    taunt = 'DON\'T'
  elif taunt_count == 3:
    taunt = 'WANT' 
  elif taunt_count == 4:
    taunt = 'NONE' 
  elif taunt_count == 5:
    taunt = 'UNLESS YOU GOT' 
  elif taunt_count == 6:
    taunt = 'BUNS'
  elif taunt_count == 6:
    taunt = 'HUN'
  else: 
    taunt = 'My anaconda don\'t'

  return json.dumps({
    'move': best_move,
    'taunt': taunt
  })

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
  right = [x+1, y]
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

def safe_food_square(board, food):
  x = food[0]
  y = food[1]

  left = [x-1, y]
  right = [x+1, y]
  up = [x, y-1]
  down = [x, y+1]

  directions = [left, right, up, down]
  
  safe_sq = True

  for direction in directions:
    if direction[0] < (width - 1) and direction[0] >=0:
      if direction[1] < (height - 1) and direction[1] >= 0:
        if board[direction[0]][direction[1]]['state'] is 'head':
          safe_sq = False
  return safe_sq

def find_follow_move(snake):
  # find snake butt
  snake_butt = snake['coords'][len(snake['coords'])-1]
  return snake_butt

def convert_coord_to_move(best_move, head):
  x = head[0]
  y = head[1]

  left = [x-1, y]
  right = [x+1, y]
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
