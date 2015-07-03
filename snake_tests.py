import math


food = [[9, 9], [9, 10], [10, 9], [10, 10]]
head = [4,4]

temp_closest = food[0]
temp_min_dist = pow(20,2)
for f in food:
	a = abs(f[1] - head[1])
	b = abs(f[0] - head[0])
	distance = math.sqrt( pow(a, 2) + pow(b, 2))
	print 'td', temp_min_dist
	print 'd', distance
	if distance < temp_min_dist:
		temp_min_dist = distance
		temp_closest = f
	print '==='
print 'closest', temp_closest
