param(
  [Parameter(ValueFromRemainingArguments=$true)]
  [string[]]$Args
)

$ErrorActionPreference = 'Stop'

# Run without needing an editable install by setting PYTHONPATH to src
$env:PYTHONPATH = (Join-Path $PSScriptRoot 'src')
python -m aiweb_gen @Args
