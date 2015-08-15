# mandel3.pyx
# cython: profile=True
# distutils : 

import cython,random
import numpy as pnp
cimport numpy as np # for the special numpy stuff
import sfml as sf
cimport libcpp.sfml as sfc
from pysfml.graphics cimport Image as cImage
import logging 
import math 


from cython.parallel import parallel, prange

from libc.math cimport sqrt, log 
from libc.stdio cimport printf


#=================================================================================================================
@cython.profile(False)
@cython.boundscheck(False)
@cython.cdivision

cdef inline int mandel(double real, double imag, int max_iterations=20) nogil:
    
    cdef double z_real = 0., z_imag = 0., modulus, mu
    cdef int i

    for i in range(0, max_iterations):
        z_real, z_imag = ( z_real*z_real - z_imag*z_imag + real,
                           2*z_real*z_imag + imag )
        if (z_real*z_real + z_imag*z_imag) >= 20.0:
            return i
            #break
        
    return 0

    #modulus=sqrt(z_real*z_real + z_imag*z_imag)
    #mu= i-(log(log(modulus)))/log(2.0)
    
    #printf("%i\n",<int>(mu*256))
    #return <int>(mu*10)
                 
#=================================================================================================================
@cython.boundscheck(False)
@cython.cdivision
cdef  create_fractal_parallel( 
                        double min_x,
                        double max_x,
                        double min_y,
                        int nb_iterations,
                        np.ndarray[np.uint8_t,  ndim=2, mode="c"] colours  ,
                        np.ndarray[np.uint8_t,  ndim=3, mode="c"] image  ,
                        np.ndarray[np.int32_t,  ndim=2, mode="c"] data  ):
    
    cdef int width, height
    cdef int x, y, start_y, end_y
    cdef long nb_colours, colour, count
    cdef double real, imag, pixel_size
    cdef int c1,l

    nb_colours = len(colours)
    width = image.shape[0]
    height = image.shape[1]
    pixel_size = (max_x - min_x) / width
    
    arrlen=width*height      
    for l in prange(arrlen, nogil=True, schedule='dynamic'):
        
        x=l//height
        y=l%height
        real = min_x + x*pixel_size
        imag = min_y + y*pixel_size
        colour = mandel(real, imag, nb_iterations) % nb_colours
        
        data[x, y] = colour 
        
        c1=min(255,colour)
        image[x, y, 0] = c1
        
        colour=max(0,colour-c1)
        c1=min(255,colour)
        image[x,y,1] = c1
        
        colour=max(0,colour-c1)
        c1=min(255,colour)
        image[x,y,2] = c1 
      
                         
