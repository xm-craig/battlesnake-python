import bottle
import json

width = 0
height = 0

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
		'name': 'aspkickers',
		'color': '#00ffff',
		'head_url': 'http://i.imgur.com/jhitWnu.png',
		'taunt': 'There\'s a snake in my boot!'
	})


@bottle.post('/move')
def move():
	global width, height
	data = bottle.request.json

	print data['snakes']
	print data['food']

	oursnake_index = 0
	oursnake_head = []

	for index in range(len(data['snakes'])):
		if(data['snakes'][index] == 'aspkickers'):
			oursnake_index = index

	oursnake_head = data['snakes'][oursnake_index]['coords'][0]

	print data['snakes'][oursnake_index]['coords']
	print oursnake_head
	print data['food']

	# get the coordinates 
	all_snakes = []
	
	# for snake in snakes
	for snake in data['snakes']:
		for coord in snake['coords']:
			all_snakes.append(coord)

		print all_snakes
	 
	#look at tiles left, right, up down from head
	#for each tile, compare coords in tile to coords in all_snakes
	#if tile coords != all_snakes coords, move there

	x = oursnake_head[0]
	y = oursnake_head[1]
	up = [x, y-1]
	down = [x, y+1]
	left = [x+1, y]
	right = [x-1, y]   
	
	#check if any of the tiles has a snake in it
	if up in all_snakes:
		up = False
	elif down in all_snakes:
		down = False
	elif left in all_snakes:
		left = False
	elif right in all_snakes:
		right = False


	our_square = 'up'

	if up is not False:
		our_square = 'up'
	elif down is not False:
		our_square = 'down'
	elif left is not False:
		our_square = 'left'
	elif right is not False:
		our_square = 'right'






	#look at left tile
	
	print all_snakes
		
	return json.dumps({
		'move': our_square,
		'taunt': 'You\'re my favourite deputy!'
	})

def isWall(index):
	if(index[0] < 0 or index[0] > width) or (index[1] < 0 or index[1] > height):
		return True

	return False

@bottle.post('/end')
def end():
	data = bottle.request.json

	return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
