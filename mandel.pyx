'''
Created on 26 Jul 2015



@author: nick
'''
from functools import reduce
import sfml as sf 
from numpy import NaN, arange, zeros, isnan
 

deb=open("debug.txt","w")

cdef class Mandelbrot(object):
    '''
    classdocs
    '''
    cdef object win
    cdef object X 
    cdef object Y   
    cdef object Z 
    cdef object colors

    def __init__(self, win):
        
        self.win=win
        self.colors=[0]*256
        for n in range(0,64):
            self.colors[   0 + n ] = sf.Color(  n*4, 4 * n, 0 )
            self.colors[  64 + n ] = sf.Color(  64, 255, 4 * n )
            self.colors[ 128 + n ] = sf.Color(  64, 255 - 4 * n , 255 )
            self.colors[ 192 + n ] = sf.Color(  64, 0, 255 - 4 * n )
 
    def m(self, a):
    
        z = 0
        cdef int n 
        for n in xrange(1, 150  ):
            z = z**2 + a
            if abs(z) > 2:
                return n
            
        return NaN
    
    def calc(self):
        
        cdef int ix,iy
        cdef float x,y
         
         
        self.X = arange(-1, 0, .001)
        self.Y = arange(-0.5,  0.5, .001)
        self.Z = zeros((len(self.Y), len(self.X)))
        
        for iy, y in enumerate(self.Y):
            
            for ix, x in enumerate(self.X):
                z=x+(1j*y)
                self.Z[iy,ix] = self.m(z)

 
    def draw(self):
        
        cdef int ix,iy,x1,y1
        cdef float x,y
        
        sh=sf.CircleShape()
        sh.radius=0.5
        y1=0
         
        self.X = arange(-1.5, 0.5, .001)
        self.Y = arange(-0.5,  0.5, .001) 
        
        for iy, y in enumerate(self.Y):
            
            x1=0
            y1+=1
            
            for ix, x in enumerate(self.X):
            
                x1+=1
                z=x+(1j*y)
                c= self.m(z)
               
                sh.fill_color=sf.Color.BLACK
                if not isnan(c):
                    c*=3   
                    sh.fill_color=self.colors[min(255,int(c))]
                sh.position=sf.Vector2(x1,y1)
                self.win.draw(sh)
            
            self.win.display()   
                     
        