#=================================================================================================================
class Mandelbrot2(object ):
    
    def __init__(self,float sizex,float sizey,speed=10):
        
       
        self.speed=speed
        self.sizex=sizex
        self.sizey=sizey
        self.palette_size=256*3
        self.palette_tex=sf.RenderTexture(self.palette_size*4, 5)
        self.render_tex=sf.RenderTexture(sizex,sizey)
        self.colours=self.make_palette2()
        self.image=pnp.zeros((sizex, sizey, 3 ), dtype=pnp.uint8) + 125
        self.data=pnp.zeros((sizex, sizey), dtype=pnp.int32) + 125
        self.logger=logging.getLogger("mandlebrot")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.FileHandler("mandel.log"))
        self.clock=sf.Clock()
        self.sf_img=[]
        self.curr_image=-1
        self.calc_time=0.0
        
        
        
    def get_palette_tex(self):
        
        return self.palette_tex.texture
    
    def get_render_tex(self):
        
        return self.render_tex.texture
       
    def new_colours(self):
        
        self.colours=self.make_palette2()
   
    def make_palette2(self):
        
        colours=pnp.zeros((self.palette_size,3), dtype=pnp.uint8) + 125
        cdef int i 
        cdef int r,g,b,a 
        col=sf.Color.RED 
        gen=gen_random_color2(col,self.speed)
        
        cols=[]
        for i in xrange(0,self.palette_size/2):
            r,g,b,a=gen.next()
            cols.append((r,g,b,a))
        ind=self.palette_size/2-1
        for i in xrange(0,self.palette_size/2):
            cols.append(cols[ind])
            ind-=1
            
        i=0
        for r,g,b,a in cols:

            self.draw_to_palette_tex(i,(r,g,b))
            i+=1
            
        self.palette_tex.display()
        return pnp.array(colours, dtype=pnp.uint8)   
    
    def calc(self, min_x, max_x, min_y, iterations):       
        
        self.clock.restart()
        create_fractal_parallel(min_x, max_x, min_y, iterations, self.colours, self.image, self.data)
        sf_img=sf.Image.create(self.sizex,self.sizey,sf.Color.BLACK)       
        self.build_sf_image(self.image,sf_img)     
        self.sf_img.append(sf_img) 
        self.curr_image+=1   
        self.calc_time = self.clock.elapsed_time.milliseconds/1000.0
    
    def draw_to_palette_tex(self,index,col):
        
        rect=sf.RectangleShape()
        rect.size=sf.Vector2(1,5)
        r,g,b =col
        rect.fill_color=sf.Color(r,g,b)
        rect.position=sf.Vector2(index,0)
        self.palette_tex.draw(rect) 
        rect.position=sf.Vector2(index+self.palette_size,0)
        self.palette_tex.draw(rect) 
        rect.position=sf.Vector2(index+self.palette_size*2,0)
        self.palette_tex.draw(rect) 
        rect.position=sf.Vector2(index+self.palette_size*3,0)
        self.palette_tex.draw(rect) 
        
    def draw_palette(self,win):
        
        w=win.size.x
        h=win.size.y
        
        rect=sf.RectangleShape()
        rect.position=sf.Vector2(0,h-7)
        rect.size=sf.Vector2(w,7)
        r,g,b=self.colours[-1]
        rect.fill_color=sf.Color.BLACK
        win.draw(rect)
        
        sprite=sf.Sprite(self.palette_tex.texture)
        sprite.position=sf.Vector2(0,h-5)
        sprite.scale(sf.Vector2(float(w)/float(self.palette_size),1.0))
        win.draw(sprite)
         
          
    @cython.boundscheck(False)
    def build_texture(self):
        
        sprite=sf.Sprite(sf.Texture.from_image(self.sf_img[self.curr_image]))
        self.render_tex.draw(sprite)
        self.render_tex.display()
        
    def build_sf_image(self, np.ndarray[np.uint8_t,  ndim=3, mode="c"] image, cImage sf_img   ):
        
        cdef int w,h,x,r,g,b

        w= image.shape[0]
        h= image.shape[1]
       
        for x in xrange(0,w):
            for y in xrange(0,h):
                r=image[x,y,0]
                g=image[x,y,1]
                b=image[x,y,2]
               
                sf_img.p_this.setPixel(x,y, sfc.Color(r,g,b,255))
   
    
    def set_image_index(self,index):
        
        if index >= len(self.sf_img):
            index=len(self.sf_img)-1
        self.curr_image=index
        
    
            
        
#######################################################################################################################
def gen_random_color(col, delta):
       
    while True:
        
        r = col.r
        g = col.g
        b = col.b
        
        r += random.randint(-delta, delta)
        g += random.randint(-delta, delta)
        b += random.randint(-delta, delta)
        col.r = clamp(r)
        col.g = clamp(g)
        col.b = clamp(b)
        yield col
#######################################################################################################################
def gen_random_color2(col, delta):
     
    col.r=random.randint(0,255) 
    col.g=random.randint(0,255) 
    col.b=random.randint(0,255) 
    
    dr = random.choice((-2*delta, -delta, delta, delta*2))/10.0
    dg = random.choice((-2*delta, -delta, delta, delta*2))/10.0
    db = random.choice((-2*delta, -delta, delta, delta*2))/10.0
    
    while True:
        
        r = col.r
        g = col.g
        b = col.b
        
        r += dr
        g += dg
        b += db 
        
        if r > 255.0 :
            r=254.0
            dr=-dr
        if g > 255.0:
            g=254.0
            dg=-dg
        if b > 255.0:
            b=254.0
            db=-db
            
        if r < 0.0 :
            r=1.0
            dr=-dr
        if g < 0.0:
            g=1.0
            dg=-dg
        if b < 0.0:
            b=1.0
            db=-db 
                  
        col.r = r #clamp(r)
        col.g = g #clamp(g)
        col.b = b #clamp(b)
        yield col
                
#######################################################################################################################  
def gen_random_grayscale(col, delta):
       
    while True:
        
        r = col.r
        g = col.g
        b = col.b
        
        r += random.randint(-delta, delta)
        
        col.r = clamp(r)
        col.g = clamp(r)
        col.b = clamp(r)
        yield col
        
#######################################################################################################################                  
def clamp(col):
    
    if col < 0:
        return 0
    if col > 255:
        return 255
    return col
#######################################################################################################################
 
    
    