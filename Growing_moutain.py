from tkinter import *
import pdb


col_hod = 10
list_point_polygon = []
status_capturer = False
list_point_capturer = []
last_x = 0
last_y = 0
col_bal = 0
players = []

# for i in players:
# 		if i.status == True:
# 			color = i.color
# 			i.status = False
# 			if players.index(i) == len(players):
# 				i = players[0]
# 				i.status = True
# 			else:
# 				index = players.index(i)+1
# 				players[index].status = True


def instaler_begin_setings():
	global list_point_capturer, corect_x, corect_y, last_x, last_y, status_capturer, list_point_polygon, col_hod, players, color, player

	col_hod = 10
	list_point_polygon = []
	status_capturer = False
	last_x = 0
	last_y = 0
	corect_x = None
	corect_y = None

	player = players[0]
	color = player.color

	players.append(players.pop(0))


class Start_window():
	def __init__(self, title):
		self.title = title


	def init_start_window(self):
		self.window = Tk()
		self.window.title(self.title)

		self.new_game = Button(text='New game')
		self.online_game = Button(text='Online game')
		self.settings = Button(text='Settings')
		self.exit = Button(text='Exit')

		self.new_game.bind('<Button-1>', Event.start_game)

		self.new_game.pack()
		self.online_game.pack()
		self.settings.pack()
		self.exit.pack()

		self.window.mainloop()


class Event():
	
	def start_game(event):
		global root

		root.window.destroy()
		root = Game_field('Growing mountain', 600, 600)
		root.init_game_field()


class Game_field():
	def __init__(self, title, w_canvas, h_canvas):
		self.title = title
		self.w_canvas = w_canvas
		self.h_canvas = h_canvas


	def init_game_field(self):
		global players, Player_1, Player_2
		self.window = Tk()
		self.window.title(self.title)
		self.c = Canvas(self.window, width=self.w_canvas, height=self.h_canvas, bg='white')
		
		players.append(Player('Player_1', 'green', True))
		players.append(Player('Player_2', 'orange', False))

		Player_1 = players[0]
		Player_2 = players[1]
		
		self.name_player_1 = Label(text='Player_1')
		self.bals_player_1 = Label(text=str(Player_1.bals))
		self.name_player_2 = Label(text='Player_2')
		self.bals_player_2 = Label(text=str(Player_2.bals))

		root.init_canvas()

		instaler_begin_setings()
		self.c.bind('<Motion>', move)
		self.c.bind('<Button-1>', capturer)

		self.name_player_1.pack()
		self.bals_player_1.pack()
		self.name_player_2.pack()
		self.bals_player_2.pack()
		self.c.pack()
		
		self.window.mainloop()

	def init_canvas(self):
		for i in range(int(self.w_canvas/20)):
			x_line = 20 * i
			self.c.create_line(x_line, 0, x_line, self.h_canvas)

		for i in range(int(self.h_canvas/20)):
			y_line = 20 * i
			self.c.create_line(0, y_line, self.w_canvas, y_line)

		for i in range(int(self.w_canvas/20)):
			x_line = 20 * i
			for i in range(int(self.h_canvas/20)):
				y_line = 20 * i
				self.c.create_oval((x_line - 2, y_line - 2), (x_line + 2, y_line + 2), fill='black')

		list_points_center = []

		for i in range(0, self.w_canvas+1, 20):
			list_points_center.append([i, self.h_canvas-20])

		for i in range(self.w_canvas, -1, -20):
			list_points_center.append([i, self.h_canvas])

		center = self.c.create_polygon(list_points_center, fill='blue', outline='black')

		list_point_capturer = append_point_in_list_point_capturer(self.c.coords(center))


class Player():
	def __init__(self, name, color, status):
		self.name = name
		self.color = color
		self.status = status
		self.bals = 0
		

def append_point_in_list_point_capturer(list_point):
	'''Добавляет центр в список точек привязки'''
	global list_point_capturer, corect_x, corect_y, last_x, last_y, status_capturer, list_point_polygon, col_hod

	for i in range(0, len(list_point)-1, 2):
		if list_point_capturer.count([list_point[i], list_point[i+1]]) == False:
			list_point_capturer.append([list_point[i], list_point[i+1]])
	return list_point_capturer


