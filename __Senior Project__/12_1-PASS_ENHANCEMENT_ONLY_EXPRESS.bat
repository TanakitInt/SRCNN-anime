@ECHO ON
py tf-test.py

py delete-old-file.py

py user-input.py

py predict-enhance.py

py image-quality-assessment.py

py img-denoise.py

py user-output.py
timeout 5

