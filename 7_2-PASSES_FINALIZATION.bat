@ECHO ON
py img-final-denoise.py
timeout 3
py user-output.py
timeout 10

