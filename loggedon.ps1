$ComputerName = Read-Host ″Enter remote computer name″
$credential = Get-Credential

Get-WMIObject Win32_Process -filter ‘name=″explorer.exe″’ -computername $computername -Credential $credential |
ForEach-Object {
$owner = $_.GetOwner()
‘{0}\{1}’ -f $owner.Domain, $owner.User} |
Sort-Object |
Get-Unique |
ForEach-Object {
$rv = 1 | Select-Object ComputerName, User
$rv.ComputerName = $computername
$rv.User = $_
$rv
}