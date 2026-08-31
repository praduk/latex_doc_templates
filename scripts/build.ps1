$ErrorActionPreference = "Stop"
$BuildScript = Join-Path $PSScriptRoot "build.py"

if (Get-Command py.exe -CommandType Application -ErrorAction SilentlyContinue) {
    & py -3 -c "import sys; raise SystemExit(sys.version_info < (3, 9))"
    if ($LASTEXITCODE -eq 0) {
        & py -3 $BuildScript @args
        exit $LASTEXITCODE
    }
}

if (Get-Command python.exe -CommandType Application -ErrorAction SilentlyContinue) {
    & python -c "import sys; raise SystemExit(sys.version_info < (3, 9))"
    if ($LASTEXITCODE -eq 0) {
        & python $BuildScript @args
        exit $LASTEXITCODE
    }
}

throw "Python 3.9 or newer was not found. Install it, then rerun this command."
