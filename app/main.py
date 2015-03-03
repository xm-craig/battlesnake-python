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
  global life, taunt_count

  data = bottle.request.json

  print data['food']
  print data['snakes'] 
  print '=================='

  snake_heads = []
  jer_here = False

  smallest_snake_length = width * height

  # get data for my snake, jer's snake, target snake
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
      target_snake_name = snake['name']
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
    if not adjacent_square_safe(board, closest_food, 'head'):
      safe_squares.remove(closest_food)

    best_move = find_closest(safe_squares,closest_food)

  # if jer not here, follow shortest snake if i'm bigger
  else:
    print 'i\'m coming for you', target_snake_name
    snake_butt, snake_head = find_snake_parts(target_snake_data)

    if square_adjacent(head, snake_butt):  
      # if snake is not about to eat, their butt is a safe place to be
      if adjacent_square_safe(board = board, point = snake_head, state = 'food'):
        safe_squares.append(snake_butt)
    
    best_move = find_closest(safe_squares, snake_butt)

    if taunt_count < 8:
      taunt_count += 1
    else: 
      taunt_count = 1


  print 'best_move', best_move

  # Keep track of how hungry the snake is.
  if best_move in food:
    life = 100
  else: 
    life = life - 1

  # convert best move from coordinates into a string
  best_move = convert_coord_to_move(best_move, head)
  print 'best move', best_move

  taunt = taunt_gen()


  return json.dumps({
    'move': best_move,
    'taunt': taunt
  })


def square_adjacent(head, snake_butt):
  adj = False

  x = head[0]
  y = head[1]

  left = [x-1, y]
  right = [x+1, y]
  up = [x, y-1]
  down = [x, y+1]
  
  if snake_butt == left or snake_butt == right or snake_butt == up or snake_butt == down:
    adj = True

  return adj

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

def adjacent_square_safe(board, point, state):
  x = point[0]
  y = point[1]

  left = [x-1, y]
  right = [x+1, y]
  up = [x, y-1]
  down = [x, y+1]

  directions = [left, right, up, down]
  
  safe_sq = True

  for direction in directions:
    if direction[0] < (width - 1) and direction[0] >=0:
      if direction[1] < (height - 1) and direction[1] >= 0:
        if board[direction[0]][direction[1]]['state'] is state:
          safe_sq = False
  return safe_sq

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

def find_snake_parts(snake):
  snake_butt = snake['coords'][len(snake['coords'])-1]
  snake_head = snake['coords'][0]
  return snake_butt, snake_head


def taunt_gen():
  if taunt_count == 1:
    return 'MY ANACONDA'
  elif taunt_count == 2:
    return 'DON\'T'
  elif taunt_count == 3:
    return 'WANT' 
  elif taunt_count == 4:
    return 'NONE' 
  elif taunt_count == 5:
    return 'UNLESS YOU' 
  elif taunt_count == 6:
    return 'GOT'
  elif taunt_count == 7:
    return 'BUNS'
  elif taunt_count == 8:
    return 'HUN'
  else: 
    return 'My anaconda don\'t'

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
