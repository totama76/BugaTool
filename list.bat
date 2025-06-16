@echo off
setlocal EnableDelayedExpansion

REM Comprueba si estamos en un repositorio Git
git rev-parse --is-inside-work-tree >nul 2>&1
IF ERRORLEVEL 1 (
    echo No estas en un repositorio Git.
    exit /b 1
)

REM Listar los últimos 20 commits en formato hash y mensaje
echo ================================
echo Lista de commits (últimos 20):
echo ================================
git log --oneline -n 20

REM Pedir al usuario que introduzca el hash
set /p commitHash=Introduce el hash del commit al que quieres hacer checkout (solo los primeros caracteres son suficientes):

REM Confirmación
echo Vas a hacer checkout al commit: %commitHash%
set /p confirm=¿Confirmar? (s/n): 

IF /I NOT "%confirm%"=="s" (
    echo Cancelado por el usuario.
    exit /b 0
)

REM Ejecutar el checkout
git checkout %commitHash%
IF ERRORLEVEL 1 (
    echo Error al hacer checkout. ¿Seguro que el hash es correcto?
    exit /b 1
)

echo Checkout realizado correctamente en estado detached.
echo Usa ^`git checkout main^` para volver a la rama principal.



REM -------------------------------------------------------







REM ira a una version
REM git checkout f3a4e1c


REM ir a la ultima
REM git checkout main



REM Rama
REM git checkout -b rama-desde-viejo f3a4e1c


REM clonar en otra carpeta
REM git clone https://github.com/tu-usuario/repositorio.git carpeta-temporal
REM cd carpeta-temporal
REM git checkout f3a4e1c
