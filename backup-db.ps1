# Prosty skrypt do backupu bazy danych w PowerShell

$DbName = "app_database"
$BackupDir = "C:\backups\db"
$Date = Get-Date -Format "yyyyMMdd_HHmmss"
$SqlFile = Join-Path -Path $BackupDir -ChildPath "${DbName}_${Date}.sql"
$GzFile = "${SqlFile}.gz"

# Sprawdź czy katalog istnieje
if (-not (Test-Path -Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    Write-Host "Utworzono katalog $BackupDir"
}

# Wykonaj backup
Write-Host "Rozpoczynam backup bazy $DbName..."

# Zrzut bazy danych mysqldump do pliku .sql
cmd /c "mysqldump -u root -p $DbName > `"$SqlFile`""

if ($LASTEXITCODE -eq 0 -and (Test-Path -Path $SqlFile)) {
    # Kompresja pliku .sql do formatu .gz przy użyciu natywnych klas .NET
    $inputStream = [System.IO.File]::OpenRead($SqlFile)
    $outputStream = [System.IO.File]::Create($GzFile)
    $gzipStream = [System.IO.Compression.GZipStream]::new($outputStream, [System.IO.Compression.CompressionMode]::Compress)
    
    $inputStream.CopyTo($gzipStream)
    
    $gzipStream.Dispose()
    $outputStream.Dispose()
    $inputStream.Dispose()

    # Usunięcie nieskompresowanego pliku tymczasowego
    Remove-Item -Path $SqlFile -Force

    Write-Host "Backup zakończony sukcesem: $GzFile"
} else {
    Write-Error "Błąd podczas wykonywania backupu!"
    exit 1
}