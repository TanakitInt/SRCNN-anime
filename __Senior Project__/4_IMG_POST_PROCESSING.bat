@ECHO ON
py img-denoise.py
timeout 3
py img-bicubic-denoise.py
timeout 10

