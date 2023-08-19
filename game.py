import pygame as pg
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import os

from button import Button
from pygame.locals import QUIT, KEYDOWN, K_q

screenWidth = 1280
screenHeight = 720
aspectRatio = screenWidth/screenHeight


def get_font(size):
    return pg.font.Font(os.path.join(os.path.dirname(__file__),"assets/font.ttf"), size)


class App:

    def __init__(self):

        pg.init()
        pg.display.set_mode((screenWidth, screenHeight),
                            pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        self.quit_button = Button(image=pg.image.load(os.path.join(os.path.dirname(__file__),"assets/Play Rect.png")), pos=(640, 650),
                                  text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")

        # initialize screen

        glClearColor(0.0, 0.0, 0.0, 0)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.shader = self.createShader(os.path.join(os.path.dirname(
            __file__), "shaders/vertex.txt"), os.path.join(os.path.dirname(__file__), "shaders/fragment.txt"))
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        # cube object for position and rotation
        self.cube = Cube(
            position=[0, 0, -3],
            eulers=[0, 0, 0]
        )

        self.cube_mesh = CubeMesh()

        # matrix for projected view
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=screenWidth/screenHeight,
            near=0.1, far=10, dtype=np.float32
        )

        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
        )
        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")

        self.mainLoop()

    def mainLoop(self):

        running = True

        while running:
            for event in pg.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_q:  # Check for "Q" key press
                        running = False

                # Handle button events
                self.quit_button.handle_event(event)
            # clear screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)

            # updating rotation

            # about X-axis
            self.cube.eulers[0] += 0.25
            if self.cube.eulers[0] > 360:
                self.cube.eulers[0] -= 360

            # about Y-axis
            self.cube.eulers[2] += 0.25
            if self.cube.eulers[2] > 360:
                self.cube.eulers[2] -= 360
            # about Z-axis
            self.cube.eulers[1] += 0.25
            if self.cube.eulers[1] > 360:
                self.cube.eulers[1] -= 360

            # rotation
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.cube.eulers),
                    dtype=np.float32
                )
            )

            # updating translation

            # along X-axis
            self.cube.position[0] += self.cube.xDirection*0.005
            if self.cube.position[0] > 0.95*aspectRatio:
                self.cube.xDirection = -1
            if self.cube.position[0] < -0.95*aspectRatio:
                self.cube.xDirection = 1
            # along Y-axis
            self.cube.position[1] += self.cube.yDirection*0.005
            if self.cube.position[1] > 0.85:
                self.cube.yDirection = -1
            if self.cube.position[1] < -0.85:
                self.cube.yDirection = 1

            # sending it to its position
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=self.cube.position,
                    dtype=np.float32
                )
            )

            glUniformMatrix4fv(self.modelMatrixLocation, 1,
                               GL_FALSE, model_transform)

            # actually drawing the cube
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)

            pg.display.flip()

            self.clock.tick(60)

        self.quit()

    def createShader(self, vertexFilepath, fragmentFilepath):
        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))

        return shader

    def quit(self):

        self.cube_mesh.destroy()
        glDeleteProgram(self.shader)
        pg.quit()


class Cube:

    def __init__(self, position, eulers) -> None:
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
        self.xDirection = 1
        self.yDirection = 1
        self.zDirection = 1


class CubeMesh:

    def __init__(self):

        # x,y,z,R,G,B
        self.vertices = (
            # front face
            -0.3, -0.3, -0.3, 1.0, 1.0, 0.0,  # BottomLeftFront yellow
            0.3, -0.3, -0.3, 0.0, 1.0, 1.0,  # BottomRightFront cyan
            0.3,  0.3, -0.3, 0.0, 0.0, 1.0,  # TopRightFront blue

            0.3,  0.3, -0.3, 0.0, 0.0, 1.0,  # TopRightFront blue
            -0.3,  0.3, -0.3, 0.0, 1.0, 0.0,  # TopLeftFront green
            -0.3, -0.3, -0.3, 1.0, 1.0, 0.0,  # BottomLeftFront yellow

            # left face
            -0.3, -0.3, -0.3, 1.0, 1.0, 0.0,  # BottomLeftFront yellow
            -0.3, -0.3, 0.3, 0.0, 1.0, 1.0,  # BottomLeftBack cyan
            -0.3,  0.3, 0.3, 0.0, 0.0, 1.0,  # TopLeftBack blue

            -0.3,  0.3, 0.3, 0.0, 0.0, 1.0,  # TopLeftBack blue
            -0.3,  0.3, -0.3, 0.0, 1.0, 0.0,  # TopLeftFront green
            -0.3, -0.3, -0.3, 1.0, 1.0, 0.0,  # BottomLeftFront yellow

            # back face
            -0.3, -0.3, 0.3, 0.0, 1.0, 1.0,  # BottomLeftBack cyan
            0.3, -0.3, 0.3, 1.0, 1.0, 0.0,  # BottomRightBack yellow
            0.3,  0.3, 0.3, 0.0, 1.0, 0.0,  # TopRightBack green

            0.3,  0.3, 0.3, 0.0, 1.0, 0.0,  # TopRightBack green
            -0.3,  0.3, 0.3, 0.0, 0.0, 1.0,  # TopLeftBack blue
            -0.3, -0.3, 0.3, 0.0, 1.0, 1.0,  # BottomLeftBack cyan

            # right face

            0.3, -0.3, -0.3, 0.0, 1.0, 1.0,  # BottomRightFront cyan
            0.3, -0.3, 0.3, 1.0, 1.0, 0.0,  # BottomRightBack yellow
            0.3,  0.3, 0.3, 0.0, 1.0, 0.0,  # TopRightBack green

            0.3,  0.3, 0.3, 0.0, 1.0, 0.0,  # TopRightBack green
            0.3,  0.3, -0.3, 0.0, 0.0, 1.0,  # TopRightFront blue
            0.3, -0.3, -0.3, 0.0, 1.0, 1.0,  # BottomRightFront cyan

            # top face
            0.3,  0.3, -0.3, 0.0, 1.0, 1.0,  # TopRightFront cyan
            0.3,  0.3, 0.3, 0.0, 1.0, 1.0,  # TopRightBack cyan
            -0.3,  0.3, -0.3, 0.0, 1.0, 1.0,  # TopLeftFront cyan

            -0.3,  0.3, -0.3, 0.0, 1.0, 1.0,  # TopLeftFront cyan
            -0.3,  0.3, 0.3, 0.0, 1.0, 1.0,  # TopLeftBack cyan
            0.3,  0.3, 0.3, 0.0, 1.0, 1.0,  # TopRightBack cyan

            # bottom face
            0.3, -0.3, -0.3, 0.0, 1.0, 1.0,  # BottomRightFront cyan
            0.3, -0.3, 0.3, 0.0, 1.0, 1.0,  # BottomRightBack cyan
            -0.3, -0.3, -0.3, 0.0, 1.0, 1.0,  # BottomLeftFront cyan

            -0.3, -0.3, -0.3, 0.0, 1.0, 1.0,  # BottomLeftFront cyan
            -0.3, -0.3, 0.3, 0.0, 1.0, 1.0,  # BottomLeftBack cyan
            0.3, -0.3, 0.3, 0.0, 1.0, 1.0,  # BottomRightBack cyan


        )

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = len(self.vertices)//6
        self.vao = glGenVertexArrays(1)  # vertex array object
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)  # vertex buffer object
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes,
                     self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)  # position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)  # color
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                              24, ctypes.c_void_p(12))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


# if __name__ == "__main__":
    # myApp = App()
