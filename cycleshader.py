'''
Created on 28 Jul 2015

@author: nick
'''
import sfml as sf
import math

class CycleShader(object):


    def __init__(self, win, colour_lookup_tex ):
        
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

        void main()
        {
                vec2 pos= gl_TexCoord[0].st; 
                vec4 pixel = texture2D(texture, pos.xy);  
                float pi = ( pixel.r > 0.0 ) ? paletteIndex : 0.0 ;
                vec2 index = vec2(pixel.r+pixel.g+pixel.b+pi,0)/vec2(4.0,0);
                vec4 indexedColor = ( pixel.r > 0.0) ? texture2D(colorTable, index): vec4(0.0,0.0,0.0,255.0);
                gl_FragColor =  gl_Color * (indexedColor);
         }
        """
        
        
        self.frag2="""
        
        uniform sampler2D texture;
        uniform float time;
        
        vec3 rgb2hsv(vec3 c)
        {
            vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
            vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
            vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
        
            float d = q.x - min(q.w, q.y);
            float e = 1.0e-10;
            return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
        }
         
        
        vec3 hsv2rgb(vec3 c)
        {
            vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
            vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
            return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
        }
        
        float rand(vec2 co){
          return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 137.5453);
        }
        
        void main()
        {
            float M_PI=3.14159265358;
        
            vec2 pos= gl_TexCoord[0].st; 
            vec4 pixel = texture2D(texture, pos.xy);  
            vec3 hsv  =rgb2hsv(pixel.rgb);
            hsv.x=sin((time*2.0)+hsv.x);
            
            pixel.rgb=hsv2rgb(hsv);
        
            //float r= abs(cos(time*1.4));
            //float g= abs(cos(M_PI/4.0+(time*2.5)));
            //float b= abs(cos(M_PI/2.0+(time*3.6)));
        
        
        
            //pixel.rgb=vec3(pixel.r*r,pixel.g*g,pixel.b*b);
        
            gl_FragColor =  gl_Color * (pixel);
        }
        """
        
        try:
            self.shader=sf.Shader.from_memory(vertex=self.vert, fragment=self.frag)
        except IOError as e:
            print "Shader loader exception : \n", e
            raise
            
        self.shader.set_texture_parameter("colorTable", colour_lookup_tex )
        self.shader.set_1float_parameter("paletteIndex", 0 )
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
            
        
 
 
 
    

        