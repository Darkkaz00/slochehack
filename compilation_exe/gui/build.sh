windres dlg_three.rc -o res.o
windres manifest.rc -o manifest.o
cc *.c res.o manifest.o -mwindows -lcomctl32 -o slochehack.exe