# cython-mandelbrot

Mandelbrot visualisations with cython/SFML
==========================================

Requires PySFML, Numpy and Cython

Old school Fractint-style colour cycling using fragment shader in cycleshader.py
Heavy computations are done by cython extensions mandel2.pyx, julia.pyx utilising Cython's parallelisation features,
 - so is nice and fast. Draws a full screen unzoomed set in ~0.2s on 8-core Intel i7.

Set calculation code taken from http://aroberge.blogspot.co.uk/2010/01/profiling-adventures-and-cython.html

-  Mouse left        draw zoom rectangle
-  Mouse right/ENTER recalculate zoomed area
-  C                 randomize colour cycle palette
-  J                 switch to Julia mode, use mouse to view Julias at various set coords.
-  SPACE             switch to zoom mode
-  [                 slow down colour cycling
-  ]                 speed up colour cycling
-  UP                increase iterations
-  DOWN              decrease iterations
-  LEFT              increase palette change frequency
-  RIGHT             decrease palette change frequency
-  ESC               quit
