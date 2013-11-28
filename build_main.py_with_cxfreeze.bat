python C:\Python32\Scripts\cxfreeze main.py --target-dir ../build --target-name=PyTanks.exe --icon=icon.ico
mkdir ..\build\tanks
mkdir ..\build\shut
mkdir ..\build\blocks
cp tanks/* ../build/tanks/
cp shut/* ../build/shut/
cp blocks/* ../build/blocks/
cp freesansbold.ttf ../build/