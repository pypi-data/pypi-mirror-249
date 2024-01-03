import sys
import random
import tkinter as tk
from tkinter import messagebox
import turtle


turtle = turtle


class Ruptured:
    def __init__(self):
        self.key_bindings = {}
        self.game_running = True
        self.sprites = []

    def write(self, value):
        print(value)

    def ask(self, value):
        user = input(value)
        return user

    def rad(self, value):
        return random.randint(0, value)

    def window_title(self, title):
        self.window.title(title)
        return

    def window_size(self, x, y):
        self.window.geometry(f"{x}x{y}")
        return

    def window_text(self, text):
        text_message = tk.Message(self.window, text=text, width=300)
        text_message.pack(pady=20)

    def window_header(self, hdr):
        text_label = tk.Label(self.window, text=hdr, wraplength=300)
        text_label.pack(pady=20)

    def start(self):
        self.window.mainloop()

    def key_selceted(self, key, callback, sprite):
        if sprite is not None:
           self.key_bindings[key] = (sprite, callback)
        else:
            self.key_bindings[key] = callback 

    def key_down(self, event):
        key = event.char.lower()
        if key in self.key_bindings:
            callback = self.key_bindings[key]
            callback()
        elif key in self.key_bindings:
            callback - self.key_bindings
            callback()
        else:
            print(f"Unknown key pressed: {key}")
    def size(self, value):
        length = len(value)
        return length

    def draw_window(self):
        self.screen = turtle.Screen()
        self.screen

    def create_brush(self):
        self.turtle = turtle.Turtle()
        return

    def brush_left(self, value):
        self.turtle.left(value)
        return

    def brush_right(self, value):
        self.turtle.right(value)
        return

    def brush_forward(self, value):
        self.turtle.forward(value)
        return

    def brush_backward(self, value):
        self.turtle.forward(value)
        return

    def draw_close(self):
        self.screen.exitonclick()

    def color(self, color):
        self.turtle.color(color)
        return

    def draw_speed(self, speed):
        self.turtle.speed(speed)

    def window(self):
        self.window = tk.Tk()

    def hide_brush(self):
        self.turtle.hideturtle()

    def set_position(self, x, y):
        self.turtle.goto(x, y)

    def brush_up(self):
        self.turtle.penup()

    def brush_down(self):
        self.turtle.penup()

    def draw_shape(self, shape):
        self.turtle.shape(shape)

    def fill_color(self, color):
        self.turtle.fillcolor(color)

    def draw_dot(self):
        self.turtle.dot()

    def stamp_brush(self):
        self.turtle.stamp()

    def draw_finish(self):
        self.turtle.done()

    def window_background(self, color):
        self.window.configure(background=color)

    def window_button(self, text, command):
        button = tk.Button(self.window, text=text, command=command)
        button.pack(pady=10)
        return button

    def window_entry(self):
        entry = tk.Entry(self.window)
        entry.pack(pady=10)
        return entry

    def window_popup(title, message):
        messagebox.showinfo(title, message)

    def value_type(self, value):
        vt = type(value)
        return vt

    def convert(self, value, contype):
        con = contype(value)
        return con

    def draw_circle(self, radius):
        if self.turtle:
            self.turtle.circle(radius)
        else:
            print('\033Error: Brush not found\033')

    def draw_square(self, side_length):
        if self.turtle:
            for _ in range(4):
                self.turtle.forward(side_length)
                self.turtle.left(90)
        else:
            print('\033Error: Brush not found\033')

    def draw_triangle(self, side_length):
        if self.turtle:
            for _ in range(3):
                self.turtle.forward(side_length)
                self.turtle.left(120)
        else:
            print('\033Error: Brush not found\033')

    def draw_star(self, size):
        if self.turtle:
            for _ in range(5):
                self.turtle.forward(size)
                self.turtle.right(144)
        else:
            print('\033Error: Brush not found\033')

    def brush_barchart(self, data):
        bar_width = 20
        for value in data:
            self.turtle.begin_fill()
            self.turtle.forward(bar_width)
            self.turtle.left(90)
            self.turtle.forward(value)
            self.turtle.left(90)
            self.turtle.forward(bar_width)
            self.turtle.left(90)
            self.turtle.forward(value)
            self.turtle.left(90)
            self.turtle.end_fill()
            self.turtle.forward(bar_width)

    def brush_scatterplot(self, points):
        for x, y in points:
            self.turtle.penup()
            self.turtle.goto(x, y)
            self.turtle.dot(5)

    def brush_linechart(self, values):
        self.turtle.penup()
        x, y = -150, -150
        for value in values:
            self.turtle.goto(x, y)
            self.turtle.pendown()
            self.turtle.goto(x, y + value)
            x += 30

    def brush_clear(self):
        self.turtle.clear()

    def brush_reset(self):
        self.turtle.reset()

    def brush_size(self, size):
        self.turtle.pensize(size)

    def brush_bgcolor(self, color):
        self.screen.bgcolor(color)

    def draw_polygon(self, sides, length):
        if self.turtle:
            angle = 360 / sides
            for _ in range(sides):
                self.turtle.forward(length)
                self.turtle.left(angle)
        else:
            print('\033Error: Brush not found\033')

    def draw_text(self, text, font=("Arial", 12, "normal")):
        if self.turtle:
            self.turtle.write(text, font=font)
        else:
            print('\033Error: Brush not found\033')

    def draw_arc(self, radius, extent):
        if self.turtle:
            self.turtle.circle(radius, extent=extent)
        else:
            print('\033Error: Brush not found\033')

    def draw_rectcolor(self, width, height, color):
        if self.turtle:
            self.turtle.begin_fill()
            self.turtle.color(color)
            for _ in range(2):
                self.turtle.forward(width)
                self.turtle.left(90)
                self.turtle.forward(height)
                self.turtle.left(90)
            self.turtle.end_fill()
        else:
            print('\033Error: Brush not found\033')

    def draw_image(self, filename):
        if self.turtle:
            self.screen.addshape(filename)
            self.turtle.shape(filename)
        else:
            print('\033Error: Brush not found\033')

    def draw_tricolor(self, side_length, color="yellow"):
        if self.turtle:
            self.turtle.begin_fill()
            self.turtle.color(color)
            for _ in range(3):
                self.turtle.forward(side_length)
                self.turtle.left(120)
            self.turtle.end_fill()
        else:
            print('\033Error: Brush not found\033')

    def brush_character(self, filename, x=0, y=0,):
        sprite = turtle.Turtle()
        sprite.penup()
        sprite.shape(filename)
        sprite.goto(x, y)
        self.sprites.append(sprite)

        return sprite
    
    def relocate_character(self, sprite, dx, dy):
        x, y = sprite.position()
        sprite.setposition(x + dx, y + dy)

    def hide_character(self, sprite):
        sprite.hideturtle()

    def show_character(self, sprite):
        sprite.showturtle()
    
    def character_collision(self, sprite1, sprite2):
        x1, y1 = sprite1.position()
        x2, y2 = sprite2.position()
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return distance < 20 
    
    def character_up(self, sprite):
        self.relocate_charactera(sprite, 0, 10)

    def character_down(self, sprite):
        self.relocate_character(sprite, 0, -10)

    def character_left(self, sprite):
        self.relocate_character(sprite, -10, 0)

    def character_right(self, sprite):
        self.relocate_character(sprite, 10, 0)

    def detect_collision(self, sprite_type, callback):
        player = next((sprite for sprite in self.sprites if sprite.shape() == "turtle"), None)
        if player:
            for item in self.sprites:
                if item.shape() == sprite_type and self.is_collision(player, item):
                    callback(item)
                    self.sprites.remove(item)
                    self.spawn_items()

    def window_keepinscreen(self, sprite):
        x, y = sprite.position()
        screen_width = self.screen.window_width() / 2
        screen_height = self.screen.window_height() / 2
        new_x = max(-screen_width, min(x, screen_width))
        new_y = max(-screen_height, min(y, screen_height))
        sprite.goto(new_x, new_y)

    def follow_sprite(self, follower, target, speed):
        follower.setheading(follower.towards(target))
        follower.forward(speed)   

    def end(self):
       self.game_running = False
       sys.exit()

    def window_end(self):
        self.game_running = False
        self.screen.bye()


