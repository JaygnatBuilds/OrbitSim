from tkinter import Canvas, Tk, ttk


WIDTH, HEIGHT = 1200, 675


class OrbitSimulation:
    def __init__(self,root):
        self.root = root
        self.root.title("Orbit Simulation - github.com/JustinGnatiuk")
        self.canvas = None
        self.orbit_manager = None

        self.build_gui()

    def build_gui(self):
        content = ttk.Frame(self.root)

        self.canvas = Canvas(content, width=WIDTH, height=HEIGHT, bg="black")

    def start(self):
        if self.canvas is None:
            raise ValueError("orbitSim requires a Canvas to run orbital simulation")



if __name__ == "__main__":
    print("Welcome to orbitSim")

    root = Tk()
    orbit_sim = OrbitSimulation(root)
    orbit_sim.start()
    root.mainloop()

    print("Exiting orbitSim")
