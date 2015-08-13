# mandel3.pyx
# cython: profile=True
# distutils : 

import cython,random
import numpy as pnp
cimport numpy as np # for the special numpy stuff
import sfml as sf
import logging 
import math 


from cython.parallel import parallel, prange

from libc.math cimport sqrt, log 
from libc.stdio cimport printf


#=================================================================================================================
@cython.profile(False)
@cython.boundscheck(False)
@cython.cdivision

cdef inline int julia(double z_real, double z_imag, double c_real, double c_imag, int max_iterations=20) nogil:
    
    
    cdef int i

    for i in range(0, max_iterations):
        
        z_real, z_imag = ( z_real*z_real - z_imag*z_imag + c_real,
                           2*z_real*z_imag + c_imag )
        
        if (z_real*z_real + z_imag*z_imag) >= 4.0:
            return i
        
    return 0

 
                   
#=================================================================================================================
@cython.boundscheck(False)
@cython.cdivision
cdef  create_fractal_parallel( 
                        double c_real,
                        double c_imag,
                        int nb_iterations,
                        int colours  ,
                        np.ndarray[np.uint8_t,  ndim=3, mode="c"] image  ):
    
    cdef:
        double min_x = -2.0
        double max_x = 2.0
        double min_y = -1.0
        double max_y = 2.0    
        int width, height
        int x, y, start_y, end_y
        int colour, count
        double real, imag, pixel_size
        int c,c1, l

    width = image.shape[0]
    height = image.shape[1]
    pixel_size = (max_x - min_x) / width
    
    arrlen=width*height      
    for l in prange(arrlen, nogil=True, schedule='dynamic'):
        
        x=l//height
        y=l%height
        real = min_x + x*pixel_size
        imag = min_y + y*pixel_size
        colour = julia(real, imag, c_real, c_imag,  nb_iterations) % colours
        
    
        c1=min(255,colour)
        image[x, y, 0] = c1
        
        colour=max(0,colour-c1)
        c1=min(255,colour)
        image[x,y,1] = c1
        
        colour=max(0,colour-c1)
        c1=min(255,colour)
        image[x,y,2] = c1 
            
                
              
                         
#=================================================================================================================
class Julia(object ):
    
    def __init__(self,float sizex,float sizey,speed=10):
        
       
        self.speed=speed
        self.sizex=sizex
        self.sizey=sizey
        self.render_tex=sf.RenderTexture(sizex,sizey)
        self.palette_size=256*3
        self.image=pnp.zeros((sizex, sizey, 3 ), dtype=pnp.uint8) + 125
        self.clock=sf.Clock()
        self.sf_img=None
        self.curr_image=-1
        self.calc_time=0.0
        
        
    
    def get_render_tex(self):
        
        return self.render_tex.texture
       
 
    def calc(self, float c_real, float c_imag, int iterations):       
        
        create_fractal_parallel(c_real, c_imag , iterations, self.palette_size, self.image)
        self.build_sf_image(self.image)
        
 
    def build_texture(self):
        
        sprite=sf.Sprite(sf.Texture.from_image(self.sf_img))
        self.render_tex.draw(sprite)
        self.render_tex.display()
        
    def build_sf_image(self, np.ndarray[np.uint8_t,  ndim=3, mode="c"] image   ):
        
        cdef int w,h,x,r,g,b

        col=sf.Color.BLUE
        sfcol=sf.Color 

        w= image.shape[0]
        h= image.shape[1]
        sf_img=sf.Image.create(self.sizex,self.sizey,sf.Color.BLACK)
        
        for x in xrange(0,w):
            for y in xrange(0,h):
                r=image[x,y,0]
                g=image[x,y,1]
                b=image[x,y,2]
               
                col=sfcol(r,g,b,255)
                sf_img[x,y]=col
                
        self.sf_img=sf_img 
        
    
 
        
    
            
        
 