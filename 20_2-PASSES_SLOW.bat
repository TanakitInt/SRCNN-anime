@ECHO ON
py tf-test.py
timeout 3
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
timeout 3
py img-denoise.py
timeout 3
py img-bicubic-denoise.py
timeout 3
py user-output.py
timeout 3
py reinput-2passes.py
timeout 3
py delete-old-file.py
timeout 3
py user-input.py
timeout 3
py predict-enhance.py
timeout 3
py image-quality-assessment.py
timeout 3
py img-denoise.py
timeout 3
py img-final-denoise.py
timeout 3
py user-output.py
timeout 10


