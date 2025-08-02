@echo off
echo ==========================
echo Liberando memoria en Windows
echo ==========================

:: 1. Cerrar procesos comunes que consumen RAM
echo Cerrando procesos innecesarios...

taskkill /F /IM OneDrive.exe >nul 2>&1
taskkill /F /IM msedge.exe >nul 2>&1
taskkill /F /IM Widgets.exe >nul 2>&1
taskkill /F /IM Copilot.exe >nul 2>&1

:: 2. Limpiar carpeta temporal
echo Limpiando archivos temporales...
del /q /f /s "%TEMP%\*" >nul 2>&1

:: 3. Ejecutar CleanMgr con configuración personalizada
echo Ejecutando el Liberador de espacio en disco (cleanmgr)...
cleanmgr /sagerun:1

:: 4. Reiniciar el Explorador de Windows (explorer.exe)
echo Reiniciando el Explorador de Windows...
taskkill /f /im explorer.exe >nul 2>&1
timeout /t 2 >nul
start explorer.exe

:: 5. Fin
echo.
echo ✅ Memoria y espacio temporal liberados.
echo Puedes cerrar esta ventana.
