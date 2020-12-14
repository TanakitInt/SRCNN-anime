@ECHO ON
py tf-test.py

py delete-old-file.py

py user-input.py

py bicubic.py

py predict-enhance.py

py predict-bicubic-enhance.py

py image-quality-assessment.py

py img-denoise.py

py img-bicubic-denoise.py

py user-output.py
timeout 5