def create_game_field(root, w, h, list_point_capturer = []):
	'''Создаёт игравое поле'''
	global c

	c = Canvas(root, width=w, height=h, bg='white')
	
	for i in range(int(w/20)):
		x_line = 20 * i
		c.create_line(x_line, 0, x_line, h)

	for i in range(int(h/20)):
		y_line = 20 * i
		c.create_line(0, y_line, w, y_line)

	for i in range(int(w/20)):
		x_line = 20 * i
		for i in range(int(h/20)):
			y_line = 20 * i
			c.create_oval((x_line - 2, y_line - 2), (x_line + 2, y_line + 2), fill='black')

	list_points_center = []

	for i in range(0, w+1, 20):
		list_points_center.append([i, h-20])

	for i in range(w, -1, -20):
		list_points_center.append([i, h])

	center = c.create_polygon(list_points_center, fill='blue', outline='black')

	list_point_capturer = append_point_in_list_point_capturer(c.coords(center))

	c.pack()


def opr_nap():
	global list_point_capturer, corect_x, corect_y, last_x, last_y, status_capturer, list_point_polygon, col_hod

	x1 = list_point_polygon[0]
	x2 = list_point_polygon[-1]

	if list_point_capturer.index(x1) < list_point_capturer.index(x2):
		return 'left'
	elif list_point_capturer.index(x1) > list_point_capturer.index(x2):
		return 'right'
	else:
		return 'error'


def get_col_bal(list_point_new_polygon):
	global col_bal

	list_x_cordinat = []
	list_y_cordinat = []

	for i in list_point_new_polygon:
		list_x_cordinat.append(i[0])
		list_y_cordinat.append(i[1])

	x_min = min(list_x_cordinat)
	y_min = min(list_y_cordinat)
	x_max = max(list_x_cordinat)
	y_max = max(list_y_cordinat) 

	point = []
	col_point_in_polygon = 0
	status = False

	point = [x_min, y_min]
	while point != [x_max+20, y_min]:
		step = 0
		while True:
			x = point[0]
			y = point[1] + 20*step  

			if [x, y] in list_point_new_polygon:
				if status == False:
					status = True
					col_point_in_polygon -= 1
				else:
					status = False

			if status == True:
				col_point_in_polygon +=1

			step += 1

			if y == y_max:
				point[0] += 20
				break

	player.bals += int(col_point_in_polygon + (len(list_point_new_polygon)/2) - 1)
	update_bals_players()


def update_bals_players():
	global Player_1, Player_2
	root.bals_player_1['text'] = str(Player_1.bals)
	root.bals_player_2['text'] = str(Player_2.bals)


def create_new_polygon():
	global list_point_polygon, list_point_capturer

	# pdb.set_trace()
	list_point_new_polygon = []
	for i in range(0, len(list_point_polygon)-1):
		x1 = list_point_polygon[i][0]
		y1 = list_point_polygon[i][1]
		x2 = list_point_polygon[i+1][0]
		y2 = list_point_polygon[i+1][1]

		# NW
		if x1 > x2 and y1 > y2:
			if [x1, y1] in list_point_new_polygon:
				list_point_new_polygon.append([x1, y2])
			else:
				list_point_new_polygon.append([x1, y1])
				list_point_new_polygon.append([x1, y2])

		# NE
		elif x1 < x2 and y1 > y2:
			if [x2, y1] in list_point_new_polygon:
				if [x1, y1] in list_point_new_polygon:
					list_point_new_polygon.remove([x1, y1])
				list_point_new_polygon.append([x2, y2])
			else:
				list_point_new_polygon.append([x2, y1])
				list_point_new_polygon.append([x2, y2])

		# SW
		elif x1 > x2 and y1 < y2:
			if [x2, y1] in list_point_new_polygon:
				if [x1, y1] in list_point_new_polygon:
					list_point_new_polygon.remove([x1, y1])
				list_point_new_polygon.append([x2, y2])
			else:
				list_point_new_polygon.append([x1, y1])
				list_point_new_polygon.append([x2, y1])
				list_point_new_polygon.append([x2, y2])

		# SE
		elif x1 < x2 and y1 < y2:
			if [x1, y1] in list_point_new_polygon:
				if [x1, y2] in list_point_new_polygon:
					list_point_new_polygon.remove([x1, y1])
				list_point_new_polygon.append([x1, y2])
			else:
				list_point_new_polygon.append([x1, y1])
				list_point_new_polygon.append([x1, y2])	
		else:
			if [x2, y2] in list_point_new_polygon:
				pass
			else:
				list_point_new_polygon.append([x1, y1])
				list_point_new_polygon.append([x2, y2])
			
	try:
		if list_point_polygon[0][0] != list_point_polygon[-1][0] and list_point_polygon[0][1] != list_point_polygon[-1][1]:
			list_point_new_polygon.remove(list_point_polygon[0])
	except Exception as e:
		pass

	newlist = []
	for i in list_point_new_polygon:
		if i not in newlist:
			newlist.append(i)

	list_point_new_polygon = newlist
	# c.create_polygon(list_point_new_polygon, width=2, outline='red')

	get_col_bal(list_point_new_polygon)


