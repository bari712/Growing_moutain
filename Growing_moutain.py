from tkinter import *
import pdb


col_hod = 10
list_point_polygon = []
status_capturer = False
list_point_capturer = []
last_x = 0
last_y = 0
color = 'green'


def instaler_begin_setings():
	global list_point_capturer, corect_x, corect_y, last_x, last_y, status_capturer, list_point_polygon, col_hod

	col_hod = 10
	list_point_polygon = []
	status_capturer = False
	last_x = 0
	last_y = 0
	corect_x = None
	corect_y = None


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


def get_col_bal():
	global list_point_polygon, list_point_capturer

	# pdb.set_trace()
	# построение нового полигона
	list_point_new_polygon = [list_point_polygon[0]]
	# list_point_polygon.append(list_point_polygon[0])
	for i in range(0, len(list_point_polygon)-1):
		x1 = list_point_polygon[i][0]
		y1 = list_point_polygon[i][1]
		x2 = list_point_polygon[i+1][0]
		y2 = list_point_polygon[i+1][1]

		# list_point_new_polygon.append(list_point_polygon[i])

		# NW
		if x1 > x2 and y1 > y2:
			if [x1, y2] in list_point_new_polygon:
				list_point_new_polygon.pop()
				list_point_new_polygon.append([x2, y2])
			else:
				list_point_new_polygon.append([x1, y2])
				list_point_new_polygon.append([x2, y2])
				

		# NE
		elif x1 < x2 and y1 > y2:
			if [x2, y1] in list_point_new_polygon:
				list_point_new_polygon.pop()
				list_point_new_polygon.append([x2, y2])
			else:
				list_point_new_polygon.append([x2, y1])
				list_point_new_polygon.append([x2, y2])

		# SW
		elif x1 > x2 and y1 < y2:
			if [x2, y1] in list_point_new_polygon:
				list_point_new_polygon.pop()
				list_point_new_polygon.append([x2, y2])
			else:
				list_point_new_polygon.append([x2, y1])
				list_point_new_polygon.append([x2, y2])


		# SE
		elif x1 < x2 and y1 < y2:
			if [x1, y2] in list_point_new_polygon:
				list_point_new_polygon.pop()
				list_point_new_polygon.append([x2, y2])
			else:
				list_point_new_polygon.append([x1, y2])
				list_point_new_polygon.append([x2, y2])
		else:
			if [x2, y2] in list_point_new_polygon:
				list_point_new_polygon.pop()
			else:
				list_point_new_polygon.append([x2, y2])
				
	if list_point_polygon[0][0] != list_point_polygon[-1][0] and list_point_polygon[0][1] != list_point_polygon[-1][1]:
		list_point_new_polygon.remove(list_point_polygon[0])

	c.create_polygon(list_point_new_polygon, width=2, outline='red')

	# for i in list_point_new_polygon:
	# 	c.delete('test')
	# 	c.create_oval(i[0]-4, i[1]-4, i[0]+4, i[1]+4, fill='blue', tag='test')
	# 	input()


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
	c.create_polygon(list_point_polygon, fill='green', outline='black')
	get_col_bal()
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
	global list_point_capturer, corect_x, corect_y, last_x, last_y, status_capturer, list_point_polygon, col_hod

	c.delete('capturer')
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
			c.create_oval((corect_x - 4, corect_y - 4), (corect_x + 4, corect_y + 4), fill=color, tag='capturer')
			c.create_line(last_x, last_y, corect_x, corect_y, width=3, fill=color, tag='capturer')
	else:
		if list_point_capturer.count([corect_x, corect_y]):
			last_x = corect_x
			last_y = corect_y
			c.create_oval((corect_x - 4, corect_y - 4), (corect_x + 4, corect_y + 4), fill=color, tag='capturer')


def capturer(event):
	global list_point_capturer, corect_x, corect_y, last_x, last_y, status_capturer, list_point_polygon, col_hod

	if status_capturer == True:
		if test():
			c.create_line(last_x, last_y, corect_x, corect_y, width=3, fill=color, tag='polygon')
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
	root = Tk()
	create_game_field(root, 200, 200)
	c.bind('<Motion>', move)
	c.bind('<Button-1>', capturer)
	c.bind('<Button-3>', off)
	root.mainloop()


if __name__ == '__main__':
	main()