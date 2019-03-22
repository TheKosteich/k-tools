# Author: Vladimir Eremin
# http://forums.veeam.com/member31097.html
# Moderator: Konstantin Tornovskiy
# Date of change: 23/12/2016
# 

##################################################################
#                   User Defined Variables
##################################################################

# Names of VMs to backup separated by semicolon (Mandatory)
$VMNames = 
#	"CA0233",
#	"KAV4206",
#	"NGmgmtFW-ZLVS",
#	"SPB25-SHELFKAV",
#	"spb25-shelfLdc",
#	"spb25-shelfpam",
#	"spb25-shelfsam",
#	"spb30-ibvc",
#	"spb30-shelf-bkpVM",
#	"spb30-shelf-certupd",
#	"spb30-shelf-ISE01",
#	"spb30-shelf-ISE02",
#	"spb30-shelfbh01",
#	"SPB30-SHELFKOZ",
#	"spb30-shelfmd",
#	"spb30-shelfrm",
	"spb30-shelfzab"

# Name of vCenter or standalone host VMs to backup reside on (Mandatory)
$HostName = "spb30-ibvc"

# Directory that VM backups should go to (Mandatory; for instance, C:\Backup)
$Directory = "D:\backup"

# Desired compression level (Optional; Possible values: 0 - None, 4 - Dedupe-friendly, 5 - Optimal, 6 - High, 9 - Extreme) 
$CompressionLevel = "5"

# Quiesce VM when taking snapshot (Optional; VMware Tools are required; Possible values: $True/$False)
$EnableQuiescence = $True

# Protect resulting backup with encryption key (Optional; $True/$False)
$EnableEncryption = $True

# Encryption Key (Optional; path to a secure string)
# Encryption key is - "2892dc3cd4c0f8430841b3ba0e3dccfc30d0069fed628c664efe608b1027421a"
$EncryptionKey = ConvertTo-SecureString "2892dc3cd4c0f8430841b3ba0e3dccfc30d0069fed628c664efe608b1027421a" -AsPlainText -Force
$EncryptionKey = Add-VBREncryptionKey -Password $EncryptionKey

# Retention settings (Optional; By default, VeeamZIP files are not removed and kept in the specified location for an indefinite period of time. 
# Possible values: Never , Tonight, TomorrowNight, In3days, In1Week, In2Weeks, In1Month)
$Retention = "In3days"

##################################################################
#                   Notification Settings
##################################################################

# Enable notification (Optional)
$EnableNotification = $False

# Email SMTP server
$SMTPServer = ""

# Email FROM
$EmailFrom = "" 

# Email TO
$EmailTo = ""

# Email subject
$EmailSubject = ""

##################################################################
#                   Email formatting 
##################################################################

$style = "<style>BODY{font-family: Arial; font-size: 10pt;}"
$style = $style + "TABLE{border: 1px solid black; border-collapse: collapse;}"
$style = $style + "TH{border: 1px solid black; background: #dddddd; padding: 5px; }"
$style = $style + "TD{border: 1px solid black; padding: 5px; }"
$style = $style + "</style>"

##################################################################
#                   End User Defined Variables
##################################################################

#################### DO NOT MODIFY PAST THIS LINE ################
Asnp VeeamPSSnapin

$Server = Get-VBRServer -name $HostName
$MesssagyBody = @()

foreach ($VMName in $VMNames)
{
  $VM = Find-VBRViEntity -Name $VMName -Server $Server
  
  If ($EnableEncryption)
  {
    $ZIPSession = Start-VBRZip -Entity $VM -Folder $Directory -Compression $CompressionLevel -DisableQuiesce:(!$EnableQuiescence) -AutoDelete $Retention -EncryptionKey $EncryptionKey
  }
  
  Else 
  {
    $ZIPSession = Start-VBRZip -Entity $VM -Folder $Directory -Compression $CompressionLevel -DisableQuiesce:(!$EnableQuiescence) -AutoDelete $Retention
  }
  
  If ($EnableNotification) 
  {
    $TaskSessions = $ZIPSession.GetTaskSessions().logger.getlog().updatedrecords
    $FailedSessions =  $TaskSessions | where {$_.status -eq "EWarning" -or $_.Status -eq "EFailed"}
  
  if ($FailedSessions -ne $Null)
  {
    $MesssagyBody = $MesssagyBody + ($ZIPSession | Select-Object @{n="Name";e={($_.name).Substring(0, $_.name.LastIndexOf("("))}} ,@{n="Start Time";e={$_.CreationTime}},@{n="End Time";e={$_.EndTime}},Result,@{n="Details";e={$FailedSessions.Title}})
  }
   
  Else
  {
    $MesssagyBody = $MesssagyBody + ($ZIPSession | Select-Object @{n="Name";e={($_.name).Substring(0, $_.name.LastIndexOf("("))}} ,@{n="Start Time";e={$_.CreationTime}},@{n="End Time";e={$_.EndTime}},Result,@{n="Details";e={($TaskSessions | sort creationtime -Descending | select -first 1).Title}})
  }
  
  }   
}
If ($EnableNotification)
{
$Message = New-Object System.Net.Mail.MailMessage $EmailFrom, $EmailTo
$Message.Subject = $EmailSubject
$Message.IsBodyHTML = $True
$message.Body = $MesssagyBody | ConvertTo-Html -head $style | Out-String
$SMTP = New-Object Net.Mail.SmtpClient($SMTPServer)
$SMTP.Send($Message)
}

