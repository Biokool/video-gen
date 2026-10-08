@echo off
chcp 65001 >nul 2>nul
setlocal
title Ollama modo CPU - video-gen

:: El driver NVIDIA de esta maquina (546.29, 2023) no compila el PTX de
:: los builds CUDA de Ollama -> "PTX JIT compilation failed" y NINGUN
:: modelo arranca. Fuerza la libreria CPU (con driver 560+ puedes borrar
:: estas dos lineas para usar la GTX 1050).
set "OLLAMA_LLM_LIBRARY=cpu"
set "CUDA_VISIBLE_DEVICES="

curl -s -m 2 http://localhost:11434/api/tags >nul 2>nul
if not errorlevel 1 (
    echo Ollama ya esta corriendo en localhost:11434
    echo Si los modelos fallan con "PTX JIT compilation failed", cierra
    echo el Ollama actual y vuelve a lanzar este .bat.
    exit /b 0
)

echo Arrancando Ollama en modo CPU (el primer modelo tarda en cargar)...
start "" /min ollama serve

set /a intentos=0
:wait
timeout /t 2 /nobreak >nul
curl -s -m 2 http://localhost:11434/api/tags >nul 2>nul
if not errorlevel 1 goto ready
set /a intentos+=1
if %intentos% lss 20 goto wait
echo AVISO: Ollama no respondio en 40s. Revisa que "ollama" este en el PATH.
exit /b 0

:ready
echo Listo: los modelos locales ya se pueden elegir en el panel
echo   (sidebar Modelo ^> Backend ^> Ollama - local).

endlocal
exit /b 0
