# cython-mandelbrot

Mandelbrot visualisations with cython/SFML
==========================================

Requires PySFML, Numpy and Cython

Old school Fractint-style colour cycling using GLSL fragment shader.
Julia mode for exploring the Julia set.
Mandala mode for psychedelic visuals.
Heavy computations are done by cython extensions mandel2.pyx, julia.pyx utilising Cython's parallelisation features.
Set calculation code taken from http://aroberge.blogspot.co.uk/2010/01/profiling-adventures-and-cython.html

-  Mouse left        draw zoom rectangle
-  Mouse right/ENTER recalculate zoomed area
-  C                 randomize colour cycle palette
-  J                 switch to Julia mode, use mouse to view Julias at various set coords.
-  K                 toggle mandala mode 
-  SPACE             switch to zoom mode
-  D                 play loop of smooth zoom from top level into coordinates previously viewed
-  [                 slow down colour cycling
-  ]                 speed up colour cycling
-  UP                increase iterations
-  DOWN              decrease iterations
-  LEFT              increase palette change frequency
-  RIGHT             decrease palette change frequency
-  ESC               quit
