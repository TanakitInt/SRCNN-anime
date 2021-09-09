@ECHO ON
py prepare-data-resize-0.5.py
timeout 3
py prepare-data-sharpening.py
timeout 3
py prepare-data-to-h5.py
timeout 10

