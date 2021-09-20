Title AutoClass By Shaheer Sarfaraz -- Updating
@REM elevating to admin
@REM https://stackoverflow.com/questions/6811372/how-to-code-a-bat-file-to-always-run-as-admin-mode/45382540
set filepath=%~dp0
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )

if exist "%temp%\config" rmdir "%temp%\config"
mkdir "%temp%\config"
move "..\config\*" "%temp%\config\"

cd ..
@REM https://stackoverflow.com/questions/1125968/git-how-do-i-force-git-pull-to-overwrite-local-files
git reset --hard origin/master
git pull

cd build
git clone https://github.com/DaKheera47/scheduled-class-launcher.git
python update.py

del /f /s /q "./scheduled-class-launcher" 1>nul
rmdir /s /q "./scheduled-class-launcher"

move "%temp%\config\*" "..\config\"
pause
