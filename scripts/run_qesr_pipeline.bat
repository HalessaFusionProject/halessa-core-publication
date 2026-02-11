@echo off
setlocal
cd /d "%~dp0.."

python scripts\build_phase_previews.py --registry data\config\phase_preview_registry.json
python scripts\build_phase_meshes.py --registry data\config\phase_mesh_registry.json
python scripts\build_qesr_phase_sequence.py

where jupyter-nbconvert >nul 2>&1
if %errorlevel%==0 goto run_nbconvert
python -m nbconvert --version >nul 2>&1
if %errorlevel%==0 goto run_nbconvert_module
echo Skipping notebook validation (nbconvert not found).
goto after_nb

:run_nbconvert
jupyter-nbconvert --to notebook --execute src\notebooks\validate_phase_outputs.ipynb --output-dir results --output validate_phase_outputs_run.ipynb
goto after_nb

:run_nbconvert_module
python -m nbconvert --to notebook --execute src\notebooks\validate_phase_outputs.ipynb --output-dir results --output validate_phase_outputs_run.ipynb

:after_nb

python scripts\audit_phase_fields.py
echo Pipeline complete.
