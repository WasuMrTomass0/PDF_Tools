python -V
echo "Python 3.10 is preferred. Verify your Python version"
timeout 5
rmdir /s /q .\..\venv
python -m venv ..\venv
..\venv\Scripts\python.exe -m pip install -r ..\requirements.txt
..\venv\Scripts\python.exe -V
