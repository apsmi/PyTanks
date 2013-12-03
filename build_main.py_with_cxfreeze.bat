python C:\Python32\Scripts\cxfreeze main.py --target-dir ../build/PyTanksClient/ --target-name=PyTanks.exe -O --icon=icon.ico
mkdir ..\build\PyTanksClient\tanks
mkdir ..\build\PyTanksClient\shut
mkdir ..\build\PyTanksClient\blocks
cp tanks/* ../build/PyTanksClient/tanks/
cp shut/* ../build/PyTanksClient/shut/
cp blocks/* ../build/PyTanksClient/blocks/
cp freesansbold.ttf ../build/PyTanksClient/