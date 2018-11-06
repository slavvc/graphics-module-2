from PIL import ImageTk
import tkinter as tk
import tkinter.filedialog
import lib
import numpy as np

size = (400, 400)


class Main:
    def __init__(self, root):
        self.root = root
        
        self.ui_list = [
            'lab6',
            'graphic',
            'save-load',
            'screw'
        ]

        self.polyhedron = lib.Polyhedron.Cube(lib.Point(0, 0, 0), 100)
        self.camera = lib.Camera.ortho()
        self.transform = lib.Transform.identity()

        self.current = 3

        self.menu_var = tk.StringVar()
        self.menu_var.set(self.ui_list[self.current])
        self.menu = tk.OptionMenu(root, self.menu_var, *self.ui_list)
        self.menu.grid(row=0, column=0)

        self.frames = [Lab6(root),
                       Graphic(root),
                       SaveLoad(root),
                       Screw(root)]
        self.frames[self.current].grid(row=1, column=0)

        self.menu_var.trace("w", self.change_menu)

    def change_menu(self, *args):
        tr = self.menu_var.get()
        idx = self.ui_list.index(tr)
        self.frames[self.current].grid_forget()
        fr = self.frames[idx]
        fr.grid(row=1, column=0)
        self.current = idx


class Graphic(tk.Frame):
    def __init__(self, root):
        super().__init__(root)


