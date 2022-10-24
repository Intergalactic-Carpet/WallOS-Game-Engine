import turtle
import random
import keyboard
from time import sleep
from math import ceil, atan, sqrt
from shapely.geometry import Polygon
from pynput.keyboard import Controller

backpack_alter = 2
key_board = Controller()
screen = turtle.Screen()
screen.tracer(False)
screen.title('WallOS -- Game Engine -- Version 1.0')
ground = turtle.Turtle()
ground.hideturtle()
ground.speed(0)
player = turtle.Turtle()
player.hideturtle()
player.speed(0)
player.fillcolor('white')
orientation_ = 0
death_collisions = []
players = []
gravity = -9.8  # m/s
gravity = gravity
gga = 30
collisions = []
record = []
respawn_list = []
text = turtle.Turtle()
text.hideturtle()
main_screen = turtle.Turtle()
main_screen.hideturtle()
mouse_pointer = turtle.Turtle()
mouse_pointer.hideturtle()
box = turtle.Turtle()
box.hideturtle()
door = turtle.Turtle()
door.hideturtle()
door.speed(0)
sensor = turtle.Turtle()
sensor.hideturtle()
sensor.speed(0)
debug = False
main_colour = 'black'
prox_sensor = []
door_ceil = []
door_left_walls = []
door_right_walls = []
door_floors = []
w_box = turtle.Turtle()
w_box.hideturtle()
w_box.speed(0)
bxs = 5
bys = 6
w_top = Polygon([(-350, 350), (350, 350), (0, 500)])
w_bot = Polygon([(-350, -350), (350, -350), (0, -500)])
w_left = Polygon([(-350, 400), (-350, -400), (-500, 0)])
w_right = Polygon([(350, 400), (350, -400), (500, 0)])


def record_pos(pos, relay=False):
    global record
    if not relay:
        record = record + [pos]
    else:
        rel = record
        record = []
        return rel, rel


def list_add(_list, list_):
    if type(_list) != list:
        _list = [_list]
    _list = _list + [list_]
    return _list


def draw_death_rectangle(x, y, w, h, fill=True):
    global death_collisions
    x2 = x + w
    y2 = y + h
    # draw rec
    ground.pencolor('darkred')
    ground.fillcolor('indigo')
    ground.penup()
    ground.goto(x, y)
    if fill:
        ground.begin_fill()
    ground.pendown()
    ground.goto(x, y2)
    ground.goto(x2, y2)
    ground.goto(x2, y)
    ground.goto(x, y)
    if fill:
        ground.end_fill()
    ground.color(main_colour)
    death_collisions = death_collisions + \
        [(Polygon([(x, y), (x, y2), (x2, y2), (x2, y)]), [(x, y), (x, y2), (x2, y2), (x2, y)])]


def draw_collision_slope(x, y, x2, y2, width, fill=False):
    global collisions
    ground.penup()
    ground.goto(x, y)
    ground.pendown()
    if fill:
        ground.begin_fill()
    ground.goto(x2, y2)
    ground.goto(x2, y2 + width)
    ground.goto(x, y + width)
    ground.goto(x, y)
    if fill:
        ground.end_fill()
    left = [(x, y), (x, y2)]
    right = [(x2, y), (x2, y2)]
    collisions = collisions + [left, right, 'slope']


def draw_collision_rectangle(x, y, w, h, fill=False, rebound=10):
    global collisions
    x2 = x + w
    y2 = y + h
    # draw rec
    ground.penup()
    ground.goto(x, y)
    if fill:
        ground.begin_fill()
    ground.pendown()
    ground.goto(x, y2)
    ground.goto(x2, y2)
    ground.goto(x2, y)
    ground.goto(x, y)
    if fill:
        ground.end_fill()
    collisions = collisions + [[x, y, x2, y2, rebound, 'block']]
    print(collisions)
    # calc collision


def draw_screen():
    global person, space_key

    def draw_char():
        global orientation_, backpack_alter, players
        x = 5
        if keyboard.is_pressed('control'):
            x -= 4
        if keyboard.is_pressed('shift'):
            x += 3
        if keyboard.is_pressed('a'):
            x = x * -1
        elif keyboard.is_pressed('d'):
            pass
        else:
            x = 0
        if space_key.check_key():
            y = 20
        else:
            y = 0
        if keyboard.is_pressed('control'):
            i = 0.75
        else:
            i = 1
        person.update(False, x, y)
        coords = person.coords
        x2 = x
        # backpack
        backpack_alter = (backpack_alter - x2) / 20
        backpack_alter_ = backpack_alter * 10
        if backpack_alter_ <= 0.1:
            player.penup()
            player.goto(person.x, person.y2)
            player.setheading(270)
            if i == 1:
                player.forward(5)
            else:
                player.forward(15)
            player.begin_fill()
            player.pendown()
            player.setheading(0)
            player.forward(backpack_alter_ - 2)
            player.setheading(270)
            player.forward(15)
            player.setheading(180)
            player.forward(backpack_alter_ - 2)
            player.end_fill()
        if backpack_alter_ >= -0.1:
            player.penup()
            player.goto(person.x2, person.y2)
            player.setheading(270)
            if i == 1:
                player.forward(5)
            else:
                player.forward(15)
            player.begin_fill()
            player.pendown()
            player.setheading(0)
            player.forward(backpack_alter_ + 2)
            player.setheading(270)
            player.forward(15)
            player.setheading(180)
            player.forward(backpack_alter_ + 2)
            player.end_fill()
        x, y = coords
        player.penup()
        player.goto(x, y)
        player.pendown()
        player.setheading(90)
        player.forward(50 * i)
        player.begin_fill()
        player.setheading(0)
        player.forward(10)
        player.setheading(270)
        player.forward(15)
        player.setheading(0)
        player.backward(10)
        player.end_fill()
        player.setheading(270)
        player.backward(15)
        player.forward(15)
        player.setheading(0)
        player.forward(10)
        player.setheading(270)
        player.backward(15)
        player.forward(50 * i)

    def draw_doors_and_sensors():
        global prox_sensor, players
        door1.open = sensor1.on
        door1.draw()
        door1.calc_collisions()
        sensor1.y = door1.sy + door1.height / 2
        sensor1.draw()

    def draw_map():
        draw_collision_rectangle(-250, -10, 600, 10, True)
        draw_collision_rectangle(-50, 45, 25, 5)
        draw_collision_rectangle(-100, 80, 50, 5)
        draw_collision_rectangle(-250, 80, 50, 5)
        draw_collision_rectangle(-100, 170, 100, 5)
        draw_collision_rectangle(-150, 100, 5, 50)
        draw_collision_rectangle(240, 45, 100, 5)
        draw_death_rectangle(-450, -300, 1000, 5)
        # draw_collision_slope(20, -20, 150, 90, 15)
        spawn1 = CreateCheckpoint(-100, 250, 50, 50, 'spawn1')
        spawn1.draw()
        draw_collision_rectangle(150, 90, 400, 15)
        draw_collision_rectangle(150, 170, 400, 15)

    person = CreatePlayer(-5, 0, 10, 50)
    door1 = CreateDoubleVerticalSlidingDoor(105, 70, 150, 10, 65, 20)
    sensor1 = CreateProximityButton(150, 100, 50, 50, 50, 5, 'e', 'sensor1')
    # CreateProximityButton(150, 100, 50, 50, 50, 5, 'e', 'sensor1')
    space_key = BufferKey(' ', 1.5, touching_map, person.map_coll)
    draw_map()
    while True:
        update_box()
        player.clear()
        door.clear()
        sensor.clear()
        draw_doors_and_sensors()
        players = []
        draw_char()
        screen.update()
        sleep(0.01)
        if keyboard.is_pressed('escape'):
            exit()


