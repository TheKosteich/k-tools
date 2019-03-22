@echo OFF

reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\Results\Install" /v LastSuccessTime > C:\tmp\upd.txt

FOR /F "usebackq skip=2 tokens=1-6" %%A IN (C:\tmp\upd.txt) DO (
    @echo %%C > C:\tmp\upd_time.txt
    set LAST_UPDATE=%%C
)

del C:\tmp\upd.txt