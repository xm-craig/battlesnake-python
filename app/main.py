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
		width 

		return json.dumps({
				'name': 'aspkickers',
				'color': '#00ffff',
				'head_url': 'http://i.imgur.com/jhitWnu.png',
				'taunt': 'There\'s a snake in my boot!'
		})


@bottle.post('/move')
def move():
		data = bottle.request.json

    print data['snakes']
    print data['food']

    oursnake_index = 0

    for index in range(len(data['snakes'])):
      if(data['snakes'][index] == 'aspkickers'):
        oursnake_index = index


    print data['snakes'][oursnake_index]['coords']
    print data['food']

		all_snakes = []
		

		# for snake in snakes
		for snake in data['snakes']:
				for coord in snake['coords']:
						all_snakes.append(coord)

		print all_snakes

		return json.dumps({
				'move': 'right',
				'taunt': 'You\'re my favourite deputy!'
		})

#def isWall(point):


@bottle.post('/end')
def end():
		data = bottle.request.json

		return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
