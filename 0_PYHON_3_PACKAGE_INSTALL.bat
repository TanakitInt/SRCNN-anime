@ECHO ON
pip install --upgrade pip
timeout 3
pip install -r _requirements/requirements.txt
timeout 3
conda install --file _requirements/conda.txt