def collision_search(c1, c2, dimensions='null'):
    if debug:
        print(dimensions)
    detected = False
    for _ in range(len(c2)):
        if c1.intersects(c2[_][0]):
            detected = True
    return detected


def invert(in_):
    if in_:
        in_ = False
    else:
        in_ = True
    return in_


def close_to(var, var2, thresh):
    re = False
    if thresh > (var - var2) > -thresh:
        re = True
    return re


def find_smallest(list_, secondary_index=0):
    rec = float('inf')
    for _ in range(len(list_)):
        if int(list_[_][secondary_index]) < rec:
            rec = int(list_[_][secondary_index])
    return rec


def find_largest(list_, secondary_index=0):
    rec = -float('inf')
    for _ in range(len(list_)):
        if int(list_[_][secondary_index]) > rec:
            rec = int(list_[_][secondary_index])
    return rec


class CreateProximityButton:

    def __init__(self, x, y, top_prox, right_prox, left_prox, bottom_prox, button_key, name, size=5, draw=True,
                 on_colour='green', off_colour='red', prox_colour='orange'):
        global prox_sensor
        self.draw_ = draw
        self.oc = on_colour
        self.ofc = off_colour
        self.size = size
        self.key_ = str.lower(str(button_key))
        self.x = x
        self.y = y
        self.pxc = prox_colour
        x2 = x + right_prox
        x = x - left_prox
        y2 = y + top_prox
        y = y - bottom_prox
        self.collisions = [(x, y), (x2, y), (x2, y2), (x, y2)]
        prox_sensor = list_add(prox_sensor, [Polygon(self.collisions), self.collisions])
        self.collisions = Polygon(self.collisions)
        self.name = name
        self.on = False
        self.toggle_source = Toggle(False)
        self.key_store = 0

    def key_state(self):
        return self.on

    def draw(self):
        if self.draw_:
            if collision_search(self.collisions, [person.full_collisions]):
                sensor.color(self.pxc)
            elif self.on:
                sensor.color(self.oc)
            else:
                sensor.color(self.ofc)
            sensor.penup()
            sensor.goto(self.x + self.size, self.y + self.size)
            sensor.begin_fill()
            sensor.pendown()
            sensor.goto(self.x + self.size, self.y)
            sensor.goto(self.x, self.y)
            sensor.goto(self.x, self.y + self.size)
            sensor.goto(self.x + self.size, self.y + self.size)
            sensor.end_fill()
        self.key_press()

    def key(self):
        return self.key_

    def key_press(self):
        if collision_search(self.collisions, [person.full_collisions]) and keyboard.is_pressed(self.key_):
            if self.key_store <= 0:
                self.on = self.toggle_source.toggle()
                self.key_store += 1
        else:
            self.key_store = 0


class Toggle:

    def __init__(self, on):
        self.on = on

    def toggle(self):
        if self.on:
            self.on = False
        else:
            self.on = True
        return self.on

    def state(self):
        return self.on


class CreateProximitySensor:

    def __init__(self, x, y, top_prox, right_prox, left_prox, bottom_prox, size=5, on_colour='green', off_colour='red'):
        global prox_sensor
        self.oc = on_colour
        self.ofc = off_colour
        self.size = size
        self.x = x
        self.y = y
        x2 = x + right_prox
        x = x - left_prox
        y2 = y + top_prox
        y = y - bottom_prox
        self.collisions = [(x, y), (x2, y), (x2, y2), (x, y2)]
        prox_sensor = list_add(prox_sensor, [Polygon(self.collisions), self.collisions])
        self.collisions = Polygon(self.collisions)

    def draw(self, on):
        if on:
            sensor.color(self.oc)
        else:
            sensor.color(self.ofc)
        sensor.penup()
        sensor.goto(self.x + self.size, self.y + self.size)
        sensor.begin_fill()
        sensor.pendown()
        sensor.goto(self.x + self.size, self.y)
        sensor.goto(self.x, self.y)
        sensor.goto(self.x, self.y + self.size)
        sensor.goto(self.x + self.size, self.y + self.size)
        sensor.end_fill()


class CreateHorizontalSlidingDoor:

    def __init__(self, closed_x, open_size, y, time_ms, width, height, is_left_open=True, fill=False):
        self.cx = closed_x
        self.y = y
        self.sx = closed_x
        self.side = is_left_open
        if self.side:
            self.ox = self.cx - open_size
        else:
            self.ox = self.cx - open_size
        self.speed = time_ms
        self.fill = fill
        self.width = width
        self.height = height
        self.open = False

    def draw(self):
        if self.open:
            self.sx += (self.ox - self.sx) / self.speed
        else:
            self.sx += (self.cx - self.sx) / self.speed
        x = self.sx + self.width
        y = self.y + self.height
        door.penup()
        door.goto(self.sx, self.y + self.height / 2)
        door.pendown()
        door.goto(self.sx, y)
        door.goto(x, y)
        door.goto(x, self.y + self.height / 2)
        door.goto(self.sx, self.y + self.height / 2)

    def calc_collisions(self):
        pass


class CreateDoubleVerticalSlidingDoor:

    def __init__(self, closed_y, open_size, x, time_ms, height, width, is_up_open=False, fill=False):
        self.cy = closed_y
        self.x = x
        self.sy = closed_y
        self.sx = width
        self.side = is_up_open
        self.original_y = closed_y
        self.oy = self.cy - open_size / 2
        self.speed = time_ms
        self.fill = fill
        self.width = width
        self.height = height
        self.open = False

    def draw(self):
        if self.open:
            self.sy += (self.oy - self.sy) / self.speed
        else:
            self.sy += (self.cy - self.sy) / self.speed
        door.penup()
        door.goto(self.x + self.sx, self.sy)
        door.pendown()
        door.goto(self.x + self.sx, self.sy + self.height / 2)
        door.goto(self.x + self.width - self.sx, self.sy + self.height / 2)
        door.goto(self.x + self.width - self.sx, self.sy)
        door.goto(self.x + self.sx, self.sy)

        door.penup()
        door.goto(self.x + self.sx, -self.sy + self.height / 2 + self.original_y * 2)
        door.pendown()
        door.goto(self.x + self.sx, -self.sy + self.height + self.original_y * 2)
        door.goto(self.x + self.width - self.sx, -self.sy + self.height + self.original_y * 2)
        door.goto(self.x + self.width - self.sx, -self.sy + self.height / 2 + self.original_y * 2)
        door.goto(self.x + self.sx, -self.sy + self.height / 2 + self.original_y * 2)

    def calc_collisions(self):
        pass


