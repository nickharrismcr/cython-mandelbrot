  

import random
import numpy as np
import sfml as sf
import math 
 
 

def mandel(real, imag, max_iterations=20):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after a maximum allowed number of iterations, the absolute value of
       the resulting number is greater or equal to 2.'''
    z_real=0.0
    z_imag=0.0
    for i in range(0, max_iterations):
        z_real, z_imag = ( z_real*z_real - z_imag*z_imag + real,
                           2*z_real*z_imag + imag )
        if (z_real*z_real + z_imag*z_imag) >= 4:
            return i
    
    return 0

#=================================================================================================================

def  create_fractal( 
                        min_x,
                        max_x,
                        min_y,
                        nb_iterations,
                        colours,
                        image,
                        data  ):


    nb_colours = len(colours)
    width = image.shape[0]
    height = image.shape[1]
    pixel_size = (max_x - min_x) / width
            
    for x in range(width):
        real = min_x + x*pixel_size
        for y in range(height):
            
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
                 
def refresh_image( 
                    colours  ,
                    image  ,
                    data  ): 

        w=image.shape[0]
        h=image.shape[1]
        
        arrlen=w*h      
        for l in range(0,arrlen):
            
            x=l//h 
            y=l%h 
            colour=data[x, y]  
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
    
    def __init__(self,win, sizex, sizey,speed=10):
        
        self.win=win
        self.speed=speed
        self.palette_size=256*3
        self.palette_tex=sf.RenderTexture(self.palette_size*4, 5)
        self.colours=self.make_palette2()
        self.image=np.zeros((sizex, sizey, 3 ), dtype=np.uint8) + 125
        self.data=np.zeros((sizex, sizey), dtype=np.int32) + 125
        self.sf_img=sf.Image.create(sizex,sizey,sf.Color.BLACK)
        self.clock=sf.Clock()
        self.image_list=[]
        self.calc_time=0.0
        self.draw_time=0.0
        
        
    def get_palette_tex(self):
        
        return self.palette_tex.texture
       
    def new_colours(self):
        
        self.colours=self.make_palette2()
        refresh_image(self.colours, self.image, self.data )
    
    
     
   
    def make_palette2(self):
        
        colours=np.zeros((self.palette_size,3), dtype=np.uint8) + 125
    
        col=sf.Color.RED 
        gen=gen_random_grayscale(col,self.speed)
        
        for i in xrange(0,self.palette_size):
            r,g,b,a=gen.next()
            #colours[i,0]=r 
            #colours[i,1]=g
            #colours[i,2]=b
            self.draw_to_palette_tex(i,(r,g,b))
            
        self.palette_tex.display()
        return np.array(colours, dtype=np.uint8)   
    
    def calc(self, min_x, max_x, min_y, iterations):       
        
        self.clock.restart()
        create_fractal(min_x, max_x, min_y, iterations, self.colours, self.image, self.data)
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
        
    def draw_palette(self):
        w=self.win.size.x
        h=self.win.size.y
        
        rect=sf.RectangleShape()
        rect.position=sf.Vector2(0,h-7)
        rect.size=sf.Vector2(w,7)
        r,g,b=self.colours[-1]
        rect.fill_color=sf.Color.BLACK
        self.win.draw(rect)
        
        sprite=sf.Sprite(self.palette_tex.texture)
        sprite.position=sf.Vector2(0,h-5)
        sprite.scale(sf.Vector2(float(w)/float(self.palette_size),1.0))
        self.win.draw(sprite)
         
          
    def draw(self):
        
        self.do_draw(self.image)
        
    
    def do_draw(self, image   ):
        
        
        self.clock.restart()
        
        col=sf.Color.BLUE
        sfcol=sf.Color 

        w= image.shape[0]
        h= image.shape[1]
        sf_img=self.sf_img
        
        for x in xrange(0,w):
            for y in xrange(0,h):
                r=image[x,y,0]
                g=image[x,y,1]
                b=image[x,y,2]
               
                col=sfcol(r,g,b,255)
                sf_img[x,y]=col
                
        sprite=sf.Sprite(sf.Texture.from_image(sf_img))
        self.win.draw(sprite)
        
        self.draw_time=self.clock.elapsed_time.milliseconds/1000.0

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
 
    
    