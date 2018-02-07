@ECHO OFF
@RD /S /Q .\Multi_Ring_Buffer
mkdir Multi_Ring_Buffer
xcopy /s help .\Multi_Ring_Buffer\help\
xcopy *.py .\Multi_Ring_Buffer\
xcopy *.svg .\Multi_Ring_Buffer\
xcopy *.txt .\Multi_Ring_Buffer\
xcopy *.qrc .\Multi_Ring_Buffer\
xcopy *.ui .\Multi_Ring_Buffer\
