@Echo Off
Title Installing Windows 7 updates
For %%F In (MSU\*.msu) Do Call :msin %%F
For %%A In (CAB\*.cab) Do Call :kbin %%A
Exit
:msin
Start /Wait %1 /quiet /norestart
:kbin
Start /Wait pkgmgr /ip /m:%1 /quiet /norestart
GoTo :EOF
Exit