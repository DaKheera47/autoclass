Title AutoClass By Shaheer Sarfaraz -- Manual Class Mode
@REM elevating to admin
@REM https://stackoverflow.com/questions/6811372/how-to-code-a-bat-file-to-always-run-as-admin-mode/45382540
set filepath=%~dp0
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )

pip install -r ../requirements.txt
python ../launcher.py
echo "[31mAn error occured. Please save a screenshot of the text above as a crash report."
pause
