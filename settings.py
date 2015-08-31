import cPickle 

class Settings(object):
    
    def __init__(self):
        
        self.settings={}
    
    def save(self,app):
        self.settings["xstart"]=app.xstart
        self.settings["xend"]=app.xend
        self.settings["ystart"]=app.ystart
        self.settings["cyclestep"]=app.step
        self.settings["palette_pixels"]=app.mandelbrot2.palette_list
        self.settings["iterations"]=app.iters
    
    def to_file(self,file):    
        
        cPickle.dump(self.settings,file)
        
    def from_file(self,file):
        
        self.settings=cPickle.load(file)
        
    def load(self,app):
        
        app.xstart=self.settings["xstart"]
        app.xend=self.settings["xend"]
        app.ystart=self.settings["ystart"]
        app.cyclestep=self.settings["cyclestep"]
        app.mandelbrot2.load_colours(self.settings["palette_pixels"])
        app.iters=self.settings["iterations"]
        