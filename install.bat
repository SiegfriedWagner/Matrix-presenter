python -m pip install --user --upgrade pip
python -m pip install --user virtualenv
setx /m PATH %PATH%;c:\users\%USERNAME%\appdata\local\programs\python\python37-32\Scripts
python -m virtualenv ./venv
call ./venv/Scripts/activate
python -m pip install -r ./requirements.txt
pause