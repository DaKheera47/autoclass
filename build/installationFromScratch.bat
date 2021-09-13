Title AutoClass By Shaheer Sarfaraz -- Please Be Patient
@REM elevating to admin
@REM https://stackoverflow.com/questions/6811372/how-to-code-a-bat-file-to-always-run-as-admin-mode/45382540
set filepath=%~dp0
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )

@REM installing choco
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

call RefreshEnv.cmd

@REM installing packages
choco install obs-studio zoom git -y
choco install python -y

@REM refreshing path variables
call RefreshEnv.cmd

@REM cd to initial path
cd /d %filepath%
echo %filepath%

@REM getting from git
git clone https://github.com/DaKheera47/scheduled-class-launcher.git

cd scheduled-class-launcher/build
echo %cd%

start cmd /c scheduledClassLauncher.bat
exit
