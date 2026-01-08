@echo off
setlocal

REM --- Ruta correcta a pythonw.exe ---
set PYW="C:\Users\Usuario\AppData\Local\Programs\Python\Python310\pythonw.exe"

REM --- Directorio raíz del proyecto (carpeta donde está este .bat) ---
set ROOT=%~dp0

cd /d "%ROOT%"

REM --- Ejecutar run_gui.py sin consola ---
%PYW% "%ROOT%run_gui.py" 2>"%ROOT%startup_error.log"

REM --- Si hubo errores, mostrar mensaje ---
if exist "%ROOT%startup_error.log" (
    for %%A in ("%ROOT%startup_error.log") do if %%~zA GTR 0 (
        echo Ha ocurrido un error durante el arranque. 
        echo Revisa el archivo startup_error.log
        pause
        exit /b
    )
)

endlocal
exit