class CreateDoubleInsetVerticalSlidingDoor:

    def __init__(self, closed_y, open_size, x, time_ms, height, width, is_up_open=False, fill=False, fancy=True):
        self.cy = closed_y
        self.x = x
        self.sy = closed_y
        self.sx = width
        self.side = is_up_open
        self.original_y = closed_y
        self.oy = self.cy - open_size / 2
        self.detailed = fancy
        self.speed = time_ms
        self.fill = fill
        self.width = width
        self.height = height
        self.open = False

    def draw(self):
        i = 0.75
        if self.open:
            if self.sx <= self.width * i or close_to(self.sx, self.width * i, 0.1):
                self.sy += (self.oy - self.sy) / self.speed
            else:
                self.sx += (self.width * i - self.sx) / self.speed
        else:
            self.sy += (self.cy - self.sy) / self.speed
            if close_to(self.sy, self.cy, 0.1):
                self.sx += (self.width - self.sx) / self.speed
        door.penup()
        door.goto(self.x + self.sx, self.sy)
        door.pendown()
        door.goto(self.x + self.sx, self.sy + self.height / 2)
        if self.detailed and not close_to(self.sx, self.width * i, 0.1):
            door.penup()
        door.goto(self.x + self.width - self.sx, self.sy + self.height / 2)
        if self.detailed and not close_to(self.sx, self.width * i, 0.1):
            door.pendown()
        door.goto(self.x + self.width - self.sx, self.sy)
        door.goto(self.x + self.sx, self.sy)

        door.penup()
        door.goto(self.x + self.sx, -self.sy + self.height / 2 + self.original_y * 2)
        door.pendown()
        door.goto(self.x + self.sx, -self.sy + self.height + self.original_y * 2)
        door.goto(self.x + self.width - self.sx, -self.sy + self.height + self.original_y * 2)
        door.goto(self.x + self.width - self.sx, -self.sy + self.height / 2 + self.original_y * 2)
        if self.detailed and not close_to(self.sx, self.width * i, 0.1):
            door.penup()
        door.goto(self.x + self.sx, -self.sy + self.height / 2 + self.original_y * 2)
        if self.detailed and not close_to(self.sx, self.width * i, 0.1):
            door.pendown()

    def calc_collisions(self):
        pass


def load_points(points):
    turtle.clear()
    for _ in range(len(points)):
        if _ == 0:
            turtle.penup()
        turtle.goto(points[_])
        turtle.pendown()


class CreateInsetVerticalSlidingDoor:

    def __init__(self, closed_y, open_size, x, time_ms, height, width, is_up_open=False, fill=False):
        self.cy = closed_y
        self.x = x
        self.sy = closed_y
        self.sx = width
        self.side = is_up_open
        self.oy = self.cy - open_size
        self.speed = time_ms
        self.fill = fill
        self.width = width
        self.height = height
        self.open = False

    def draw(self):
        i = 0.75
        if self.open:
            if self.sx <= self.width * i or close_to(self.sx, self.width * i, 0.1):
                self.sy += (self.oy - self.sy) / self.speed
            else:
                self.sx += (self.width * i - self.sx) / self.speed
        else:
            self.sy += (self.cy - self.sy) / self.speed
            if close_to(self.sy, self.cy, 0.1):
                self.sx += (self.width - self.sx) / self.speed
        door.penup()
        door.goto(self.x + self.sx, self.sy)
        door.pendown()
        door.goto(self.x + self.sx, self.sy + self.height)
        door.goto(self.x + self.width - self.sx, self.sy + self.height)
        door.goto(self.x + self.width - self.sx, self.sy)
        door.goto(self.x + self.sx, self.sy)

    def calc_collisions(self):
        pass


class CreateVerticalSlidingDoor:

    def __init__(self, closed_y, open_size, x, time_ms, height, width, is_up_open=False, fill=False):
        self.cy = closed_y
        self.x = x
        self.sy = closed_y
        self.side = is_up_open
        if self.side:
            self.oy = self.cy - open_size
        else:
            self.oy = self.cy - open_size
        self.speed = time_ms
        self.fill = fill
        self.width = width
        self.height = height
        self.open = False

    def draw(self):
        if self.open:
            self.sy += (self.oy - self.sy) / self.speed
        else:
            self.sy += (self.cy - self.sy) / self.speed
        door.penup()
        door.goto(self.x, self.sy)
        door.pendown()
        door.goto(self.x, self.sy + self.height)
        door.goto(self.x + self.width, self.sy + self.height)
        door.goto(self.x + self.width, self.sy)
        door.goto(self.x, self.sy)

    def calc_collisions(self):
        pass


class CreateCheckpoint:

    def __init__(self, x, y, w, h, name, edge_colour='lightblue', x_alter=0, y_alter=0):
        global respawn_list
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name
        self.colour = edge_colour
        x2 = x + w
        y2 = y + h
        self.x2 = x2
        self.y2 = y2
        self.x_alter = x_alter
        self.y_alter = y_alter
        self.collisions = [(x, y), (x, y2), (x2, y2), (x2, y)]
        self.poly_col = Polygon([(x, y), (x, y2), (x2, y2), (x2, y)])
        self.respawn_point = ((((x + x2) / 2) + x_alter), (y + 1 + y_alter))
        respawn_list = respawn_list + [(self.poly_col, self.collisions, self.respawn_point, name)]

    def draw(self):
        x2 = self.x + self.w
        y2 = self.y + self.h
        if self.colour == 'null':
            colour = main_colour
        else:
            colour = self.colour
        ground.color(colour)
        ground.penup()
        ground.goto(self.x, self.y)
        ground.pendown()
        ground.goto(self.x, y2)
        ground.goto(x2, y2)
        ground.goto(x2, self.y)
        ground.goto(self.x, self.y)
        ground.color(main_colour)


class CreatePlayer:

    def __init__(self, x, y, w, h, speed=5, run_speed=7, time=20):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = x + w
        self.y2 = y + h
        self.xs = 0
        self.ys = 0
        self.map_coll = [self.x, self.y, self.x2, self.y2]
        self.speed = speed
        self.run_speed = run_speed
        self.coords = x, y
        self.time = time
        self.dimensions = [(self.x, self.y), (self.x, self.y2), (self.x2, self.y2), (self.x2, self.y)]
        self.full_collisions = [Polygon(self.dimensions), self.dimensions]
        self.anchor = 'null'

    def update(self, running, x=0, y=0):
        self.dimensions = [(self.x, self.y), (self.x, self.y2), (self.x2, self.y2), (self.x2, self.y)]
        self.full_collisions = [Polygon(self.dimensions), self.dimensions]
        if running:
            if x < 0:
                x = -(self.run_speed + x)
            else:
                x = self.run_speed + x
        if keyboard.is_pressed('ctrl'):
            y2 = self.y + (self.h * 0.75)
        else:
            y2 = self.y2
        x, y = calculate_player(x, y, self.xs, self.ys, [self.x, self.y, self.x2, y2], self.time)
        self.map_coll = [self.x, self.y, self.x2, y2]
        self.xs += x
        self.ys += y
        self.x += self.xs
        self.y += self.ys
        self.x2 = self.x + self.w
        self.y2 = self.y + self.h
        self.coords = self.x, self.y
        anchor, contact = respawn_search(Polygon(self.dimensions))
        if contact:
            self.anchor = anchor
        if collision_search(Polygon(self.dimensions), death_collisions, self.dimensions) or keyboard.is_pressed('r'):
            if self.anchor != 'null':
                x, y = self.anchor[2]
                self.set_coords(x - self.w / 2, y, True)
            else:
                self.set_coords(0 - self.w / 2, 1, True)

    def set_coords(self, x, y, reset):
        if reset:
            self.xs = 0
            self.ys = 0
        self.x = x
        self.y = y


