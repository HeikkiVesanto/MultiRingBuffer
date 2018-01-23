@ECHO OFF
@RD /S /Q .\MultiRingBuffer
mkdir MultiRingBuffer
xcopy /s help .\MultiRingBuffer\help\
xcopy *.py .\MultiRingBuffer\
xcopy *.svg .\MultiRingBuffer\
xcopy *.txt .\MultiRingBuffer\
xcopy *.qrc .\MultiRingBuffer\
xcopy *.ui .\MultiRingBuffer\
