python -m venv ./venv-windows
./venv-windows/Scripts/activate
python -m pip install -r requirements.txt

$Shell = New-Object -ComObject ("WScript.Shell")
$ShortCut = $Shell.CreateShortcut((pwd).Path + "\MatrixPresenter.lnk")
$ShortCut.TargetPath= (pwd).Path + "\venv-windows\Scripts\pythonw.exe"
$ShortCut.Arguments= (pwd).Path + "\main.py"
$ShortCut.WorkingDirectory = (pwd).Path;
$ShortCut.WindowStyle = 1;
$ShortCut.Description = "Matrix presenter";
$ShortCut.Save()