def touching_map(char_dimensions):
    # block config: ([x, y, x2, y2, rebound], type)
    # char config: [x, y, x2, y2]
    o_ = 0
    cx1 = char_dimensions[0]
    cy1 = char_dimensions[1]
    cx2 = char_dimensions[2]
    cy2 = char_dimensions[3]
    if char_dimensions[1] == 'slope':
        pass
    else:
        for _ in range(len(collisions)):
            x = collisions[_][0]
            y = collisions[_][1]
            x2 = collisions[_][2]
            y2 = collisions[_][3]
            if cx2 > x > cx1 and cy2 > y and cy1 < y2:
                o_ += 1
            elif cx1 < x2 < cx2 and cy2 > y and cy1 < y2:
                o_ += 1
            if close_to(cy1, y2, 5) and cx2 > x and cx1 < x2:
                o_ += 1
            elif y < cy2 < y2 and cx2 > x and cx1 < x2:
                o_ += 1
    if o_ > 0:
        o_ = True
    else:
        o_ = False
    return o_


def calculate_player(tx, ty, cx, cy, char_dimensions, time_):
    sx = (tx - cx) / time_
    sy = (ty - cy) / gga
    # block config: ([x, y, x2, y2, rebound], type)
    # char config: [x, y, x2, y2]
    cx1 = char_dimensions[0]
    cy1 = char_dimensions[1]
    cx2 = char_dimensions[2]
    cy2 = char_dimensions[3]
    if char_dimensions[1] == 'slope':
        pass
    else:
        for _ in range(len(collisions)):
            x = collisions[_][0]
            y = collisions[_][1]
            x2 = collisions[_][2]
            y2 = collisions[_][3]
            rebound = collisions[_][4]
            if cx2 > x > cx1 and cy2 > y and cy1 < y2 and cx > 0:
                sx = (cx / rebound) * -20
            elif cx1 < x2 < cx2 and cy2 > y and cy1 < y2 and cx < 0:
                sx = (cx / rebound) * -20
            if y < cy1 < y2 and cy < 0 and cx2 > x and cx1 < x2:
                sy = (1 - cy) / 1
            elif y < cy2 < y2 and cx2 > x and cx1 < x2:
                sy = (cy / rebound) * -20
            elif not close_to(cy1, y2, 2) and close_to(sy, 0, 1) and not space_key.check_key():
                sy = (gravity - cy) / gga

    return sx, sy


def of_true():
    return True


class BufferKey:

    def __init__(self, key, max_duration_s, optional_function=of_true, optional_arg='null'):
        self.max = max_duration_s * 100
        self.buffer = 0
        self.key = key
        self.of = optional_function
        self.arg = optional_arg

    def reset(self):
        self.buffer = 0

    def max_out(self):
        self.buffer = self.max

    def check_key(self):
        if self.of == touching_map:
            call = touching_map(self.arg)
        else:
            call = self.of
        on = False
        if keyboard.is_pressed(self.key) and self.buffer < self.max:
            self.buffer += 1
            on = True
        elif self.buffer > 0 and call:
            self.buffer = 0
        return on


def update_box():
    global bxs, bys
    s_ = 10
    w_box.clear()
    x = w_box.xcor()
    y = w_box.ycor()
    coll = Polygon([(x, y), (x, y + s_), (x + s_, y + s_), (x + s_, y)])
    if coll.intersects(w_top):
        if bys > 0:
            bys = bys * -1
    elif coll.intersects(w_bot):
        if bys < 0:
            bys = bys * -1
    if coll.intersects(w_left):
        if bxs < 0:
            bxs = bxs * -1
    elif coll.intersects(w_right):
        if bxs > 0:
            bxs = bxs * -1
    w_box.penup()
    w_box.goto(x + bxs, y + bys)
    w_box.pendown()
    x = w_box.xcor()
    y = w_box.ycor()
    x2 = x + s_
    y2 = y + s_
    w_box.goto(x, y2)
    w_box.goto(x2, y2)
    w_box.goto(x2, y)
    w_box.goto(x, y)


def respawn_search(collisions_):
    collision = False
    anchor = 'null'
    for _ in range(len(respawn_list)):
        if collisions_.intersects(respawn_list[_][0]):
            collision = True
            anchor = respawn_list[_]
    return anchor, collision


def prep_assets():
    global person, back_button, debugger_label, space_key
    debugger_label = CreateButton('debug', 'debug', 0, -750, 0.1, 0, True, True, 'null', False)
    back_button = CreateButton('back', 'back', 0, -250, 0.2, 0, True, False, 'null', False)


def create_paragraph(_text_, max_chars):
    max_chars = int(max_chars)
    total_chars = 0
    text_list = []
    for de in range(int(ceil(int(len(_text_)) / max_chars))):
        text_ = ''
        for _ in range(max_chars):
            try:
                text_ = text_ + _text_[total_chars]
            except IndexError:
                pass
            total_chars += 1
        text_list = text_list + [text_]
    return text_list


def reset_mouse_pos():
    set_mouse_pos(0, 0)


class CreateButton:
    """
    Defines the button parameters according to the inputted information
    """

    def __init__(self, text_to_calc, text_to_print, button_x, button_y, size, orientation, bounding, greyed_out,
                 colour, bold):
        self.text_to_calc = text_to_calc
        self.text_to_print = text_to_print
        self.bx = button_x
        self.by = button_y
        self.size = size
        self.orientation = orientation
        self.bounding = bounding
        self.greyed = greyed_out
        self.bold = bold
        if 'null' in colour:
            self.colour = main_colour
        else:
            self.colour = colour
        spacing = 10
        if debug:
            print(f'Button Parameters: {self.text_to_calc}, {self.text_to_print}, {self.bx}, {self.by},'
                  f' {spacing}, {self.size}, {self.orientation}, {self.bounding}')
        main_screen.pencolor(self.colour)
        text.pencolor(self.colour)
        text_input = str.lower(str(text_to_calc))
        text_length = len(text_input)
        allowed_chars = 'abcdefghijklomnpqrstuvwxyz1234567890 ><-[]|_()!+%$'
        chars_length = len(allowed_chars)
        index = 0
        output = ''
        for _ in range(text_length):
            indexed = text_input[index]
            index_2 = 0
            for i in range(chars_length):
                second_indexed = allowed_chars[index_2]
                if indexed in second_indexed:
                    output = output + indexed
                index_2 += 1
            index += 1
        conditioned_len = len(output)
        final_x = self.bx + (conditioned_len * 70) * self.size
        final_y = self.by - (100 * self.size)
        if self.orientation == 0:
            alter = final_x / 2
        else:
            alter = 0
        if debug:
            print('fx', final_x, 'fy', final_y, 'bx', button_x, 'by', button_y, 'alt', alter)
        bound = Polygon([((self.bx - spacing) - alter, self.by + spacing),
                         ((final_x + spacing) - alter, self.by + spacing),
                         ((final_x + spacing) - alter, final_y - spacing),
                         ((self.bx - spacing) - alter, final_y - spacing)])
        self.final_x = final_x
        self.final_y = final_y
        self.spacing = spacing
        self.alter = alter
        self.bound = bound

    def draw_button(self):
        """
        Draws the button based on the previously inputted information
        """
        if self.bold:
            text.pensize(7)
        else:
            text.pensize(1)
        if self.greyed:
            text.color('grey')
            main_screen.pencolor('grey')
        else:
            text.color(self.colour)
            main_screen.pencolor(main_colour)
        contact = mouse.intersects(self.bound)
        if contact and not self.greyed:
            spacing = 15
        else:
            spacing = 10
        if self.bounding:
            main_screen.penup()
            main_screen.goto((self.bx - spacing) - self.alter, self.by + spacing)
            main_screen.begin_fill()
            main_screen.pendown()
            main_screen.goto((self.final_x + spacing) - self.alter, self.by + spacing)
            main_screen.goto((self.final_x + spacing) - self.alter, self.final_y - spacing)
            main_screen.goto((self.bx - spacing) - self.alter, self.final_y - spacing)
            main_screen.goto((self.bx - spacing) - self.alter, self.by + spacing)
            main_screen.end_fill()
        draw_text(self.bx, self.by, self.text_to_print, self.size, self.alter)
        text.pencolor(self.colour)
        main_screen.pencolor(main_colour)
        if self.greyed:
            contact = False
        return contact


