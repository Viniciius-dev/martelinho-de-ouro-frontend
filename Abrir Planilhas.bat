@echo off
title Automacao de Planilhas
cd /d "%~dp0"
echo.
echo  ===================================
echo   Abrindo Automacao de Planilhas...
echo  ===================================
echo.
streamlit run app.py
pause
