@echo off
setlocal
cd /d "%~dp0.."
python scripts\build_qesr_phase_sequence.py %*
pause
