import math
from tkinter import Canvas, messagebox

# Astronomical Units ( converted to meters )
AU = 149.6e6 * 1000
# Gravitational Constant
G = 6.67428e-11
# Scale factor
SCALE = 250 / AU # 1 AU = 100 pixels
# 1 day time step
TIMESTEP = 3600*24

class Vector2:
    def __init__(self, x, y) -> None:
        self.x, self.y = x, y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self,other) -> bool:
        return not self.__eq__(other)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def distance_to(self, other):
        return math.sqrt((other.x - self.x) ** 2, (other.y - self.y) ** 2)



class CelestialObject:
    def __init__(self, 
                origin: Vector2, 
                canvas: Canvas, 
                radius: int,
                mass: int, 
                tag: str,
                ) -> None:
        self.center = Vector2(origin.x, origin.y)
        self.canvas = canvas
        self.radius = radius
        self.mass = mass
        self.velocity = Vector2(0,0)
        self.orbit = [self.center]
        self.sun = False
        self.distance_to_sun = 0
        self.color = "white"
        self.tag = tag

    def draw(self):
        x1 = self.center.x - self.radius
        y1 = self.center.y - self.radius
        x2 = self.center.x + self.radius
        y2 = self.center.y + self.radius
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", outline=self.color)

    def attraction(self, other):

        # calculate distance between 2 objects
        distance_x = other.center.x - self.center.x
        distance_y = other.center.y - self.center.y
        distance = self.center.distance_to(other.center)

        # if other is sun, calculate distance to sun
        if( other.sun ):
            self.distance_to_sun = distance

        force = ( G * self.mass * other.mass ) / distance ** 2
        theta = math.atan2(distance_x, distance_y)
        force_x = math.cos(theta) * force
        forcy_y = math.sin(theta) * force

        return force_x, force_y

    # Sum force of attraction between current object and all other celestial objects
    def update_position(self, planets):

        total_force_x = total_force_y = 0

        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_force_x += fx
            total_force_y += fy

        self.velocity += Vector2(total_force_x, total_force_y) / self.mass * TIMESTEP

        self.center += self.velocity * TIMESTEP
        self.orbit.append(self.center)

class ObjectManager:
    def __init__(self, canvas: Canvas, config: list) -> None:
        self.canvas = canvas
        self.celestialObjects = []
        self.config = config

        self.canvas.bind("<Button-1>", self.spawn_object)

    # Spawn Celestial Object ( a Circle )
    def spawn_object(self, event):
        
        # Grab config info from config entries
        mass = self.config[0].get()
        tag = self.config[1].get()
        
        if(mass == ""):
            messagebox.showerror("Error", "Object must have mass.") 
            return
        if(tag == ""):
            messagebox.showerror("Error","Object must have a tag (Name)")
            return

        new_object = CelestialObject(
            Vector2(event.x, event.y), 
            self.canvas,
            10,
            mass,
            tag
        )
        self.celestialObjects.append(new_object)
        new_object.draw()

    def spawn_sun(self, width, height):
        
        # mass of the sun
        mass = 1.98892 * 10**30

        # calculate center of canvas
        x = width // 2
        y = height // 2

        new_object = CelestialObject(
            Vector2(x, y),
            self.canvas,
            20,
            mass,
            "Sun"
        )
        new_object.sun = True
        new_object.distance_to_sun = 0

        self.celestialObjects.append(new_object)

    def update_objects(self):

        for planet in celestialObjects:
            planet.update_position(self.celestialObjects)
            planet.draw()
