@echo off
echo Limpiando archivos de la carpeta Descargas que no comienzan con 'AZ-' o 'CC-'...

cd /d "%USERPROFILE%\Downloads"

:: Recorre todos los archivos en la carpeta
for %%f in (*) do (
    set "filename=%%~nxf"
    call :check_and_delete "%%~nxf"
)

:: Elimina carpetas como antes
for /d %%x in (*) do rd /s /q "%%x"

echo Limpieza completada.
exit /b

:check_and_delete
set "name=%~1"
setlocal enabledelayedexpansion

:: Evalúa si el archivo comienza con AZ- o CC-
set "prefix=!name:~0,3!"

if /i not "!prefix!"=="AZ-" if /i not "!prefix!"=="CC-" (
    echo Eliminando !name!
    del /q /f "!name!"
) else (
    echo Conservando !name!
)

endlocal
goto :eof