def set_mouse_pos(mx, my):
    global mouse, text_box_clear
    clear_screen()
    mouse_pointer.penup()
    mouse_pointer.goto(mx, my)
    mouse_pointer.pendown()
    nx = mouse_pointer.xcor()
    ny = mouse_pointer.ycor()
    if text_box_clear:
        clear_screen()
        screen.update()
        text_box_clear = False
    mouse = Polygon([(nx, ny + 1), (nx + 1, ny - 1), (nx - 1, ny - 1)])
    debugger_label.draw_button()
    screen.update()


def draw_label(text_to_calc, text_to_print, label_x, label_y, size, orientation, greyed_out, colour='null',
               bold=False, bounding=False):
    """
    Draws a label based on parameters and returns if the button is pressed
    :param text_to_calc: The text to be calculated for the bounding, collisions, and orientation
    :param text_to_print: The text that is printed
    :param label_x: Top Left corner X coordinate
    :param label_y: Top Left corner Y coordinate
    :param size: Size of the text
    :param orientation: If it's centered or not, a value of -1 keeps the top left corner of the text relative to the
     given coordinates, while a value of 0 centers the text
    :param greyed_out: Whether the text and bounding is grey or not, if True the button turns grey and the contact value
     is set to False
    :param colour: Colour of the text and bounding
    :param bold: Whether the text is bold
    :param bounding: Whether a box surrounds the text
    :return: Whether the button has been clicked (contact)
    """
    global custom_label
    custom_label = CreateButton(text_to_calc, text_to_print, label_x, label_y, size, orientation, bounding, greyed_out,
                                colour, bold)
    contact = custom_label.draw_button()
    return contact


def draw_box(start_x, start_y, width, height, colour, fill, x_center, y_center, size=0):
    """
    Draws a box with the specified parameters
    :param start_x: The top left corner of the box (x coordinate)
    :param start_y: The top left corner of the box (y coordinate)
    :param width: The width of the box
    :param height: The height of the box
    :param colour: The colour of the box
    :param fill: Whether the box is filled
    :param x_center: Whether the box is centered along the X axis
    :param y_center: Whether the box is centered along the Y axis
    :param size: size of text (keep at 0 if you're not using text)
    :return: Nothing
    """
    if x_center:
        start_x = (start_x - (width / 2)) - (70 * size)
    if y_center:
        start_y = start_y - (height / 2)
    final_x = start_x + width
    final_y = start_y + height
    box.color(colour)
    box.penup()
    box.goto(start_x, start_y)
    if fill:
        box.begin_fill()
    box.goto(final_x, start_y)
    box.goto(final_x, final_y)
    box.goto(start_x, final_y)
    box.goto(start_x, start_y)
    if fill:
        box.end_fill()


def input_box(add_string):
    global text_box_string, text_box_output, text_box_input, text_box_clear, int_rate, principal, alias
    if text_box_input:
        clear_screen()
        box.clear()
        if add_string == '-':
            text_box_string = f"{text_box_string[0: -1]}"
        elif add_string == '=':
            text_box_output = text_box_string
            text_box_string = ''
            if debug:
                print(text_box_output)
            if alias != '':
                pass
            alias = ''
            text_box_input = False
            text_box_clear = True
            clear_screen()
        else:
            text_box_string = text_box_string + str(add_string)
        if alias == '':
            pass
        else:
            draw_label('Continue', 'Continue', 0, -200, 0.3, 0, False, bounding=True)
        draw_box(0, -40, (len(text_box_string) * 70) * 0.3 + 20, 50, 'lightgrey', True,
                 True, False, 0)
        draw_label(text_box_string,
                   str.lower(text_box_string), 0, 0, 0.3, 0, False)
        debugger_label.draw_button()


def clear_screen():
    main_screen.clear()
    text.clear()
    box.clear()
    turtle.clear()


def decimal_remover(num):
    """
    Removes the decimal and subsequent text from the string
    :param num: The number to remove the decimal from
    :return: The outputted number without a decimal
    """
    num = number_converter(num)
    num_len = len(str(num))
    output = ''
    on = True
    index = 0
    for _ in range(num_len):
        indexed = num[index]
        if indexed == '.':
            on = False
        if on:
            output = output + indexed
        index += 1
    return output


def rounder(num, round_to):
    """
    Rounds a number by removing letters outside the specified parameter
    :param num: The number to round
    :param round_to: Decimal places to round to
    :return: Rounded Output
    """
    num = str(num)
    count = 0
    on = True
    pd_count = 0
    pd = False
    output = ''
    for _ in range(int(len(num))):
        indexed = num[count]
        if on:
            output = output + indexed
        count += 1
        if indexed == '.':
            pd = True
        elif pd:
            pd_count += 1
        if pd_count >= round_to:
            on = False
    return str(output)


def number_converter(num_input):
    """
    Removes all characters except numbers and periods
    :param num_input: String to convert
    :return: Number
    """
    num_input = str(num_input)
    num_len = len(num_input)
    allowed_chars = '1234567890.'
    chars_length = len(allowed_chars)
    index = 0
    output = ''
    for _ in range(num_len):
        indexed = num_input[index]
        index_2 = 0
        for i in range(chars_length):
            second_indexed = allowed_chars[index_2]
            if indexed in second_indexed:
                output = output + indexed
            index_2 += 1
        index += 1
    return output


