Param(
  [string]$LOG_PATH = "${PWD}\logs",
  [string]$LOG_PEFIX = "test",
  [string]$LOG_SUFFIX = ".log",
  [string]$ADDRESS = ( Get-Content .\host.address -Raw ),
  [string]$FILES_TO_COPY = "app.py",
  [string]$COMMAND = "docker run -it --rm -v ${PWD}:/build/source:rw -v ${HOME}/.ssh:/build/.ssh:ro aemdesign/centos-java-buildpack bash --login /build/source/docker-copy.sh ""/build/source/${FILES_TO_COPY}"" ""${ADDRESS}""",
  [string]$WATCH_PATH = ".",
  [string]$WATCH_FILES_PATTERN = "*",
  [boolean]$WATCH_SUBFOLDERS = $true,
  [int]$WATCH_TIMEOUT = 1000,
  [string]$FUNCTIONS_URI = "https://github.com/aem-design/aemdesign-docker/releases/latest/download/functions.ps1"
)

$SKIP_CONFIG = $true
$PARENT_PROJECT_PATH = "."

. ([Scriptblock]::Create((([System.Text.Encoding]::ASCII).getString((Invoke-WebRequest -Uri "${FUNCTIONS_URI}").Content))))

function Invoke-ChangeAction
{
  param
  (
    [Parameter(Mandatory)]
    [System.IO.WaitForChangedResult]
    $Change
  )

  Write-Warning 'Change detected:'
  $Change | Out-String | Write-Warning

  Invoke-Expression -Command "$COMMAND" | Tee-Object -Append -FilePath "${LOG_FILE}"

}



# find the path to watch
$WATCH_FOLDER = Resolve-Path "${WATCH_PATH}"
# specify the file or folder properties you want to monitor
$WATCH_ATTRIBUTE_FILTER = [IO.NotifyFilters]::FileName, [IO.NotifyFilters]::LastWrite
# specify the type of changes you want to monitor
$WATCH_CHANGE_TYPES = [System.IO.WatcherChangeTypes]::Created, [System.IO.WatcherChangeTypes]::Deleted

printSectionBanner "Watching File Changes"
printSectionLine "$COMMAND"
printSectionLine "WATCH_PATH: ${WATCH_PATH}"
printSectionLine "WATCH_FILES_PATTERN: ${WATCH_FILES_PATTERN}"
printSectionLine "WATCH_FOLDER: ${WATCH_FOLDER}"
printSectionLine "WATCH_ATTRIBUTE_FILTER: ${WATCH_ATTRIBUTE_FILTER}"
printSectionLine "WATCH_CHANGE_TYPES: ${WATCH_CHANGE_TYPES}"


if ( -Not( $SILENT ) )
{
  $START = Read-Host -Prompt "Do you want to start watching update and run with these settings? (y/n)"

  if ($START -ne "y")
  {
    Write-Output "Quiting..."
    Exit
  }
}

# https://powershell.one/tricks/filesystem/filesystemwatcher

$WATCH
try
{
  Write-Warning "Watching: $WATCH_FOLDER"

  # create a filesystemwatcher object
  $WATCH = New-Object -TypeName IO.FileSystemWatcher -ArgumentList $WATCH_FOLDER, $WATCH_FILES_PATTERN -Property @{
    IncludeSubdirectories = $WATCH_SUBFOLDERS
    NotifyFilter = $WATCH_ATTRIBUTE_FILTER
  }

  # start monitoring manually in a loop:
  do
  {
    # wait for changes for the specified timeout
    # IMPORTANT: while the watcher is active, PowerShell cannot be stopped
    # so it is recommended to use a timeout of 1000ms and repeat the
    # monitoring in a loop. This way, you have the chance to abort the
    # script every second.
    $RESULT = $WATCH.WaitForChanged($WATCH_CHANGE_TYPES, $WATCH_TIMEOUT)
    # if there was a timeout, continue monitoring:
    if ($RESULT.TimedOut) { continue }

    Invoke-ChangeAction -Change $RESULT
    # the loop runs forever until you hit CTRL+C
  } while ($true)
}
finally
{
  # release the watcher and free its memory:
  $WATCH.Dispose()
  Write-Warning 'FileSystemWatcher removed.'
}


