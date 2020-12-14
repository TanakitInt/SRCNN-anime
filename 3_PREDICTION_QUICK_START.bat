@ECHO ON
py delete-old-file.py
timeout 3
py user-input.py
timeout 3
py bicubic.py
timeout 3
py predict-enhance.py
timeout 3
py predict-bicubic-enhance.py
timeout 3
py image-quality-assessment.py
timeout 10

