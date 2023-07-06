import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import ctypes
from warp import MatrixT


class App:
    def __init__(self):
        pg.init()
        self.width = 1280
        self.height = 720
        pg.display.set_mode((self.width, self.height),
                            pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption('Computación gráfica')
        self.clock = pg.time.Clock()

        glClearColor(0.0, 0.0, 0.0, 1)

        self.shader = self.createShader(
            "shaders/vertex.txt", "shaders/fragmentTex.txt")

        glUseProgram(self.shader)

        self.pA = (-0.9, -0.9)
        self.pB = (0.1, -0.9)
        self.pC = (0.1, 0.1)

        self.K = 0.8

        self.square1 = Square(self.pA, self.K, 0, 1.0)
        self.square2 = Square(self.pB, self.K, 1, 1.0)
        self.square3 = Square(self.pC, self.K, 2, 1.0)

        self.p = [(0.0, 0.0), (-0.4, -0.4), (0.0, -0.8),
                  (0.4, -0.4), (0.4, 0.3), (0.0, 0.5), (-0.4, 0.3)]

        self.pA0, self.pA1, self.pA2, self.pA3 = ((-0.4, -0.4), (0.0, -0.8),
                                                  (0.0, 0.0), (-0.4, 0.3))

        self.pB0, self.pB1, self.pB2, self.pB3 = (self.pA1, (0.4, -0.4),
                                                  (0.4, 0.3), self.pA2)

        self.pC0, self.pC1, self.pC2, self.pC3 = (self.pA3, self.pA2,
                                                  self.pB2, (0.0, 0.5))

        self.updateC(self.pA, self.K,
                     self.p[1], self.p[2], self.p[0], self.p[6], "cA")
        self.updateC(self.pB, self.K,
                     self.p[2], self.p[3], self.p[4], self.p[0], "cB")
        self.updateC(self.pC, self.K,
                     self.p[6], self.p[0], self.p[4], self.p[5], "cC")

        glUniform1i(glGetUniformLocation(self.shader, "imageTextureA"), 0)
        glUniform1i(glGetUniformLocation(self.shader, "imageTextureB"), 1)
        glUniform1i(glGetUniformLocation(self.shader, "imageTextureC"), 2)

        self.textures = []
        self.textures.append(
            Textures("img/A/alex.png", "img/B/alex.png", "img/C/alex.png"))

        self.textures.append(
            Textures("img/A/cow.png", "img/B/cow.png", "img/C/cow.png"))

        self.textures.append(
            Textures("img/A/creeper.png", "img/B/creeper.png", "img/C/creeper.png"))

        self.textures.append(
            Textures("img/A/husk.png", "img/B/husk.png", "img/C/husk.png"))

        self.textures.append(
            Textures("img/A/redCow.png", "img/B/redCow.png", "img/C/redCow.png"))

        self.textures.append(
            Textures("img/A/skeleton.png", "img/B/skeleton.png", "img/C/skeleton.png"))

        self.textures.append(
            Textures("img/A/steve.png", "img/B/steve.png", "img/C/steve.png"))

        self.textures.append(
            Textures("img/A/witherSkeleton.png", "img/B/witherSkeleton.png", "img/C/witherSkeleton.png"))

        self.textures.append(
            Textures("img/A/zombie.png", "img/B/zombie.png", "img/C/zombie.png"))

        self.mainLoop()

    def updateC(self, p0, K, p0_, p1_, p2_, p3_, dst):
        c = MatrixT(p0, K, p0_, p1_, p2_, p3_)
        glUniform1fv(glGetUniformLocation(self.shader, dst),
                     8, np.array(c, dtype=np.float32))

    def mainLoop(self):
        running = True

        self.A_color = np.array(np.random.rand(3), dtype=np.float32)
        self.B_color = np.array(np.random.rand(3), dtype=np.float32)
        self.C_color = np.array(np.random.rand(3), dtype=np.float32)

        self.selected = 0  # 0, ..., 6
        self.discoMode = False

        self.counter = 0
        self.tex = 0
        self.rad = np.radians(np.random.rand())

        self.textures[0].use()

        while (running):
            # check events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
                if (event.type == pg.KEYDOWN):
                    if (event.key == pg.K_0):
                        self.selected = 0
                    if (event.key == pg.K_1):
                        self.selected = 1
                    if (event.key == pg.K_2):
                        self.selected = 2
                    if (event.key == pg.K_3):
                        self.selected = 3
                    if (event.key == pg.K_4):
                        self.selected = 4
                    if (event.key == pg.K_5):
                        self.selected = 5
                    if (event.key == pg.K_6):
                        self.selected = 6
                    if (event.key == pg.K_d):
                        self.discoMode = False if (self.discoMode) else True
                if (event.type == pg.MOUSEBUTTONDOWN):
                    x, y = pg.mouse.get_pos()
                    x = 2 * x / self.width - 1
                    y = -2 * y / self.height + 1
                    for i in range(7):
                        if (self.selected == i):
                            self.p[i] = (x, y)
                    self.updateC(
                        self.pA, self.K, self.p[1], self.p[2], self.p[0], self.p[6], "cA")
                    self.updateC(
                        self.pB, self.K, self.p[2], self.p[3], self.p[4], self.p[0], "cB")
                    self.updateC(
                        self.pC, self.K, self.p[6], self.p[0], self.p[4], self.p[5], "cC")

            if (self.counter >= 100):
                self.textures[self.tex % len(self.textures)].use()
                self.tex += 1
                self.counter = 0

            if (self.discoMode):
                self.rad += 0.1
                self.A_color = np.array([(np.sin(2 * self.rad)+1)/2, (np.cos(
                    2 * self.rad)+1)/2, (np.sin(4 * self.rad)+1)/2], dtype=np.float32)
                self.B_color = np.array([(np.sin(5 * self.rad)+1)/2, (np.cos(
                    3 * self.rad)+1)/2, (np.sin(4 * self.rad)+1)/2], dtype=np.float32)
                self.C_color = np.array([(np.sin(2 * self.rad)+1)/2, (np.cos(
                    4 * self.rad)+1)/2, (np.sin(4 * self.rad)+1)/2], dtype=np.float32)
            else:
                self.noDisco = np.array([1.0, 1.0, 1.0], dtype=np.float32)
                self.A_color = self.noDisco
                self.B_color = self.noDisco
                self.C_color = self.noDisco

            glUniform1fv(glGetUniformLocation(self.shader, "colorA"),
                         8, np.array(self.A_color, dtype=np.float32))

            glUniform1fv(glGetUniformLocation(self.shader, "colorB"),
                         8, np.array(self.B_color, dtype=np.float32))

            glUniform1fv(glGetUniformLocation(self.shader, "colorC"),
                         8, np.array(self.C_color, dtype=np.float32))

            # refresh screen
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)

            glBindVertexArray(self.square1.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.square1.vertex_count)

            glBindVertexArray(self.square2.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.square2.vertex_count)

            glBindVertexArray(self.square3.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.square3.vertex_count)

            pg.display.flip()
            self.clock.tick(60)
            self.counter += 1

        self.quit()

    def quit(self):

        self.square1.destroy()
        self.square2.destroy()
        self.square3.destroy()
        for tex in self.textures:
            tex.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

    def createShader(self, vertexFilePath, fragmentFilePath):
        with open(vertexFilePath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilePath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader


class Square:

    def __init__(self, p0, K, flag, tex):

        x0, y0 = p0

        self.vertices = (
            x0,   y0, flag, 0.0, tex,
            x0+K,   y0, flag, tex, tex,
            x0+K, y0+K, flag, tex, 0.0,

            x0+K, y0+K, flag, tex, 0.0,
            x0,   y0+K, flag, 0.0, 0.0,
            x0, y0, flag, 0.0, tex
        )

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = len(self.vertices) // 5

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes,
                     self.vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              20, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                              20, ctypes.c_void_p(12))

    def destroy(self):

        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


class Textures:

    def __init__(self, fileA, fileB, fileC):
        self.textureA = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textureA)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = pg.image.load(fileA).convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pg.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width,
                     image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        self.textureB = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textureB)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = pg.image.load(fileB).convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pg.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width,
                     image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        self.textureC = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textureC)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = pg.image.load(fileC).convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pg.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width,
                     image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureA)

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.textureB)

        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.textureC)

    def destroy(self):

        glDeleteTextures(1, (self.textureA, self.textureB, self.textureC))


class Material:

    def __init__(self, filepath: str):

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = pg.image.load(filepath).convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pg.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width,
                     image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self) -> None:

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self) -> None:

        glDeleteTextures(1, (self.texture,))


if __name__ == "__main__":
    app = App()
