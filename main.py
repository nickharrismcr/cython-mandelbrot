'''
Created on 26 Jul 2015

@author: nick
'''

import sfml as sf, mandel2, cycleshader, debug, mandel_py,random, math, julia, copy,os,datetime,time
import kaleidoscope

WINDOWED=1
FULLSCREEN=0

#####################################################################################################
class App():
    
    def __init__(self, mode=FULLSCREEN):
        
        cont=sf.ContextSettings(antialiasing=3)
        self.winmode=mode
        if mode!=WINDOWED:
            win = sf.RenderWindow(sf.VideoMode.get_desktop_mode(), "Mandel", sf.window.Style.FULLSCREEN, cont )
        else:
            d_mode=sf.VideoMode.get_desktop_mode()
            w=d_mode.width
            h=d_mode.height
            h*=0.9
            w*=0.8
            win = sf.RenderWindow(sf.VideoMode(w,h), "Mandel"  )  
            
        win.vertical_synchronization = True
        win.framerate_limit = 60
        
        self.win=win
        self.win.key_repeat_enabled=False
        self.clock=sf.Clock()
        self.backgnd=sf.Color.BLACK
        self.aspect=float(win.height)/float(win.width)
        
        self.debug=debug.Debug(self.win)
        self.debugtimer=sf.Clock()
        self.mandelbrot2=mandel2.Mandelbrot2(self.win.size.x,self.win.size.y,10)
        self.julia=julia.Julia(self.win.size.x/2.0,self.win.size.y/2.0,10)
        self.julia_full=julia.Julia(self.win.size.x,self.win.size.y,10)
        self.cycle=cycleshader.CycleShader(win, self.mandelbrot2.get_palette_tex())
        self.screen_tex=sf.Texture.create(self.win.size.x, self.win.size.y)
        self.screen_tex.smooth=True
        
        
        self.init()
    
    def screenshot(self):
        
        try:
            os.mkdir(os.curdir+"/screenshots")
        except:
            pass
       
        ts=time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        filename=os.curdir+"/screenshots/mandelbrot_"+st+".bmp"
        self.win.capture().to_file(filename)
        return filename
        
    def init(self):
        
        self.cycle_switch=True
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
        self.j_x=0.0
        self.j_y=0.0
        self.dj=1.0
        self.julia_coord_list=[(0,0)]
        self.julia_replay_img_list=[]
        self.replay_index=None

        self.iters=2500 
        self.xstart=-2.5
        self.xend=2.5
        self.ystart=-1.5
        self.n_xstart, self.n_xend, self.n_ystart= self.xstart, self.xend, self.ystart
        self.s_xstart, self.s_xend, self.s_ystart, self.s_iters= self.xstart, self.xend, self.ystart, self.iters
        
        self.kal_mode=False
        self.show_palette=True
        self.mode="calc"
        
    def key_pressed(self,key):
        
        return type(self.event) is sf.KeyEvent and self.event.pressed and self.event.code is key

    def handle_events(self):
        
       
        
        for self.event in self.win.events:
            if type(self.event) is sf.CloseEvent:
                self.win.close()
                return False
            if self.key_pressed( sf.Keyboard.ESCAPE):
                self.win.close()
            if self.key_pressed( sf.Keyboard.UP):
                self.iters += 100
            if self.key_pressed( sf.Keyboard.DOWN):
                self.iters -= 100
            if self.key_pressed( sf.Keyboard.SPACE):
                self.mode = "calc"
            if self.key_pressed( sf.Keyboard.RETURN):
                self.mode = "calc"
            if self.key_pressed( sf.Keyboard.C):
                self.win.mouse_cursor_visible = False
                self.mandelbrot2.new_colours()
            if self.key_pressed( sf.Keyboard.L_BRACKET):
                self.step /= 1.1
            if self.key_pressed( sf.Keyboard.R_BRACKET):
                self.step *= 1.1
            if self.key_pressed( sf.Keyboard.S):
                self.start_display_list()
            if self.key_pressed( sf.Keyboard.K):
                self.kal_mode = not self.kal_mode
            if self.key_pressed( sf.Keyboard.LEFT):
                self.palette_down()
            if self.key_pressed( sf.Keyboard.RIGHT):
                self.palette_up()
            if self.key_pressed( sf.Keyboard.DELETE):
                self.use_shader = not self.use_shader
            if self.key_pressed( sf.Keyboard.J):
                self.mode="julia"
                x,y=self.mouse.get_position()
                self.j_x=float(x)
                self.j_y=float(y)
            if self.key_pressed( sf.Keyboard.R):
                self.replay_index=None
                self.mode="replay_julia"
            if self.key_pressed( sf.Keyboard.P):
                self.show_palette = not self.show_palette
                
        return True

    def calculate(self):
        
        self.view = self.win.default_view
        self.win.mouse_cursor_visible = False
        self.mandelbrot2.calc(self.xstart, self.xend, self.ystart, self.iters)
        self.mandelbrot2.build_texture()
        self.screen_tex=self.mandelbrot2.get_render_tex()
        self.screen_spr = sf.Sprite(self.screen_tex)
        settings={ "texture":self.screen_tex,  "position":sf.Vector2(self.win.size.x/2,self.win.size.y/2), "leaves":16,
                           "speed":1, "radius": self.win.size.y/2, "scale":1.0, "depth": 1, "bright":255  }
        self.kaleido1=kaleidoscope.Kaleidoscope(settings,self.win)
        settings2={ "texture":self.screen_tex,  "position":sf.Vector2(self.win.size.x/2,self.win.size.y/2), "leaves":16,
                           "speed":1, "radius": self.win.size.y/2, "scale":2.0, "depth": 1, "bright":200  }
        self.kaleido2=kaleidoscope.Kaleidoscope(settings2,self.win)
        self.view_list.append(None)
        self.debugtimer.restart()
        self.mode = "user_zoom"
       

    def user_zoom(self):
        
       
        self.win.mouse_cursor_visible = True
        self.win.clear(sf.Color.BLACK)
       
        states = sf.RenderStates()
        if self.use_shader:
            states.shader = self.cycle.shader
        if self.kal_mode:
            self.kaleido2.draw(self.win,states)
            self.kaleido1.draw(self.win,states)
        else:
            self.win.draw(self.screen_spr, states)
        if self.show_palette:
            self.mandelbrot2.draw_palette(self.win)
        if self.debugtimer.elapsed_time.seconds<2:
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
            if self.winmode==WINDOWED:
                x,y = self.mouse.get_position(self.win) 
            else:
                x,y = self.mouse.get_position()
               
            self.draw_box = True
            if not self.draw_area:
                self.draw_area = True
                self.box.position=sf.Vector2(x,y)
                self.box.size = sf.Vector2(2, 2)
            else:
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
        
        if self.cycle_switch:
            self.cycle.update(self.step)
        self.kaleido1.update()
        self.kaleido2.update()
        self.win.display()
        
    def start_display_list(self):
        
        self.view_index=0
        self.mode="init_display_list"
        
    def palette_down(self):
        
        self.mandelbrot2.speed += 1
        self.mandelbrot2.new_colours()
        self.cycle.set_color_table(self.mandelbrot2.get_palette_tex())
    
    def palette_up(self):
                
        self.mandelbrot2.speed -= 1 if self.mandelbrot2.speed > 1 else 0
        self.mandelbrot2.new_colours()
        self.cycle.set_color_table(self.mandelbrot2.get_palette_tex())

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
            if self.clock.elapsed_time.milliseconds > 1000.0:
                self.boxzoom=2
                
        elif self.boxzoom ==2 :
            
            fac=(self.clock.elapsed_time.milliseconds-1000.0) / 1000.0
            fac2=(math.sin((fac*0.5*math.pi)))
            x,y=self.endpos * fac2
            w,h=self.endsize + (self.startsize - self.endsize) * (1 - fac2)
            
            self.view.reset(sf.Rectangle((x,y),(w,h)))
            self.win.view=self.view
        
        
        self.win.display()
        if self.cycle_switch:
            self.cycle.update(self.step)
        
        if self.clock.elapsed_time > sf.seconds(2):
            self.clock.restart()
            self.view_index += 1
            if self.view_index == len(self.view_list):
                self.view_index = 0
                
            self.mode="init_display_list"
            
    def display_julia(self):
        
        if self.winmode==WINDOWED:
            x,y = self.mouse.get_position(self.win)
        else:
            x,y = self.mouse.get_position()
        
        self.j_x,self.j_y=x,y 
        
        pix_size = ( self.xend - self.xstart ) / float(self.win.size.x)
        yend = self.ystart + (pix_size * float(self.win.size.y))
        
        c_real = self.xstart +  (float(self.j_x)/float(self.win.size.x))*(self.xend-self.xstart)
        c_imag = self.ystart +  (float(self.j_y)/float(self.win.size.y))*(yend-self.ystart)
     
        self.julia.calc(c_real, c_imag, 520)
        self.julia.build_texture()
        self.jsprite=sf.Sprite(self.julia.get_render_tex())
        self.jsprite.position=sf.Vector2(self.win.size.x*0.5-20,20)
        
        self.win.clear(self.backgnd)
        states = sf.RenderStates()
        if self.use_shader:
            states.shader = self.cycle.shader
        self.win.draw(self.screen_spr, states)
        self.win.draw(self.jsprite,states)
        self.win.display()
        if self.cycle_switch:
            self.cycle.update(self.step)
    
        #x,y=self.julia_coord_list[-1]
        #if c_real <> x and c_imag <> y:
            #self.julia_coord_list.append((c_real,c_imag))
            
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
            self.julia_full.get_render_tex().to_image().to_file("julia_images/j_img_%s.png" % self.replay_index)
            if self.cycle_switch:
                self.cycle.update(self.step)
            
            self.replay_index+=1
            if self.replay_index==len(self.julia_coord_list):
                self.replay_index=None
                self.mode="fast_replay_julia"
                
    
    def fast_replay_julia(self):
        
        if self.replay_index==None:
            self.replay_index=1
        else:
         
            self.jsprite=sf.Sprite(sf.Texture.from_file("julia_images/j_img_%s.png" % self.replay_index))
            self.win.clear(self.backgnd)
            states = sf.RenderStates()
            if self.use_shader:
                states.shader = self.cycle.shader
            self.win.draw(self.jsprite,states)
            self.win.display()
            if self.cycle_switch:
                self.cycle.update(self.step)
            self.replay_index+=1
            if self.replay_index==len(self.julia_coord_list):
                self.replay_index=1
          
    def run(self):

        while self.win.is_open: 
            
            self.update()
            
    def update(self):
                    
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
        
        if not self.handle_events():
            return False
        
        return True                   
 
  
#####################################################################################################

#app=App(WINDOWED)
#app.run()
