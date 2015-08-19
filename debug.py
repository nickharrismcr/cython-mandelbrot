'''
Created on 25 Jun 2015

@author: nick
'''
import sfml as sf
 
class Debug():
    
    def __init__(self,win):
        
        self.font=sf.Font.from_file("resources/arial.ttf")
        self.win=win
        self.debug=sf.Text()
        self.debug.color=sf.Color.BLACK
        self.debug.character_size=10
        self.debug.font=self.font
        self.backgnd=sf.RectangleShape()
        self.backgnd.fill_color=sf.Color.WHITE
        self.backgnd.position=sf.Vector2(18,18)
        self.clock=sf.Clock()
        self.debug.position=sf.Vector2(20,20)
        
    def displayfps(self,draw=False):
        time= self.clock.elapsed_time.milliseconds
        
        if time >0.0:
            self.debug.string=str(1000.0/time)
            self.clock.restart()
            if draw:
                self.win.clear(sf.Color.WHITE)
                
            self.win.draw(self.debug)
            
            if draw:
                self.win.display()
     
    def display(self, deb_val, draw=False):
         
        self.debug.string=deb_val
           
        if draw:
            self.win.clear(sf.Color.WHITE)
        self.backgnd.size=self.debug.local_bounds.size+sf.Vector2(8,8)
        self.win.draw(self.backgnd) 
        self.win.draw(self.debug)
        
        if draw:
            self.win.display()  
            
    def progressbar(self, legend,  max,  curr, draw=False):
        
        self.debug.string=legend
        if draw:
            self.win.clear(sf.Color.WHITE)
            
        
        rec1 = sf.RectangleShape()
        rec1.position=sf.Vector2(20,80)
        rec1.size=sf.Vector2(200,60)
        rec1.outline_color=sf.Color.BLACK
        rec1.outline_thickness = 2
        rec1.fill_color=sf.Color.TRANSPARENT
        
        rec2 = sf.RectangleShape()
        rec2.position=sf.Vector2(25,85)
        w=int((float(curr)/float(max))*190.0)
        rec2.size=sf.Vector2(w,50)
        rec2.fill_color=sf.Color(0,200,0)
        
        self.win.draw(self.debug)
        self.win.draw(rec1)
        self.win.draw(rec2)
        
        if draw:
            self.win.display()
            