######################################################
# Pedro Soares Jardim
# 19102856-2
# Fundamentos de Computação Gráfica - Turma 010 - 2021/2
#####################################################
from Ponto import Ponto
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Curva:
    def __init__(self, *args:Ponto):
        self.pos = 0
        self.lst_pt = []
        self.continua = []
        for i in args:
            self.lst_pt.append(i)


    def __repr__(self) -> str:
        if len(self.lst_pt) == 3:
            return (f"""
                    Curva:
                    id:{self.pos}
                    P1:{self.lst_pt[0]}
                    P2:{self.lst_pt[1]}
                    P3:{self.lst_pt[2]}
                    Continuaçoes:{self.continua}
            """)
        elif len(self.lst_pt) == 4:
            return (f"""
                    Curva:
                    id:{self.pos}
                    P1:{self.lst_pt[0]}
                    P2:{self.lst_pt[1]}
                    P3:{self.lst_pt[2]}
                    P4:{self.lst_pt[3]}
                    Continuaçoes:{self.continua}
            """)


    def desenhaCurva(self):
        t:float = 0
        delta:float = 1/50
        p = Ponto()

        
        glBegin(GL_LINE_STRIP)
        
        while t < 1:
            
            p = self.computaBezier(t)
            glVertex2f(p.x, p.y)
            t += delta

        p =  self.computaBezier(1)
        glVertex2f(p.x, p.y)
        glEnd()



    def computaBezier(self, t:float) -> Ponto:
        um_menos_t = 1-t
        
        if len(self.lst_pt) == 3:
            p0 = self.lst_pt[0]
            p1 = self.lst_pt[1]
            p2 = self.lst_pt[2]
            
            c1x = (um_menos_t**2 * p0.x) + (2*um_menos_t * t * p1.x) + (t**2 * p2.x)
            c1y = (um_menos_t**2 * p0.y) + (2*um_menos_t * t * p1.y) + (t**2 * p2.y)
            c1 = Ponto()
            c1.set(c1x, c1y)
            return c1

        elif len(self.lst_pt) == 4:
            p0 = self.lst_pt[0]
            p1 = self.lst_pt[1]
            p2 = self.lst_pt[2]
            p3 = self.lst_pt[3]

            c1x = (um_menos_t**3 *p0.x) + ((3*um_menos_t**2)*t*p1.x) + ((3*um_menos_t**2)*t*p2.x) + (t**3 * p3.x)
            c1y = (um_menos_t**3 *p0.y) + ((3*um_menos_t**2)*t*p1.y) + ((3*um_menos_t**2)*t*p2.y) + (t**3 * p3.y)
            c1 = Ponto()
            c1.set(c1x, c1y)
            return c1
           
            