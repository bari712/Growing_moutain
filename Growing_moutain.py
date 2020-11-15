from tkinter import *


PLAYERS = []
LIST_POLYGONS = []


def test():
	global polygon, corect_x, corect_y, last_x, last_y

	if player.status_capturer != True:
		return False

	elif abs(corect_x - last_x) > 20 or abs(corect_y - last_y) > 20:
		return False

	elif player.col_hod <= 0:
		return False

	elif last_x == corect_x and last_y == corect_y:
		return False

	elif len(polygon.list_points_polygon) >= 2:
		point_hod_1 = polygon.list_points_polygon[-2]
		point_hod_2 = polygon.list_points_polygon[-1]
		if (point_hod_1[0] - point_hod_2[0] == point_hod_2[0] - corect_x and point_hod_1[1] - point_hod_2[1] == point_hod_2[1] - corect_y): 
			return False

	return True


def move(event):
	global player, corect_x, corect_y, last_x, last_y

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

	if player.status_capturer == True:
		if test():
			root.c.create_oval((corect_x - 4, corect_y - 4), (corect_x + 4, corect_y + 4), fill=player.color, tag='capturer')
			root.c.create_line(last_x, last_y, corect_x, corect_y, width=3, fill=player.color, tag='capturer')
	else:
		if root.list_points_capturer.count([corect_x, corect_y]):
			last_x = corect_x
			last_y = corect_y
			root.c.create_oval((corect_x - 4, corect_y - 4), (corect_x + 4, corect_y + 4), fill=player.color, tag='capturer')


def capturer(event):
	global polygon, player, corect_x, corect_y, last_x, last_y

	if player.status_capturer == True:
		if test():
			root.c.create_line(last_x, last_y, corect_x, corect_y, width=3, fill=player.color, tag='polygon')
			polygon.list_points_polygon.append([corect_x, corect_y])
			last_x = corect_x
			last_y = corect_y
			player.col_hod -= 1
			if root.list_points_capturer.count(polygon.list_points_polygon[-1]):
				polygon.creater_polygon()
				polygon.delete_points_from_capturer()
				polygon.add_points_in_capturer()
				polygon.create_new_polygon()
				player.recovery_settings()
	else:
		polygon = Polygon()
		player.status_capturer = True
		polygon.list_points_polygon.append([corect_x, corect_y])
		last_x = corect_x
		last_y = corect_y


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

		self.new_game.bind('<Button-1>', Events.start_game)

		self.new_game.pack()
		self.online_game.pack()
		self.settings.pack()
		self.exit.pack()

		self.window.mainloop()


class Events():
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
		self.list_points_capturer = []


	def init_game_field(self):
		self.window = Tk()
		self.window.title(self.title)
		self.c = Canvas(self.window, width=self.w_canvas, height=self.h_canvas, bg='white')

		root.init_canvas()

		self.c.bind('<Motion>', move)
		self.c.bind('<Button-1>', capturer)

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

		self.list_points_capturer = (list(i for i in list_points_center if i[1] != self.h_canvas))


class Polygon():
	def __init__(self):
		self.list_points_polygon = []
		self.list_delete = []


	def opr_nap(self):
		x1 = self.list_points_polygon[0]
		x2 = self.list_points_polygon[-1]

		if root.list_points_capturer.index(x1) < root.list_points_capturer.index(x2):
			return 'left'
		elif root.list_points_capturer.index(x1) > root.list_points_capturer.index(x2):
			return 'right'
		else:
			return 'error'


	def add_points_in_capturer(self):
		index = root.list_points_capturer.index(polygon.list_points_polygon[0]) + 1

		for i in self.list_points_polygon:
			if i not in root.list_points_capturer and i not in self.list_delete:
				root.list_points_capturer.insert(index, i)
				index += 1


	def delete_points_from_capturer(self):
		for i in self.list_delete:
			if i in root.list_points_capturer:
				index = root.list_points_capturer.index(i)
				root.list_points_capturer.pop(index)


	def creater_polygon(self):
		global player
		if self.opr_nap() == 'right':
			self.list_points_polygon.reverse()

		index = root.list_points_capturer.index(polygon.list_points_polygon[-1])
		n = -1

		while polygon.list_points_polygon[-1] != polygon.list_points_polygon[0]:
			self.list_points_polygon.append(root.list_points_capturer[index + n])
			self.list_delete.append(root.list_points_capturer[index + n])
			n -= 1
			
		# удаление ненужных точек
		self.list_points_polygon.pop()
		self.list_delete.pop()

	
		root.c.create_polygon(self.list_points_polygon, fill=player.color, outline='black')


	def create_new_polygon(self):
		# pdb.set_trace()
		list_point_new_polygon = []
		for i in range(0, len(polygon.list_points_polygon)-1):
			x1 = polygon.list_points_polygon[i][0]
			y1 = polygon.list_points_polygon[i][1]
			x2 = polygon.list_points_polygon[i+1][0]
			y2 = polygon.list_points_polygon[i+1][1]

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
			if polygon.list_points_polygon[0][0] != polygon.list_points_polygon[-1][0] and polygon.list_points_polygon[0][1] != polygon.list_points_polygon[-1][1]:
				list_point_new_polygon.remove(polygon.list_points_polygon[0])
		except Exception as e:
			pass

		newlist = []
		for i in list_point_new_polygon:
			if i not in newlist:
				newlist.append(i)

		list_point_new_polygon = newlist
		# c.create_polygon(list_point_new_polygon, width=2, outline='red')
		polygon.get_scores(list_point_new_polygon)


	def get_scores(self, list_point_new_polygon):
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

		player.scores += int(col_point_in_polygon + (len(list_point_new_polygon)/2) - 1)
		

class Player():
	def __init__(self, name, color):
		self.name = name
		self.color = color
		self.status = False
		self.scores = 0
		self.status_capturer = False
		self.col_hod = 10


	def add_scores(self, scores):
		self.scores += scores


	def recovery_settings(self):
		self.status_capturer = False
		self.col_hod = 10


def main():
	global root, player

	player = Player('Player_1', 'Green')
	root = Start_window('Growing mountain')
	root.init_start_window()


if __name__ == '__main__':
	main()