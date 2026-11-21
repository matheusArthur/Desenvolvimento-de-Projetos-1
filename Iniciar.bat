@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    where py >nul 2>&1
    if errorlevel 1 (
        python -m venv .venv
    ) else (
        py -m venv .venv
    )
    if errorlevel 1 goto falha
)
".venv\Scripts\python.exe" -c "import flask" >nul 2>&1
if errorlevel 1 (
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto falha
)
if not defined PORT set "PORT=5000"
echo Abra http://127.0.0.1:%PORT% no navegador.
echo Deixe esta janela aberta enquanto usa o projeto.
".venv\Scripts\python.exe" app.py
if errorlevel 1 goto falha
exit /b 0

:falha
echo Confira a mensagem de erro acima e o arquivo README.md.
pause
exit /b 1
