'''
Created on 28 Jul 2015

@author: nick
'''
import sfml as sf
import math

class CycleShader(object):


    def __init__(self, win, colour_lookup_tex, kal_mode=False ):
        
        self.win=win
        
        self.vert="""
        
        void main()
        {
            vec4 vertex = gl_Vertex;
            gl_Position = gl_ModelViewProjectionMatrix * vertex;
            gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
            gl_FrontColor = gl_Color;
        }
        """       
        self.frag="""
        
        uniform sampler2D texture;
        uniform sampler2D colorTable;
        uniform float paletteIndex;
        uniform vec2 scr_centre;
        
        void main()
        {
                float Bright=-0.2f;
 
                
                vec2 pos = gl_TexCoord[0].st; 
               
                vec4 pixel = texture2D(texture, pos.xy);  
                float pi = ( pixel.r > 0.0 ) ? paletteIndex : 0.0 ;
                vec2 index = vec2(pixel.r+pixel.g+pixel.b+pi,0)/vec2(4.0,0);
                vec4 indexedColor = ( pixel.r > 0.0) ? texture2D(colorTable, index): vec4(0.0,0.0,0.0,255.0);
                pixel =  indexedColor;
                pixel.rgb = pixel.rgb + vec3(Bright,Bright,Bright) ;
                
                //pixel.rgb = ((pixel.rgb - 0.5f) * max(Contrast, 0)) + 0.5f;
       
                gl_FragColor =  gl_Color * (pixel);
         }
        """
        
        
        self.frag2="""
        
        uniform sampler2D texture;
        uniform sampler2D colorTable;
        uniform float paletteIndex;
        uniform vec2 scr_centre;
        
        void main()
        {
                float Bright=-0.2f;
 
                
                vec2 pos = gl_TexCoord[0].st; 
                vec2 scrpos = gl_FragCoord.xy;
                float dist = distance(scrpos,scr_centre)/410.0 ;
                
                vec4 pixel = texture2D(texture, pos.xy);  
                float pi = ( pixel.r > 0.0 ) ? paletteIndex : 0.0 ;
                vec2 index = vec2(pixel.r+pixel.g+pixel.b+pi,0)/vec2(4.0,0);
                vec4 indexedColor = ( pixel.r > 0.0) ? texture2D(colorTable, index): vec4(0.0,0.0,0.0,255.0);
                pixel =  indexedColor;
                pixel.rgb = pixel.rgb / max(dist,0.5);   //+ vec3(Bright,Bright,Bright) * dist;
                
                //pixel.rgb = ((pixel.rgb - 0.5f) * max(Contrast, 0)) + 0.5f;
       
                gl_FragColor =  gl_Color * (pixel);
         }
        """
        frag=self.frag2 if kal_mode else self.frag 
        
        try:
            self.shader=sf.Shader.from_memory(vertex=self.vert, fragment=frag)
        except IOError as e:
            print "Shader loader exception : \n", e
            raise
            
        self.shader.set_texture_parameter("colorTable", colour_lookup_tex )
        self.shader.set_1float_parameter("paletteIndex", 0 )
        self.shader.set_2float_parameter("scr_centre", win.size.x / 2, win.size.y / 2);
        self.pal_length=colour_lookup_tex.width
        self.index=0.0
    
    def set_color_table(self, tex):
        
        self.shader.set_texture_parameter("colorTable", tex )
           
    def update(self,step):
        
        self.index+=step
        if self.index >1.00:
            self.index=0.0
        self.shader.set_1float_parameter("paletteIndex", self.index )
        
        
    #def update(self,time):
         
         #self.shader.set_1float_parameter("time",   time/30000.0)
            
        
 
 
 
    

        