function Check-PythonInstallation {
    $pythonPath = Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
    if ($pythonPath) {
        Write-Host "Python is installed at: $pythonPath" -ForegroundColor Green
    } else {
        Write-Host "Python is not installed. Please install Python from https://www.python.org/" -ForegroundColor Red
        Start-Process "https://www.python.org/downloads/"
        exit
    }
}

function Install-Pip {
    $pipVersion = python -m pip -V
    if (-not $pipVersion) {
        Write-Host "pip is not installed. Attempting to install pip..."
        $pipInstaller = "https://bootstrap.pypa.io/get-pip.py"
        $localPath = "get-pip.py"
        Invoke-WebRequest -Uri $pipInstaller -OutFile $localPath
        python get-pip.py
        Remove-Item get-pip.py -ErrorAction SilentlyContinue
    } else {
        Write-Host "pip is installed. - $pipVersion" -ForegroundColor Green
    }
}

function Check-PackageInstallation {
    $packages = @("Flask", "pandas")
    foreach ($package in $packages) {
        $isInstalled = python -c "import $package" 2>$null
        if (-not $isInstalled) {
            Write-Host "$package is not installed. Attempting to install..."
            pip install $package
        } else {
            Write-Host "$package is installed." -ForegroundColor Green
        }
    }
}

function Start-FlaskApp {
    $ScriptDirectory = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
    Set-Location -Path $ScriptDirectory

    $Env:FLASK_APP = "app.py"
    Start-Job -ScriptBlock { flask run }
    Start-Sleep -Seconds 2
    Start-Process "http://localhost:5000"
}

function Main {
    Check-PythonInstallation
    Install-Pip
    Check-PackageInstallation
    Start-FlaskApp
}

Main