def draw_text(s_x, s_y, input_text, size, alter=0):
    """
    Draws Text based on inputted parameters
    :param s_x: Top left X coordinate
    :param s_y: Top left Y coordinate
    :param input_text: Text to be drawn
    :param size: Size of the text (Max recommended: 1)
    :param alter: How much to alter the x coordinate
    :return: X coordinate of the bottom right corner, Y coordinate of the bottom right corner
    """
    index = 0
    msg = str.lower(input_text)
    str_length = len(msg)
    text.penup()
    text.goto(s_x - alter, s_y)
    text.pendown()
    for i in range(str_length):
        msg2 = msg[index]
        if 'a' in msg2:
            a(size)
        elif 'b' in msg2:
            b(size)
        elif 'c' in msg2:
            c(size)
        elif 'd' in msg2:
            d(size)
        elif 'e' in msg2:
            e(size)
        elif 'f' in msg2:
            f(size)
        elif 'g' in msg2:
            g(size)
        elif 'h' in msg2:
            lh(size)
        elif 'i' in msg2:
            letter_i(size)
        elif 'j' in msg2:
            j(size)
        elif 'k' in msg2:
            k(size)
        elif 'l' in msg2:
            letter_l(size)
        elif 'o' in msg2:
            o(size)
        elif 'm' in msg2:
            m(size)
        elif 'n' in msg2:
            n(size)
        elif 'p' in msg2:
            p(size)
        elif 'q' in msg2:
            q(size)
        elif 'r' in msg2:
            r(size)
        elif 's' in msg2:
            s(size)
        elif 't' in msg2:
            t(size)
        elif 'u' in msg2:
            u(size)
        elif 'v' in msg2:
            v(size)
        elif 'w' in msg2:
            lw(size)
        elif 'x' in msg2:
            lx(size)
        elif 'y' in msg2:
            ly(size)
        elif 'z' in msg2:
            z(size)
        elif '1' in msg2:
            num_1(size)
        elif '2' in msg2:
            num_2(size)
        elif '3' in msg2:
            num_3(size)
        elif '4' in msg2:
            num_4(size)
        elif '5' in msg2:
            num_5(size)
        elif '6' in msg2:
            num_6(size)
        elif '7' in msg2:
            num_7(size)
        elif '8' in msg2:
            num_8(size)
        elif '9' in msg2:
            num_9(size)
        elif '0' in msg2:
            num_0(size)
        elif ' ' in msg2:
            space(size)
        elif '!' in msg2:
            exclamation(size)
        elif '?' in msg2:
            question(size)
        elif "'" in msg2:
            apostrophe(size)
        elif '"' in msg2:
            quote(size)
        elif ',' in msg2:
            comma(size)
        elif '.' in msg2:
            period(size)
        elif '[' in msg2:
            left_square_bracket(size)
        elif ']' in msg2:
            right_square_bracket(size)
        elif '>' in msg2:
            back_slash(size)
        elif '<' in msg2:
            forward_slash(size)
        elif '|' in msg2:
            rod_thing(size)
        elif '-' in msg2:
            subtract_sign(size)
        elif '+' in msg2:
            addition_sign(size)
        elif '(' in msg2:
            left_curved_bracket(size)
        elif ')' in msg2:
            right_curved_bracket(size)
        elif '_' in msg2:
            under_score(size)
        elif ':' in msg2:
            colon(size)
        elif '$' in msg2:
            dollar_sign(size)
        elif '%' in msg2:
            percent_sign(size)
        index += 1
    text.penup()
    text.right(90)
    text.forward(100 * size)
    text.setheading(0)
    text.pendown()
    return text.xcor(), text.ycor()


def text_conditioner(text_input):
    text_input = str.lower(str(text_input))
    text_length = len(text_input)
    allowed_chars = 'abcdefghijklomnpqrstuvwxyz1234567890,." ><-[]|_()!'
    chars_length = len(allowed_chars)
    index = 0
    output = ''
    for _ in range(text_length):
        indexed = text_input[index]
        index_2 = 0
        for i in range(chars_length):
            second_indexed = allowed_chars[index_2]
            if indexed in second_indexed:
                output = output + indexed
            index_2 += 1
        index += 1
    return output


def rand(minimum, maximum):
    rando = random.randint(minimum, maximum)
    return rando


def text_filter(text_input, allowed_chars):
    """
    Removes all characters that aren't specified as allowed
    :param text_input: The text to be filtered
    :param allowed_chars: The characters allowed in the text
    :return: The filtered text
    """
    text_input = str.lower(str(text_input))
    text_length = len(text_input)
    chars_length = len(allowed_chars)
    index = 0
    output = ''
    for _ in range(text_length):
        indexed = text_input[index]
        index_2 = 0
        for i in range(chars_length):
            second_indexed = allowed_chars[index_2]
            if indexed in second_indexed:
                output = output + indexed
            index_2 += 1
        index += 1
    return output


def inverted_text_filter(text_input, banned_chars):
    """
    Removes all characters that are specified as banned
    :param text_input: The text to be filtered
    :param banned_chars: The characters banned from the text
    :return: The filtered text
    """
    text_input = str.lower(str(text_input))
    text_length = len(text_input)
    chars_length = len(banned_chars)
    index = 0
    output = ''
    for _ in range(text_length):
        indexed = text_input[index]
        index_2 = 0
        for i in range(chars_length):
            second_indexed = banned_chars[index_2]
            if indexed not in second_indexed:
                output = output + indexed
            index_2 += 1
        index += 1
    return output


def letter_reset(size):
    text.setheading(0)
    text.penup()
    text.left(90)
    text.forward(100 * size)
    text.right(90)
    text.forward(20 * size)
    text.pendown()
    if debug:
        position = text.pos()
        print(position)


def dollar_sign(size):
    s(size)
    text.penup()
    text.setheading(0)
    text.backward(70 * size)
    text.left(90)
    text.forward(10 * size)
    text.right(90)
    text.forward(25 * size)
    text.right(90)
    text.pendown()
    text.forward(120 * size)
    text.backward(10 * size)
    text.left(90)
    text.penup()
    text.forward(25 * size)
    text.pendown()
    letter_reset(size)


def percent_sign(size):
    bx = text.xcor()
    by = text.ycor()
    for _ in range(10):
        text.forward(10 * size)
        text.right(90)
    text.penup()
    text.goto(bx + 50 * size, by - 100 * size)
    text.pendown()
    for _ in range(10):
        text.forward(10 * size)
        text.right(90)
    text.penup()
    text.goto(bx, by)
    text.pendown()
    forward_slash(size)


def under_score(size):
    text.penup()
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.pendown()
    text.forward(50 * size)
    letter_reset(size)


def left_curved_bracket(size):
    text.penup()
    text.right(90)
    text.forward(25 * size)
    text.left(90)
    text.pendown()
    tangent(25 * size, 25 * size, True)
    text.setheading(0)
    text.forward(25 * size)
    text.penup()
    text.backward(50 * size)
    text.right(90)
    text.forward(25 * size)
    text.pendown()
    text.forward(50 * size)
    tangent(25 * size, 25 * size, False)
    text.forward(25 * size)
    letter_reset(size)


def right_curved_bracket(size):
    text.forward(25 * size)
    tangent(25 * size, 25 * size, False)
    text.right(90)
    text.forward(50 * size)
    tangent(25 * size, -25 * size, False)
    text.right(180)
    text.forward(25 * size)
    text.penup()
    text.right(180)
    text.forward(50 * size)
    text.pendown()
    letter_reset(size)


def addition_sign(size):
    text.penup()
    text.forward(25 * size)
    text.right(90)
    text.forward(25 * size)
    text.pendown()
    text.forward(50 * size)
    text.backward(25 * size)
    text.left(90)
    text.forward(25 * size)
    text.backward(50 * size)
    text.right(90)
    text.penup()
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.pendown()
    letter_reset(size)


def left_square_bracket(size):
    text.forward(50 * size)
    text.backward(50 * size)
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.forward(50 * size)
    letter_reset(size)


def right_square_bracket(size):
    text.forward(50 * size)
    text.right(90)
    text.forward(100 * size)
    text.right(90)
    text.forward(50 * size)
    text.backward(50 * size)
    letter_reset(size)


