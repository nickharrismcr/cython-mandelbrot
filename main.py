'''
Created on 26 Jul 2015

@author: nick
'''
 

if __name__ == '__main__':
    pass

import sfml as sf, mandel2, cycleshader, debug, mandel_py,random, math, julia, copy

WINDOWED=1
FULLSCREEN=0

#####################################################################################################
class App():
    
    def __init__(self, mode=FULLSCREEN):
        
        cont=sf.ContextSettings(antialiasing=4)
        if mode!=WINDOWED:
            win = sf.RenderWindow(sf.VideoMode.get_desktop_mode(), "Mandel", sf.window.Style.FULLSCREEN, cont )
        else:
            win = sf.RenderWindow(sf.VideoMode(1000,600), "Mandel"  )  
            
        win.vertical_synchronization = True
        win.framerate_limit = 60
        
        self.win=win
        self.win.key_repeat_enabled=False
        self.clock=sf.Clock()
        self.backgnd=sf.Color.BLACK
        self.aspect=float(win.height)/float(win.width)
        
        self.debug=debug.Debug(self.win)
        self.mandelbrot2=mandel2.Mandelbrot2(self.win.size.x,self.win.size.y,10)
        self.julia=julia.Julia(self.win.size.x/4.0,self.win.size.y/4.0,10)
        self.julia_full=julia.Julia(self.win.size.x,self.win.size.y,10)
        self.cycle=cycleshader.CycleShader(win, self.mandelbrot2.get_palette_tex())
        self.screen_tex=sf.Texture.create(self.win.size.x, self.win.size.y)
        
        self.step=0.0005
        self.box=sf.RectangleShape()
        self.box.fill_color=sf.Color.TRANSPARENT
        self.box.outline_color=sf.Color.WHITE
        self.box.outline_thickness=1
        self.mouse=sf.Mouse
        self.draw_area=False
        self.draw_box=False
        self.view_list=[]
        self.view_index=0
        self.use_shader=True
        self.julia_coord_list=[(0,0)]
        self.julia_replay_img_list=[]
        self.replay_index=None
        
        

    def handle_events(self):
        
       
        
        for event in self.win.events:
            if type(event) is sf.CloseEvent:
                self.win.close()
            if type(event) is sf.KeyEvent and event.code is sf.Keyboard.ESCAPE:
                self.win.close()
            
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.UP:
                self.iters += 100
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.DOWN:
                self.iters -= 100
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.SPACE:
                
                self.mode = "calc"
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.RETURN:
                self.mode = "calc"
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.C:
                self.win.mouse_cursor_visible = False
                self.mandelbrot2.new_colours()
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.L_BRACKET:
                self.step /= 1.1
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.R_BRACKET:
                self.step *= 1.1
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.S:
                self.mode = "init_display_list"
                self.view_index = 0
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.LEFT:
                self.mandelbrot2.speed += 1
                self.mandelbrot2.new_colours()
                self.cycle.set_color_table(self.mandelbrot2.get_palette_tex())
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.RIGHT:
                self.mandelbrot2.speed -= 1 if self.mandelbrot2.speed > 1 else 0
                self.mandelbrot2.new_colours()
                self.cycle.set_color_table(self.mandelbrot2.get_palette_tex())
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.DELETE:
                self.use_shader = not self.use_shader
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.J:
                self.mode="julia"
            if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.K:
                self.replay_index=None
                self.mode="replay_julia"


    def calculate(self):
        
        self.view = self.win.default_view
        self.win.mouse_cursor_visible = False
        self.mandelbrot2.calc(self.xstart, self.xend, self.ystart, self.iters)
        self.mandelbrot2.build_texture()
        self.screen_spr = sf.Sprite(self.mandelbrot2.get_render_tex())
        self.view_list.append(None)
        self.mode = "user_zoom"
       

    def user_zoom(self):
        
       
        self.win.mouse_cursor_visible = True
        self.win.clear(sf.Color.BLACK)
        #self.win.view=self.view
        states = sf.RenderStates()
        if self.use_shader:
            states.shader = self.cycle.shader
        self.win.draw(self.screen_spr, states)
        #self.win.view=self.win.default_view
        self.mandelbrot2.draw_palette(self.win)
        self.debug.display("Iterations : %s  Cycle speed : %s   Calculation time : %s    " % (self.iters, self.mandelbrot2.speed, self.mandelbrot2.calc_time))
        
        if self.draw_box:
            self.win.draw(self.box)
        
        if self.mouse.is_button_pressed(sf.Mouse.RIGHT):
            self.iters+=500
            self.mode = "calc"
            self.draw_box = False
            self.xstart, self.xend, self.ystart = self.n_xstart, self.n_xend, self.n_ystart
            bx, by = self.box.position
            bw, bh = self.box.size
            self.view_list[-1] = bx, by, bw, bh
            self.view_index += 1
       
        if self.mouse.is_button_pressed(sf.Mouse.LEFT):
            self.draw_box = True
            if not self.draw_area:
                self.draw_area = True
                self.box.position = self.mouse.get_position()
                self.box.size = sf.Vector2(0, 0)
            else:
                x, y = self.mouse.get_position()
                dx = x - self.box.position.x
                dy = dx * self.aspect
                self.box.size = sf.Vector2(dx, dy)
        
        elif self.draw_area:
            self.draw_area = False
            box_xstart = self.box.position.x
            box_xend = self.box.size.x + self.box.position.x
            box_ystart = self.box.position.y
            self.yend = self.ystart + (self.xend - self.xstart) * self.aspect
            self.n_xstart = self.xstart + ((self.xend - self.xstart) * box_xstart / self.win.size.x)
            self.n_xend = self.xstart + ((self.xend - self.xstart) * box_xend / self.win.size.x)
            self.n_ystart = self.ystart + ((self.yend - self.ystart) * box_ystart / self.win.size.y)
        
        self.cycle.update(self.step)
        self.win.display()
        


    def init_display_list(self):
        
        self.win.mouse_cursor_visible = False
        self.win.view=self.win.default_view
        self.mandelbrot2.set_image_index(self.view_index)
        self.mandelbrot2.build_texture()
        self.screen_spr = sf.Sprite(self.mandelbrot2.get_render_tex())
        self.clock.restart()
        
        self.boxzoom = 0
        if self.view_list[self.view_index] != None:
            self.boxzoom = 1
            x, y, w, h = self.view_list[self.view_index]
            self.endpos = sf.Vector2(x, y)
            self.startsize = sf.Vector2(self.win.size.x, self.win.size.y)
            self.endsize = sf.Vector2(w, h)
        self.mode="display_list"

    def display_list(self):
        
        self.win.clear(self.backgnd)
        states = sf.RenderStates()
        if self.use_shader:
            states.shader = self.cycle.shader
        self.win.draw(self.screen_spr, states)
        
        if self.boxzoom == 1:
            if self.clock.elapsed_time.milliseconds > 1.0:
                self.boxzoom=2
                
        elif self.boxzoom ==2 :
            
            fac=(self.clock.elapsed_time.milliseconds-1.0) / 1000.0
            fac2=(math.sin((fac*0.5*math.pi)))
            x,y=self.endpos * fac2
            w,h=self.endsize + (self.startsize - self.endsize) * (1 - fac2)
            
            self.view.reset(sf.Rectangle((x,y),(w,h)))
            self.win.view=self.view
        
        
        self.win.display()
        self.cycle.update(self.step)
        
        if self.clock.elapsed_time > sf.seconds(1):
            self.clock.restart()
            self.view_index += 1
            if self.view_index == len(self.view_list):
                self.view_index = 0
                
            self.mode="init_display_list"
            
    def display_julia(self):
        
        x,y = self.mouse.get_position()
        
        pix_size = ( self.xend - self.xstart ) / float(self.win.size.x)
        yend = self.ystart + (pix_size * float(self.win.size.y))
        
        c_real = self.xstart +  (float(x)/float(self.win.size.x))*(self.xend-self.xstart)
        c_imag = self.ystart +  (float(y)/float(self.win.size.y))*(yend-self.ystart)
     
        self.julia.calc(c_real, c_imag, 120)
        self.julia.build_texture()
        self.jsprite=sf.Sprite(self.julia.get_render_tex())
        self.jsprite.position=sf.Vector2(self.win.size.x*0.75-20,20)
        
        self.win.clear(self.backgnd)
        states = sf.RenderStates()
        if self.use_shader:
            states.shader = self.cycle.shader
        self.win.draw(self.screen_spr, states)
        self.win.draw(self.jsprite,states)
        self.debug.display("x : %s  y: %s   C real %s  : C imag %s  " % (x,y, c_real, c_imag))
        self.win.display()
        self.cycle.update(self.step)
    
        x,y=self.julia_coord_list[-1]
        if c_real <> x and c_imag <> y:
            self.julia_coord_list.append((c_real,c_imag))
            
    def replay_julia(self):
        
        if self.replay_index==None:
            self.replay_index=1
        else:
        
            c_real, c_imag =self.julia_coord_list[self.replay_index]
     
            self.julia_full.calc(c_real, c_imag, 120)
            self.julia_full.build_texture()
            self.jsprite=sf.Sprite(self.julia_full.get_render_tex())
            
            self.win.clear(self.backgnd)
            states = sf.RenderStates()
            if self.use_shader:
                states.shader = self.cycle.shader
            self.win.draw(self.jsprite,states)
            self.win.display()
            self.cycle.update(self.step)
            
            self.julia_replay_img_list.append(copy.copy(self.julia_full.get_render_tex()))
            self.replay_index+=1
            if self.replay_index==len(self.julia_coord_list):
                self.replay_index=None
                self.mode="fast_replay_julia"
                
    
    def fast_replay_julia(self):
        
        if self.replay_index==None:
            self.replay_index=1
        else:
        
            self.jsprite=sf.Sprite(self.julia_replay_img_list[self.replay_index])
          
            self.win.clear(self.backgnd)
            states = sf.RenderStates()
            if self.use_shader:
                states.shader = self.cycle.shader
            self.win.draw(self.jsprite,states)
            self.win.display()
            self.cycle.update(self.step)
            sf.sleep(sf.milliseconds(30))
            self.replay_index+=1
            if self.replay_index==len(self.julia_replay_img_list):
                self.replay_index=1
          
    def run(self):
        
        
        win=self.win

        self.iters=2500 
        self.xstart=-2.5
        self.xend=2.5
        self.ystart=-1.5
        self.n_xstart, self.n_xend, self.n_ystart= self.xstart, self.xend, self.ystart
        self.s_xstart, self.s_xend, self.s_ystart, self.s_iters= self.xstart, self.xend, self.ystart, self.iters
        
        self.mode="calc"

        while win.is_open: 
                        
            if self.mode=="calc":
                
                self.calculate()       
            
            elif self.mode=="user_zoom":    

                self.user_zoom()
                  
            elif self.mode=="init_display_list":
                
                self.init_display_list()
               
            elif self.mode=="display_list":
                
                self.display_list()
                
            elif self.mode=="julia":
                
                self.display_julia()     
    
            elif self.mode=="replay_julia":
                
                self.replay_julia()  
                
            elif self.mode=="fast_replay_julia":
                
                self.fast_replay_julia()        
            
            self.handle_events()                   
 
  
#####################################################################################################

app=App(0)
app.run()