class SaveLoad(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.open = tk.Button(self, text="open", command=self.open_file).grid(row=1, column=0)
        self.save = tk.Button(self, text="save", command=self.save_file).grid(row=1, column=1)
        
    def open_file(self):
        filename = tk.filedialog.askopenfilename()
        self.polyhedron = lib.Polyhedron.load_obj(filename)

    def save_file(self):
        filename = tk.filedialog.asksaveasfilename()
        self.polyhedron1.save_obj(filename)


class Screw(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.canvas_width = 500
        self.canvas_height = 400

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.grid(row=0, column=0)

        self.canvas.bind("<Button-1>", self.make_point)
        self.points = []

        self.axis_var = tk.StringVar()
        self.axis = tk.OptionMenu(self, self.axis_var, 'OX', 'OY', 'OZ')
        self.axis.grid(row=0, column=1)
        self.axis_var.set("OX")
        self.axis_var.trace('w', self.change_axis)

        self.clear_button = tk.Button(self, text="clear", command=self.clear)
        self.clear_button.grid(row=0, column=2)

        self.canvas_draw()

    def clear(self):
        self.points = []
        self.canvas_draw()

    def make_point(self, event):
        if (event.x >= 0) and (event.x < self.canvas_width) and (event.y >= 0) and (event.y < self.canvas_height):
            self.points.append((event.x, event.y))
            self.canvas_draw()

    def change_axis(self, *args):
        pass

    def canvas_draw(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_line(self.canvas_width / 2, 0, self.canvas_width / 2, self.canvas_height, fill='red')
        self.canvas.create_line(0, self.canvas_height / 2, self.canvas_width, self.canvas_height / 2, fill='red')
        for i in range(len(self.points) - 1):
            self.canvas.create_line(self.points[i], self.points[i + 1])

        for p in self.points:
            self.canvas.create_oval(p[0] - 1, p[1] - 1, p[0] + 1, p[1] + 1)


class Lab6(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.polyhedron = lib.Polyhedron.Cube(lib.Point(0, 0, 0), 100)
        self.camera = lib.Camera.ortho()
        self.transform = lib.Transform.identity()
        self.matrix_transform = lib.Transform.identity()
        self.choice_transform = lib.Transform.identity()

        self.camera_var = tk.IntVar()
        self.persp_k_var = tk.StringVar()
        self.iso_a_var = tk.StringVar()
        self.iso_b_var = tk.StringVar()
        self.object_var = tk.IntVar()
        self.radius_var = tk.StringVar()
        self.position_x_var = tk.StringVar()
        self.position_y_var = tk.StringVar()
        self.position_z_var = tk.StringVar()
        self.transform_mode_var = tk.IntVar()
        self.transform_choice_var = tk.StringVar()

        self.transform_choice_list = [
            'identity', 'translate', 'rotate',
            'scale', 'rotate_around_line', 'reflect'
        ]

        self.view = tk.Label(self, width=size[0], height=size[1])
        self.view.grid(row=0, column=0, rowspan=18)

        # Camera
        self.camera_var.trace('w', self.set_camera)
        tk.Label(self, text='Camera:').grid(row=0, column=1)
        tk.Radiobutton(
            self, text='ortho', variable=self.camera_var, value=0
        ).grid(row=1, column=2)

        tk.Radiobutton(
            self, text='persp', variable=self.camera_var, value=1
        ).grid(row=2, column=2)
        tk.Label(self, text='k:').grid(row=2, column=3)

        self.persp_k_var.trace('w', self.read_persp_k)
        tk.Entry(self, textvar=self.persp_k_var).grid(row=2, column=4)

        tk.Radiobutton(
            self, text='iso', variable=self.camera_var, value=2
        ).grid(row=3, column=2)
        tk.Label(self, text='a:').grid(row=3, column=3)

        self.iso_a_var.trace('w', self.read_iso_a_b)
        tk.Entry(self, textvar=self.iso_a_var).grid(row=3, column=4)
        tk.Label(self, text='b:').grid(row=3, column=5)

        self.iso_b_var.trace('w', self.read_iso_a_b)
        tk.Entry(self, textvar=self.iso_b_var).grid(row=3, column=6)

        # Object

        self.object_var.trace('w', self.set_object)
        tk.Label(self, text='Object:').grid(row=4, column=1)
        tk.Radiobutton(
            self, text='Cube', variable=self.object_var, value=0
        ).grid(row=5, column=2)
        tk.Radiobutton(
            self, text='Tetrahedron', variable=self.object_var, value=1
        ).grid(row=6, column=2)
        tk.Radiobutton(
            self, text='Octahedron', variable=self.object_var, value=2
        ).grid(row=7, column=2)

        self.radius_var.set(100)
        self.radius_var.trace('w', self.set_object)
        tk.Label(self, text='radius:').grid(row=4, column=3)
        tk.Entry(self, textvariable=self.radius_var).grid(row=4, column=4)

        # Position

        self.position_x_var.trace('w', self.set_object)
        self.position_y_var.trace('w', self.set_object)
        self.position_z_var.trace('w', self.set_object)
        self.position_x_var.set(0)
        self.position_y_var.set(20)
        self.position_z_var.set(0)
        tk.Label(self, text='Position:').grid(row=8, column=1)
        tk.Label(self, text='x:').grid(row=9, column=2)
        tk.Entry(self, textvariable=self.position_x_var).grid(row=9, column=3)
        tk.Label(self, text='y:').grid(row=9, column=4)
        tk.Entry(self, textvariable=self.position_y_var).grid(row=9, column=5)
        tk.Label(self, text='z:').grid(row=9, column=6)
        tk.Entry(self, textvariable=self.position_z_var).grid(row=9, column=7)

        # Transform
        tk.Label(self, text='Transform:').grid(row=10, column=1)

        self.transform_mode_var.trace('w', self.draw)
        tk.Radiobutton(
            self, text='Global', variable=self.transform_mode_var, value=0
        ).grid(row=10, column=2)
        tk.Radiobutton(
            self, text='Local', variable=self.transform_mode_var, value=1
        ).grid(row=10, column=3)
        # # Matrix
        tk.Label(self, text='Matrix:').grid(row=11, column=2)
        self.matrix_vars = []
        self.matrix_values = np.zeros((4, 4))
        for i in range(4):
            self.matrix_vars.append([])
            for j in range(4):
                self.matrix_vars[i].append(tk.StringVar())
                self.matrix_values[i][j] = (1 if i == j else 0)
                tk.Entry(self, textvar=self.matrix_vars[i][j]).grid(
                    row=12 + i, column=3 + j
                )
                self.matrix_vars[i][j].set(1 if i == j else 0)
                self.matrix_vars[i][j].trace('w', self.read_matrix)

        # # Choose
        self.transform_choice_var.set(self.transform_choice_list[0])
        self.transform_choice_current = 0
        tk.Label(self, text='Choose:').grid(row=16, column=2)
        tk.OptionMenu(self, self.transform_choice_var, *self.transform_choice_list) \
            .grid(row=16, column=3)

        # # # Choice frames
        self.transform_choice_frames = []
        self.transform_choice_var.trace('w', self.change_transform_choice)
        # # # # identity
        self.transform_choice_frames.append((tk.Frame(self), (1, 1)))
        tmp_fr = self.transform_choice_frames[-1][0]
        tk.Label(tmp_fr, text='No params here').grid(row=0, column=0)
        # # # # translate
        self.transform_choice_frames.append((tk.Frame(self), (1, 6)))
        tmp_fr = self.transform_choice_frames[-1][0]
        self.transform_choice_translate_vars = []
        self.transform_choice_translate_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='x:').grid(row=0, column=0)
        tk.Entry(tmp_fr, textvar=self.transform_choice_translate_vars[-1]) \
            .grid(row=0, column=1)
        self.transform_choice_translate_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='y:').grid(row=0, column=2)
        tk.Entry(tmp_fr, textvar=self.transform_choice_translate_vars[-1]) \
            .grid(row=0, column=3)
        self.transform_choice_translate_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='z:').grid(row=0, column=4)
        tk.Entry(tmp_fr, textvar=self.transform_choice_translate_vars[-1]) \
            .grid(row=0, column=5)
        for v in self.transform_choice_translate_vars:
            v.trace('w', self.read_transform_choice_translate)
        # # # # rotate
        self.transform_choice_frames.append((tk.Frame(self), (1, 4)))
        tmp_fr = self.transform_choice_frames[-1][0]
        self.transform_choice_rotate_vars = [tk.StringVar(), tk.StringVar()]
        tk.Label(tmp_fr, text='axis:').grid(row=0, column=0)
        tk.OptionMenu(tmp_fr, self.transform_choice_rotate_vars[0], 'x', 'y', 'z') \
            .grid(row=0, column=1)
        self.transform_choice_rotate_vars[0].set('x')
        tk.Label(tmp_fr, text="angle (radians):").grid(row=0, column=2)
        tk.Entry(tmp_fr, textvariable=self.transform_choice_rotate_vars[1]) \
            .grid(row=0, column=3)
        for v in self.transform_choice_rotate_vars:
            v.trace('w', self.read_transform_choice_rotate)
        # # # # scale
        self.transform_choice_frames.append((tk.Frame(self), (1, 6)))
        tmp_fr = self.transform_choice_frames[-1][0]
        self.transform_choice_scale_vars = []
        self.transform_choice_scale_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='sx:').grid(row=0, column=0)
        tk.Entry(tmp_fr, textvar=self.transform_choice_scale_vars[-1]) \
            .grid(row=0, column=1)
        self.transform_choice_scale_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='sy:').grid(row=0, column=2)
        tk.Entry(tmp_fr, textvar=self.transform_choice_scale_vars[-1]) \
            .grid(row=0, column=3)
        self.transform_choice_scale_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='sz:').grid(row=0, column=4)
        tk.Entry(tmp_fr, textvar=self.transform_choice_scale_vars[-1]) \
            .grid(row=0, column=5)
        for v in self.transform_choice_scale_vars:
            v.trace('w', self.read_transform_choice_scale)

        # # # # rotate_around_line
        self.transform_choice_frames.append((tk.Frame(self), (3, 6)))
        tmp_fr = self.transform_choice_frames[-1][0]

        self.transform_choice_line_rotate_vars = []
        self.transform_choice_line_rotate_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='x1:').grid(row=0, column=0)
        tk.Entry(tmp_fr, textvar=self.transform_choice_line_rotate_vars[-1]) \
            .grid(row=0, column=1)
        self.transform_choice_line_rotate_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='y1:').grid(row=0, column=2)
        tk.Entry(tmp_fr, textvar=self.transform_choice_line_rotate_vars[-1]) \
            .grid(row=0, column=3)
        self.transform_choice_line_rotate_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='z1:').grid(row=0, column=4)
        tk.Entry(tmp_fr, textvar=self.transform_choice_line_rotate_vars[-1]) \
            .grid(row=0, column=5)

        self.transform_choice_line_rotate_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='x2:').grid(row=1, column=0)
        tk.Entry(tmp_fr, textvar=self.transform_choice_line_rotate_vars[-1]) \
            .grid(row=1, column=1)
        self.transform_choice_line_rotate_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='y2:').grid(row=1, column=2)
        tk.Entry(tmp_fr, textvar=self.transform_choice_line_rotate_vars[-1]) \
            .grid(row=1, column=3)
        self.transform_choice_line_rotate_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='z2:').grid(row=1, column=4)
        tk.Entry(tmp_fr, textvar=self.transform_choice_line_rotate_vars[-1]) \
            .grid(row=1, column=5)

        # angle
        self.transform_choice_line_rotate_vars.append(tk.StringVar())
        tk.Label(tmp_fr, text='angle:').grid(row=2, column=0)
        tk.Entry(tmp_fr, textvar=self.transform_choice_line_rotate_vars[-1]) \
            .grid(row=2, column=1)

        for c in self.transform_choice_line_rotate_vars:
            c.trace("w", self.read_transform_choice_line_rotate)

        # # # # reflect
        self.transform_choice_frames.append((tk.Frame(self), (1, 2)))
        tmp_fr = self.transform_choice_frames[-1][0]
        tk.Label(tmp_fr, text='plane:').grid(row=0, column=0)
        self.transform_choice_reflect_var = tk.StringVar()
        tk.OptionMenu(tmp_fr, self.transform_choice_reflect_var, 'xy', 'xz', 'yz') \
            .grid(row=0, column=1)
        self.transform_choice_reflect_var.set('xy')
        self.transform_choice_reflect_var.trace('w', self.read_transform_choice_reflect)

        self.change_transform_choice()

        self.draw()

    def draw(self, *args):
        self.transform = self.matrix_transform.compose(self.choice_transform)
        if self.transform_mode_var.get() == 0:
            transformed = self.polyhedron.apply_transform(self.transform)
        else:
            transformed = self.polyhedron.apply_relative_transform(self.transform)
        self.im = self.camera.draw(size, transformed.points, transformed.sides)
        # self.im.show()
        self.pim = ImageTk.PhotoImage(self.im)
        self.view.configure(image=self.pim)

    def read_transform_choice_reflect(self, *args):
        plane = self.transform_choice_reflect_var.get()
        self.choice_transform = lib.Transform.reflect(plane)
        self.draw()

    def read_transform_choice_rotate(self, *args):
        ax = self.transform_choice_rotate_vars[0].get()
        try:
            angle = float(self.transform_choice_rotate_vars[1].get())
        except:
            angle = 0
        self.choice_transform = lib.Transform.rotate(ax, angle)
        self.draw()

    def read_transform_choice_translate(self, *args):
        xyz = []
        try:
            for i in range(3):
                xyz.append(float(self.transform_choice_translate_vars[i].get()))
        except:
            xyz = [0] * 3
        self.choice_transform = lib.Transform.translate(*xyz)
        self.draw()

    def read_transform_choice_scale(self, *args):
        xyz = []
        try:
            for i in range(3):
                xyz.append(float(self.transform_choice_scale_vars[i].get()))
        except:
            xyz = [1] * 3
        self.choice_transform = lib.Transform.scale(*xyz)
        self.draw()

    def read_transform_choice_line_rotate(self, *args):
        xyz1 = []
        xyz2 = []
        angle = 0.
        try:
            for i in range(3):
                xyz1.append(float(self.transform_choice_line_rotate_vars[i].get()))
            for i in range(3, 6):
                xyz2.append(float(self.transform_choice_line_rotate_vars[i].get()))
        except:
            xyz1 = [0, -1, 0]
            xyz2 = [0, 1, 0]

        try:
            angle = float(self.transform_choice_line_rotate_vars[-1].get())
        except:
            angle = 0.

        self.choice_transform = lib.Transform.rotate_around_line(lib.Line(xyz1, xyz2), angle)
        self.draw()

    def change_transform_choice(self, *args):
        tr = self.transform_choice_var.get()
        idx = self.transform_choice_list.index(tr)
        self.transform_choice_frames[self.transform_choice_current][0].grid_forget()
        fr, size = self.transform_choice_frames[idx]
        fr.grid(row=17, column=3, rowspan=size[0], columnspan=size[1])
        self.transform_choice_current = idx
        self.choice_transform = lib.Transform.identity()
        if idx == 1:
            self.read_transform_choice_translate()
        elif idx == 2:
            self.read_transform_choice_rotate()
        elif idx == 3:
            self.read_transform_choice_scale()
        elif idx == 4:
            self.read_transform_choice_line_rotate()
        elif idx == 5:
            self.read_transform_choice_reflect()

        self.draw()

    def read_matrix(self, *args):
        try:
            for i in range(4):
                for j in range(4):
                    self.matrix_values[i][j] = float(self.matrix_vars[i][j].get())
            self.matrix_transform = lib.Transform(self.matrix_values)
        except:
            self.matrix_transform = lib.Transform.identity()
        self.draw()

    def read_persp_k(self, *args):
        try:
            self.persp_k = float(self.persp_k_var.get())
        except:
            # self.persp_k_var.set("error")
            self.persp_k = 0.1
        if self.camera_var.get() == 1:
            self.camera = lib.Camera.persp(self.persp_k)
        self.draw()

    def read_iso_a_b(self, *args):
        try:
            self.iso_a = float(self.iso_a_var.get())
            self.iso_b = float(self.iso_b_var.get())
        except:
            if self.camera_var.get() == 2:
                self.camera = lib.Camera.iso()
        else:
            if self.camera_var.get() == 2:
                self.camera = lib.Camera.iso(self.iso_a, self.iso_b)
        self.draw()

    def set_camera(self, *args):
        c = self.camera_var.get()
        if c == 0:
            self.camera = lib.Camera.ortho()
        elif c == 1:
            self.read_persp_k()
        elif c == 2:
            self.read_iso_a_b()
        self.draw()

    def set_object(self, *args):
        o = self.object_var.get()
        try:
            self.radius = float(self.radius_var.get())
        except:
            self.radius = 10
        self.read_position()
        if o == 0:
            self.polyhedron = lib.Polyhedron.Cube(self.position, self.radius)
        elif o == 1:
            self.polyhedron = lib.Polyhedron.Tetrahedron(self.position, self.radius)
        elif o == 2:
            self.polyhedron = lib.Polyhedron.Octahedron(self.position, self.radius)
        self.draw()

    def read_position(self, *args):
        try:
            self.position_x = float(self.position_x_var.get())
            self.position_y = float(self.position_y_var.get())
            self.position_z = float(self.position_z_var.get())
        except:
            self.position_x = 0
            self.position_y = 0
            self.position_z = 0
        self.position = lib.Point(
            self.position_x,
            self.position_y,
            self.position_z
        )


def main():
    root = tk.Tk()
    m = Main(root)
    tk.mainloop()


if __name__ == '__main__':
    main()
