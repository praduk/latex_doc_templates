@echo off
py -3 -c "import sys; raise SystemExit(sys.version_info ^< (3, 9))" >nul 2>nul
if errorlevel 1 goto try_python
py -3 "%~dp0build.py" %*
exit /b %errorlevel%

:try_python
python -c "import sys; raise SystemExit(sys.version_info ^< (3, 9))" >nul 2>nul
if errorlevel 1 goto no_python
python "%~dp0build.py" %*
exit /b %errorlevel%

:no_python
echo Python 3.9 or newer was not found. 1>&2
exit /b 1
