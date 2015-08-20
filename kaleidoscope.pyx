import sfml as sf
import random, math, os, itertools  
from operator import pos
from imageop import scale
from idlelib.ZoomHeight import zoom_height
cimport libcpp.sfml as sfc
from pysfml.window cimport Window as cWindow 
from pysfml.system cimport Vector2 as cVector2
from pysfml.graphics cimport Texture as cTexture
from pysfml.graphics cimport ConvexShape as cConvexShape


cdef rand(double min,double max, double val):
    
    cdef double x
    x= (random.randint(100*min,100*max)/100.0)*val
    return x

cdef class Kaleidoscope(object):
    
    cdef cTexture tex
    cdef cVector2 pos
    cdef int leaves
    cdef int radius
    cdef float tex_dx
    cdef float scale
   
    cdef float tex_dy 
    cdef int bright
    cdef int currbright 
    cdef int tri_width 
    cdef float tex_x,tex_y,tex_w,tex_h
    cdef sfc.View view 
    cdef float rotate_amount 
    cdef cConvexShape polygon 
    
    def __init__(self, dict settings, cWindow win):
        
        self.tex=<cTexture>settings["texture"]
        self.pos=<cVector2>settings["position"]
        self.leaves=settings["leaves"]
        self.radius=settings["radius"]
        self.tex_dx=settings["speed"]
        self.scale=settings["scale"]
        self.tex_dy=self.tex_dx
        self.bright=settings["bright"]
        self.currbright=self.bright
        
        self.tri_width=(self.radius*2*math.pi/self.leaves)+3
        self.tex_x=self.tex.width/2
        self.tex_y=self.tex.height/2
        self.tex_w=self.radius
        self.tex_h=self.tri_width
   
        self.rotate_amount=360.0/self.leaves
        
        self.polygon = sf.ConvexShape()
        self.polygon.point_count = 3
        self.polygon.set_point(0, (0, 0))
        self.polygon.set_point(1, (self.radius , self.tri_width/2))
        self.polygon.set_point(2, (0, self.tri_width))
         
        self.polygon.origin=cVector2(self.radius, self.tri_width/2.0)
        self.polygon.fill_color=sf.Color(self.currbright,self.currbright,self.currbright, self.currbright)
        self.polygon.position = self.pos
        self.polygon.texture=self.tex
        self.polygon.ratio=cVector2(self.scale,self.scale) 
        self.polygon.texture_rectangle=sf.Rectangle(cVector2(self.tex_x,self.tex_y),cVector2(self.tex_w,self.tex_h))
        
    def update(self):
        
        self.tex_x+=self.tex_dx
        self.tex_y+=self.tex_dy
        
        if self.tex_x<=0 or self.tex_x>=self.tex.width-self.tex_w:
            self.tex_dx=-self.tex_dx
        if self.tex_y<=0 or self.tex_y>self.tex.height-self.tex_h:
            self.tex_dy=-self.tex_dy

        
    def draw(self,win,states):
        
        cdef int i 
            
        rec1=sf.Rectangle(cVector2(self.tex_x,self.tex_y),cVector2(self.tex_w,self.tex_h))
        rec2=sf.Rectangle(cVector2(self.tex_x,self.tex_y+self.tex_h),cVector2(self.tex_w, -self.tex_h))
        self.polygon.rotation=0
        poly=self.polygon
        rot=self.rotate_amount
        
        for i in range(0,self.leaves):
            
            poly.rotate(rot)
            if i%2==0:
                poly.texture_rectangle=rec1
            else:
                poly.texture_rectangle=rec2

            win.draw(self.polygon,states) 
             
            
 
                    