def add_points_in_capturer():
	global list_point_capturer, list_delete, list_point_polygon

	index = list_point_capturer.index(list_point_polygon[0]) + 1

	for i in list_point_polygon:
		if i not in list_point_capturer and i not in list_delete:
			list_point_capturer.insert(index, i)
			index += 1


def delete_points_from_capturer():
	global list_delete, list_point_capturer
	
	for i in list_delete:
		if i in list_point_capturer:
			index = list_point_capturer.index(i)
			list_point_capturer.pop(index)


def creat_polygon():
	global list_delete

	if opr_nap() == 'right':
		list_point_polygon.reverse()

	list_delete = []
	index = list_point_capturer.index(list_point_polygon[-1])
	n = -1

	while list_point_polygon[-1] != list_point_polygon[0]:
		list_point_polygon.append(list_point_capturer[index + n])
		list_delete.append(list_point_capturer[index + n])
		n -= 1
	
	# удаление ненужных точек
	list_point_polygon.pop()
	list_delete.pop()

	delete_points_from_capturer()
	add_points_in_capturer()
	root.c.create_polygon(list_point_polygon, fill=color, outline='black')
	create_new_polygon()
	instaler_begin_setings()

	# проверка точек


def test():
	global list_point_capturer, corect_x, corect_y, last_x, last_y, status_capturer, list_point_polygon, col_hod

	if status_capturer != True:
		return False

	elif abs(corect_x - last_x) > 20 or abs(corect_y - last_y) > 20:
		return False

	elif col_hod <= 0:
		return False

	elif last_x == corect_x and last_y == corect_y:
		return False

	elif len(list_point_polygon) >= 2:
		point_hod_1 = list_point_polygon[-2]
		point_hod_2 = list_point_polygon[-1]
		if (point_hod_1[0] - point_hod_2[0] == point_hod_2[0] - corect_x and point_hod_1[1] - point_hod_2[1] == point_hod_2[1] - corect_y): 
			return False

	return True


def move(event):
	global list_point_capturer, corect_x, corect_y, last_x, last_y, status_capturer, list_point_polygon, col_hod, color

	root.c.delete('capturer')
	x = event.x
	y = event.y
	corect_x = x % 20
	corect_y = y % 20

	if corect_x > 10:
		corect_x = x // 20 * 20 + 20
	else:
		corect_x = x // 20 * 20

	if corect_y > 10:
		corect_y = y // 20 * 20 + 20
	else:
		corect_y = y // 20 * 20

	if status_capturer == True:
		if test():
			root.c.create_oval((corect_x - 4, corect_y - 4), (corect_x + 4, corect_y + 4), fill=color, tag='capturer')
			root.c.create_line(last_x, last_y, corect_x, corect_y, width=3, fill=color, tag='capturer')
	else:
		if list_point_capturer.count([corect_x, corect_y]):
			last_x = corect_x
			last_y = corect_y
			root.c.create_oval((corect_x - 4, corect_y - 4), (corect_x + 4, corect_y + 4), fill=color, tag='capturer')


def capturer(event):
	global list_point_capturer, corect_x, corect_y, last_x, last_y, status_capturer, list_point_polygon, col_hod

	if status_capturer == True:
		if test():
			root.c.create_line(last_x, last_y, corect_x, corect_y, width=3, fill=color, tag='polygon')
			list_point_polygon.append([corect_x, corect_y])
			last_x = corect_x
			last_y = corect_y
			col_hod -= 1
			if list_point_capturer.count(list_point_polygon[-1]):
				creat_polygon()
	else:
		status_capturer = True
		list_point_polygon.append([corect_x, corect_y])
		last_x = corect_x
		last_y = corect_y


def off(event):
	exit()


def main():
	global root

	root = Start_window('Growing mountain')
	root.init_start_window()

	# root.new_game.bind('<Button-1>', Event.start_game())
	# create_game_field(root, 200, 200)
	# c.bind('<Motion>', move)
	# c.bind('<Button-1>', capturer)
	# c.bind('<Button-3>', off)
	# root.mainloop()


if __name__ == '__main__':
	main()