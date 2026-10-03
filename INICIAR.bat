@echo off
chcp 65001 >nul 2>nul
setlocal
title Panel Zenn Factory - video-gen
cd /d "%~dp0"

echo ==========================================================
echo    PANEL ZENN FACTORY  -  El Porque
echo    Carpeta: %~dp0
echo ==========================================================
echo.

set "PY=%~dp0.venv\Scripts\python.exe"
set "ST=%~dp0.venv\Scripts\streamlit.exe"

if exist "%PY%" goto env_ok

echo [1/3] Creando entorno virtual e instalando dependencias...
where uv >nul 2>nul
if not errorlevel 1 (
    uv venv ".venv" --python 3.11
    if errorlevel 1 goto fail
    uv pip install --python "%PY%" -r requirements.txt
    if errorlevel 1 goto fail
    goto env_ok
)
where py >nul 2>nul
if not errorlevel 1 (
    py -3 -m venv .venv
    if errorlevel 1 goto fail
    "%PY%" -m pip install --upgrade pip
    if errorlevel 1 goto fail
    "%PY%" -m pip install -r requirements.txt
    if errorlevel 1 goto fail
    goto env_ok
)

echo.
echo ERROR: no hay ni uv ni Python 3 instalados.
echo   Opcion A - uv:      powershell -c "irm https://astral.sh/uv/install.ps1 ^| iex"
echo   Opcion B - Python:  https://www.python.org/downloads/
goto fail

:env_ok
echo [1/3] Entorno OK  (%PY%)
"%PY%" -c "import manim, edge_tts, piper" >nul 2>nul
if errorlevel 1 (
    echo       Instalando dependencias faltantes ^(Manim, voces y demas^)...
    where uv >nul 2>nul
    if not errorlevel 1 (
        uv pip install --python "%PY%" -r requirements.txt
    ) else (
        "%PY%" -m pip install -r requirements.txt
    )
    if errorlevel 1 goto fail
)

if exist "%~dp0panel.db" goto db_ok
echo [2/3] Creando base de datos (seed)...
"%PY%" seed.py
if errorlevel 1 goto fail
goto db_done

:db_ok
echo [2/3] Base de datos ya existe (panel.db)

:db_done
where ffmpeg >nul 2>nul
if errorlevel 1 (
    echo [3/3] AVISO: ffmpeg no esta en el PATH - el ensamblado y los shorts no funcionaran.
) else (
    echo [3/3] ffmpeg OK
)

if exist "%~dp0ARRANCAR_OLLAMA.bat" (
    call "%~dp0ARRANCAR_OLLAMA.bat"
) else (
    echo       INFO: sin ARRANCAR_OLLAMA.bat  ^(opcional, modelos locales^).
)

echo.
echo ----------------------------------------------------------
echo   Abriendo el panel:  http://localhost:8501
echo   Para pararlo:       Ctrl+C en esta ventana
echo ----------------------------------------------------------
echo.
"%ST%" run app.py --server.port 8501
if errorlevel 1 goto fail
goto end

:fail
echo.
echo *** Hubo un error. Revisa los mensajes de arriba. ***
pause
exit /b 1

:end
endlocal
