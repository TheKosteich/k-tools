$Folder = switch ($args.count)
{
    0 {"."; break}
    1 {$args[0]; break}
}
if (!$Folder)
{
    "Неверное число параметров."
    exit
}

$SystemType = (Get-WmiObject -Class Win32_ComputerSystem | Select-Object -Property SystemType).SystemType
$SystemType = switch($SystemType)
{
    "X86-based PC" {"x86"; break}
    "x64-based PC" {"x64"; break}
    "64-bit Intel PC" {"ia64"; break}
}
if (!$SystemType)
{
    "Тип системы не поддерживается."
    exit
}

$Version = (Get-WmiObject -Class Win32_OperatingSystem | Select-Object -Property Version).Version
$Version = $Version -split ".", 0, "simplematch"
$MajorMinor = $Version[0] + '.' + $Version[1]

$FileMask = switch ($MajorMinor)
{
    # Windows XP (x86)
    "5.1" {"WindowsXP-KB*-$SystemType-*.exe"; break}
    #Windows 2003 (x86)
    "5.2" {"WindowsServer2003-KB*-$SystemType-*.exe"; break}
    #Windows Vista, Server 2008 (all)
    "6.0" {"Windows$MajorMinor-KB*-$SystemType-*.msu"; break}
    #Windows 7, Server 2008 R2 (all)
    "6.1" {"Windows$MajorMinor-KB*-$SystemType-*.msu"; break}
}
if (!$FileMask)
{
    "Данная версия операционной системы не поддерживается."
    exit
}

$Shell = New-Object -com WScript.Shell
"Выполняется установка следующих обновлений:"
Get-ChildItem "$Folder\*" -Include "$FileMask" -Recurse | ForEach-Object {
    "  - " + $_.Name
    $NameAndParam = '"'+$_.FullName+'" /quiet /norestart'
    $Shell.Run($NameAndParam, 0, "true") | Out-Null
}
"Установка обновлений завершена!"