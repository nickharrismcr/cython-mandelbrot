import sfml as sf
import random, math, os, itertools  
 
vec2=sf.Vector2

def rand(min,max,val):
    
    x= float((random.randint(100*min,100*max)/100.0))*val
    return x

class Kaleidoscope():
    
    def __init__(self,settings,win):
        
        self.tex=settings["texture"]
        self.pos=settings["position"]
        self.leaves=settings["leaves"]
        self.radius=settings["radius"]
        self.tex_dx=settings["speed"]
        self.scale=settings["scale"]
        self.zoom=settings["depth"]
        self.tex_dy=self.tex_dx
        self.bright=255
        self.currbright=self.bright
        
        self.view=sf.View(sf.Rectangle((0, 0), (win.width , win.height)))
        self.view.zoom(self.zoom)
        
        self.tri_width=(self.radius*2*math.pi/self.leaves)+3
        self.tex_x=rand( .5,1.5,self.tex.width/2)
        self.tex_y=rand( .5,1.5,self.tex.height/2)
        self.tex_w=self.radius
        self.tex_h=self.tri_width
   
         
        self.rotate_amount=360.0/self.leaves
        
        self.polygon = sf.ConvexShape()
        self.polygon.point_count = 3
        self.polygon.set_point(0, (0, 0))
        self.polygon.set_point(1, (self.radius , self.tri_width/2))
        self.polygon.set_point(2, (0, self.tri_width))
         
        self.polygon.origin=vec2(self.radius, self.tri_width/2.0)
        self.polygon.fill_color=sf.Color(self.currbright,self.currbright,self.currbright, self.currbright)
        self.polygon.position = self.pos
        self.polygon.texture=self.tex
       
        self.polygon.texture_rectangle=sf.Rectangle(vec2(self.tex_x,self.tex_y),vec2(self.tex_w,self.tex_h))
        
    def update(self):
        
        self.polygon.position = self.pos
        self.polygon.ratio=vec2(self.scale,self.scale) 
        self.tex_x+=self.tex_dx
        self.tex_y+=self.tex_dy
        
        if self.tex_x<=0 or self.tex_x>=self.tex.width-self.tex_w:
            self.tex_dx=-self.tex_dx
        if self.tex_y<=0 or self.tex_y>self.tex.height-self.tex_h:
            self.tex_dy=-self.tex_dy
        
        self.polygon.fill_color=sf.Color(self.currbright,self.currbright,self.currbright, self.currbright)
         
        
    def draw(self,win,states):
            
        rec1=sf.Rectangle(vec2(self.tex_x,self.tex_y),vec2(self.tex_w,self.tex_h))
        rec2=sf.Rectangle(vec2(self.tex_x,self.tex_y+self.tex_h),vec2(self.tex_w, -self.tex_h))
        self.polygon.rotation=0
         
        for i in range(0,self.leaves):
            
            self.polygon.rotate(self.rotate_amount)
            if i%2==0:
                self.polygon.texture_rectangle=rec1
            else:
                self.polygon.texture_rectangle=rec2

            win.draw(self.polygon,states) 
             
            
class Kaleido_list():
    
    def __init__(self,win,tex ):
        
        self.tex=tex
        self.kal_list=[]
        self.view=sf.View(sf.Rectangle((0, 0), (win.width , win.height)))
        self.lastpos=vec2(0,0)

        for i in range(-7,7):
            for j in range(-7 ,7):
                x=rand(0.5,1.5,i*300 )
                y=rand(0.5,1.5,j*300)
                settings={ "texture":self.tex,  "position":vec2(x,y), "leaves":64,
                           "speed":3, "radius": 150, "scale":random.randint(1,10)/10.0, "depth": 1  }
                self.kal_list.append(Kaleidoscope(settings,win))  
                
    def reset(self,win):
        
        self.view=sf.View(sf.Rectangle((0, 0), (win.width , win.height)))
        self.lastpos=vec2(0,0)  
           
    def update(self,tran,currzoom):
        
        lastxpos,lastypos=self.lastpos
        xpos,ypos=tran.path.get2d()
        dx= 2*(lastxpos-xpos)/currzoom
        dy= 2*(lastypos-ypos)/currzoom  
        self.lastpos=vec2(xpos,ypos)
        self.view.move(dx ,dy  )     
        self.view.rotate(tran.rotate.get1d())
        self.lastpos=vec2(xpos,ypos)
        
        for k in self.kal_list:
            k.update()
        
    def draw(self,win): 
         
        win.view=self.view 
        for k in self.kal_list:
             k.draw(win) 
                    