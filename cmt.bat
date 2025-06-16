@echo off
REM Comprueba que se ha proporcionado un mensaje de commit
IF "%~1"=="" (
    echo Uso: git_commit.bat "Mensaje del commit"
    exit /b 1
)

REM Añade todos los cambios
git add .

REM Hace el commit con el mensaje proporcionado
git commit -m "%~1"

REM Sube a la rama actual (por defecto main)
git push

REM Mensaje de éxito
echo Commit realizado y enviado correctamente.
