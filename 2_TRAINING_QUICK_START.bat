@ECHO ON
py tf-test.py
timeout 3
py train-model.py
timeout 300