def back_slash(size):
    tangent(100 * size, 50 * size, False)
    letter_reset(size)


def forward_slash(size):
    text.penup()
    text.forward(50 * size)
    text.pendown()
    tangent(100 * size, -50 * size, False)
    text.penup()
    text.forward(50 * size)
    text.pendown()
    letter_reset(size)


def subtract_sign(size):
    text.penup()
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.pendown()
    text.forward(50 * size)
    text.right(90)
    text.penup()
    text.forward(50 * size)
    text.pendown()
    letter_reset(size)


def rod_thing(size):
    text.penup()
    text.forward(25 * size)
    text.pendown()
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.penup()
    text.forward(25 * size)
    text.pendown()
    letter_reset(size)


def a(size):
    text.penup()
    text.forward(25 * size)
    text.pendown()
    tangent(100 * size, 25 * size, False)
    text.penup()
    text.backward(50 * size)
    text.left(90)
    text.forward(100 * size)
    text.right(90)
    text.forward(25 * size)
    text.pendown()
    tangent(100 * size, -25 * size, False)
    text.penup()
    text.left(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(12 * size)
    text.pendown()
    text.forward(25 * size)
    text.penup()
    text.forward(13 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    letter_reset(size)


def b(size):
    text.forward(40 * size)
    tangent(10 * size, 10 * size, False)
    text.right(90)
    text.forward(40 * size)
    text.right(90)
    text.forward(50 * size)
    text.backward(50 * size)
    text.left(90)
    text.forward(40 * size)
    text.right(90)
    tangent(10 * size, 10 * size, True)
    text.right(180)
    text.forward(40 * size)
    text.right(90)
    text.forward(100 * size)
    text.backward(100 * size)
    text.right(90)
    text.penup()
    text.forward(50 * size)
    text.pendown()
    letter_reset(size)


def c(size):
    text.forward(50 * size)
    text.backward(50 * size)
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.forward(50 * size)
    letter_reset(size)


def d(size):
    text.forward(40 * size)
    tangent(10 * size, 10 * size, False)
    text.right(90)
    text.forward(80 * size)
    tangent(-10 * size, 10 * size, False)
    text.backward(40 * size)
    text.left(90)
    text.forward(100 * size)
    text.backward(100 * size)
    text.right(90)
    text.forward(40 * size)
    text.penup()
    text.forward(10 * size)
    text.pendown()
    letter_reset(size)


def e(size):
    text.forward(50 * size)
    text.backward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.backward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    letter_reset(size)


def f(size):
    text.forward(50 * size)
    text.backward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.backward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.penup()
    text.forward(50 * size)
    text.pendown()
    letter_reset(size)


def g(size):
    text.forward(50 * size)
    text.backward(50 * size)
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(25 * size)
    text.left(90)
    text.penup()
    text.forward(50 * size)
    text.left(90)
    text.pendown()
    text.forward(25 * size)
    letter_reset(size)


def lh(size):
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.backward(100 * size)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.left(90)
    text.penup()
    text.forward(50 * size)
    text.pendown()
    letter_reset(size)


def letter_i(size):
    text.forward(50 * size)
    text.backward(25 * size)
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.backward(25 * size)
    text.forward(50 * size)
    letter_reset(size)


def j(size):
    text.forward(50 * size)
    text.backward(25 * size)
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.backward(25 * size)
    text.right(90)
    text.backward(25 * size)
    text.forward(25 * size)
    text.left(90)
    text.penup()
    text.forward(50 * size)
    text.pendown()
    letter_reset(size)


def k(size):
    text.right(90)
    text.forward(100 * size)
    text.backward(50 * size)
    text.left(90)
    text.forward(10 * size)
    tangent(50 * size, 40 * size, False)
    text.left(90)
    text.penup()
    text.forward(100 * size)
    text.pendown()
    tangent(50 * size, -40 * size, False)
    text.penup()
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(40 * size)
    text.pendown()
    letter_reset(size)


def letter_l(size):
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.forward(50 * size)
    letter_reset(size)


def o(size):
    text.forward(50 * size)
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.backward(50 * size)
    text.right(90)
    text.backward(100 * size)
    text.forward(100 * size)
    text.left(90)
    text.forward(50 * size)
    letter_reset(size)


def m(size):
    text.right(90)
    text.forward(100 * size)
    text.backward(100 * size)
    tangent(50 * size, 25 * size, False)
    text.penup()
    text.left(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(25 * size)
    text.pendown()
    text.right(90)
    text.forward(100 * size)
    text.backward(100 * size)
    tangent(50 * size, -25 * size, False)
    text.penup()
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(25 * size)
    text.pendown()
    letter_reset(size)


def n(size):
    text.right(90)
    text.forward(100 * size)
    text.backward(100 * size)
    tangent(100 * size, 50 * size, False)
    text.left(90)
    text.forward(100 * size)
    text.backward(100 * size)
    text.right(90)
    letter_reset(size)


def p(size):
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.backward(50 * size)
    text.forward(100 * size)
    text.left(90)
    text.penup()
    text.forward(50 * size)
    text.pendown()
    letter_reset(size)


def q(size):
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.right(90)
    text.backward(50 * size)
    text.forward(50 * size)
    text.right(90)
    text.forward(100 * size)
    letter_reset(size)


def r(size):
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.backward(50 * size)
    text.forward(100 * size)
    text.backward(50 * size)
    tangent(50 * size, 50 * size, False)
    letter_reset(size)


def s(size):
    text.forward(50 * size)
    text.backward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.backward(50 * size)
    text.forward(50 * size)
    letter_reset(size)


def t(size):
    text.forward(50 * size)
    text.backward(25 * size)
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.penup()
    text.forward(25 * size)
    text.pendown()
    letter_reset(size)


def u(size):
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(100 * size)
    text.backward(100 * size)
    text.right(90)
    letter_reset(size)


def v(size):
    tangent(100 * size, 25 * size, False)
    text.left(90)
    text.penup()
    text.forward(100 * size)
    text.right(90)
    text.forward(25 * size)
    text.pendown()
    tangent(100 * size, -25 * size, False)
    text.penup()
    text.forward(25 * size)
    text.pendown()
    letter_reset(size)


def lw(size):
    tangent(100 * size, 12.5 * size, False)
    text.penup()
    text.left(90)
    text.forward(100 * size)
    text.right(90)
    text.forward(12.5 * size)
    text.pendown()
    tangent(100 * size, -12.5 * size, False)
    text.penup()
    text.left(90)
    text.forward(100 * size)
    text.right(90)
    text.forward(12.5 * size)
    text.pendown()
    tangent(100 * size, 12.5 * size, False)
    text.penup()
    text.left(90)
    text.forward(100 * size)
    text.right(90)
    text.forward(12.5 * size)
    text.pendown()
    tangent(100 * size, -12.5 * size, False)
    text.penup()
    text.forward(12.5 * size)
    text.pendown()
    letter_reset(size)


def lx(size):
    tangent(100 * size, 50 * size, False)
    text.penup()
    text.left(90)
    text.forward(100 * size)
    text.pendown()
    tangent(100 * size, -50 * size, False)
    text.penup()
    text.forward(50 * size)
    text.pendown()
    letter_reset(size)


def ly(size):
    tangent(40 * size, 25 * size, False)
    text.penup()
    text.left(90)
    text.forward(40 * size)
    text.right(90)
    text.forward(25 * size)
    text.pendown()
    tangent(40 * size, -25 * size, False)
    text.right(90)
    text.forward(60 * size)
    text.left(90)
    text.penup()
    text.forward(25 * size)
    text.pendown()
    letter_reset(size)


def z(size):
    text.forward(50 * size)
    tangent(100 * size, -50 * size, False)
    text.forward(50 * size)
    letter_reset(size)


def num_1(size):
    text.forward(25 * size)
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.backward(25 * size)
    text.forward(50 * size)
    letter_reset(size)


def num_2(size):
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    letter_reset(size)


def num_3(size):
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.backward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.backward(50 * size)
    text.left(180)
    letter_reset(size)


def num_4(size):
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.right(90)
    text.backward(50 * size)
    text.forward(100 * size)
    text.left(90)
    letter_reset(size)


def num_5(size):
    text.forward(50 * size)
    text.backward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.backward(50 * size)
    text.forward(50 * size)
    letter_reset(size)


def num_6(size):
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    text.left(90)
    text.forward(50 * size)
    letter_reset(size)


def num_7(size):
    text.forward(50 * size)
    text.right(90)
    text.forward(100 * size)
    text.left(90)
    letter_reset(size)


def num_8(size):
    text.forward(50 * size)
    text.right(90)
    text.forward(100 * size)
    text.right(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(100 * size)
    text.backward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    letter_reset(size)


def num_9(size):
    for _ in range(5):
        text.forward(50 * size)
        text.right(90)
    text.forward(100 * size)
    text.left(90)
    letter_reset(size)


def num_0(size):
    text.forward(50 * size)
    text.right(90)
    text.forward(100 * size)
    text.right(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(100 * size)
    text.backward(50 * size)
    text.right(90)
    text.penup()
    text.forward(22.5 * size)
    text.pendown()
    text.begin_fill()
    for _ in range(4):
        text.forward(5 * size)
        text.right(90)
    text.end_fill()
    text.penup()
    text.forward(25 * size)
    text.right(90)
    text.forward(50 * size)
    text.left(90)
    text.pendown()
    letter_reset(size)


def space(size):
    text.penup()
    text.forward(70 * size)
    text.pendown()
    if debug:
        position = text.pos()
        print(position)


def undo():
    text.right(90)
    text.color('white')
    text.begin_fill()
    text.forward(110)
    text.right(90)
    text.forward(70)
    text.right(90)
    text.forward(110)
    text.end_fill()
    text.color('black')
    text.setheading(0)
    text.penup()
    current_x = text.xcor()
    current_line_y = text.ycor()
    new_line_y = current_line_y + 120
    if current_x < -351:
        text.goto(350, new_line_y)
    if new_line_y > 301:
        text.sety(300)
    text.pendown()
    if debug:
        position = text.pos()
        print(position)


def tangent(tangent_height, tangent_width, custom_angle):
    if not custom_angle:
        text.setheading(270)
    angle = atan(tangent_width / tangent_height)
    angle = angle * 57.295779513082321578272654463367
    text.left(angle)
    if debug:
        print(angle)
    length = tangent_height * tangent_height + tangent_width * tangent_width
    length = sqrt(length)
    text.forward(length)
    if debug:
        print(length)
    text.setheading(0)


def period(size):
    text.penup()
    text.backward(15 * size)
    text.right(90)
    text.forward(90 * size)
    text.pendown()
    text.begin_fill()
    text.forward(10 * size)
    text.left(90)
    text.forward(10 * size)
    text.left(90)
    text.forward(10 * size)
    text.left(90)
    text.forward(10 * size)
    text.right(90)
    text.end_fill()
    text.penup()
    text.forward(90 * size)
    text.right(90)
    text.forward(15 * size)
    text.pendown()


def comma(size):
    text.penup()
    text.backward(15 * size)
    text.right(90)
    text.forward(95 * size)
    text.pendown()
    text.begin_fill()
    text.forward(10 * size)
    text.left(90)
    text.forward(5 * size)
    text.left(90)
    text.forward(10 * size)
    text.left(90)
    text.forward(5 * size)
    text.right(90)
    text.end_fill()
    text.penup()
    text.forward(95 * size)
    text.right(90)
    text.forward(15 * size)
    text.pendown()


def apostrophe(size):
    text.penup()
    text.backward(5 * size)
    text.pendown()
    text.begin_fill()
    text.right(90)
    text.forward(10 * size)
    text.right(90)
    text.forward(5 * size)
    text.right(90)
    text.forward(10 * size)
    text.right(90)
    text.forward(5 * size)
    text.end_fill()
    text.penup()
    text.forward(5 * size)
    text.pendown()


def quote(size):
    text.penup()
    text.backward(5 * size)
    text.pendown()
    text.begin_fill()
    text.right(90)
    text.forward(10 * size)
    text.right(90)
    text.forward(5 * size)
    text.right(90)
    text.forward(10 * size)
    text.right(90)
    text.forward(5 * size)
    text.end_fill()
    text.penup()
    text.backward(2 * size)
    text.pendown()
    text.penup()
    text.backward(5 * size)
    text.pendown()
    text.begin_fill()
    text.right(90)
    text.forward(10 * size)
    text.right(90)
    text.forward(5 * size)
    text.right(90)
    text.forward(10 * size)
    text.right(90)
    text.forward(5 * size)
    text.end_fill()
    text.penup()
    text.forward(12 * size)
    text.pendown()


def question(size):
    text.forward(50 * size)
    text.right(90)
    text.forward(50 * size)
    text.right(90)
    text.forward(25 * size)
    text.left(90)
    text.forward(40 * size)
    text.penup()
    text.forward(5 * size)
    text.pendown()
    text.pensize(5 * size)
    text.forward(5 * size)
    text.pensize(1)
    text.penup()
    text.left(90)
    text.forward(25 * size)
    text.pendown()
    letter_reset(size)


def exclamation(size):
    text.penup()
    text.forward(25 * size)
    text.pendown()
    text.right(90)
    text.forward(90 * size)
    text.penup()
    text.forward(5 * size)
    text.pendown()
    text.pensize(5)
    text.forward(5 * size)
    text.pensize(1)
    text.left(90)
    text.penup()
    text.forward(25 * size)
    text.pendown()
    letter_reset(size)


def colon(size):
    text.penup()
    text.backward(15 * size)
    text.right(90)
    text.forward(90 * size)
    text.pendown()
    text.begin_fill()
    text.forward(10 * size)
    text.left(90)
    text.forward(10 * size)
    text.left(90)
    text.forward(10 * size)
    text.left(90)
    text.forward(10 * size)
    text.right(90)
    text.end_fill()
    text.penup()
    text.forward(80 * size)
    text.right(90)
    text.pendown()
    text.begin_fill()
    text.forward(10 * size)
    text.left(90)
    text.forward(10 * size)
    text.left(90)
    text.forward(10 * size)
    text.left(90)
    text.forward(10 * size)
    text.right(90)
    text.end_fill()
    text.penup()
    text.right(180)
    text.forward(10 * size)
    text.left(90)
    text.forward(10 * size)
    text.right(90)
    text.forward(10 * size)
    text.pendown()


prep_assets()
draw_screen()
turtle.onkeypress(draw_screen, 'space')
turtle.listen()
turtle.mainloop()
