Title AutoClass By Shaheer Sarfaraz -- Updating
@REM elevating to admin
@REM https://stackoverflow.com/questions/6811372/how-to-code-a-bat-file-to-always-run-as-admin-mode/45382540
set filepath=%~dp0
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )

cd ..
@REM https://stackoverflow.com/questions/1125968/git-how-do-i-force-git-pull-to-overwrite-local-files
git reset --hard origin/master
git pull

pause
