i686-w64-mingw32-windres dlg_three.rc -o res.o
i686-w64-mingw32-windres manifest.rc -o manifest.o
i586-mingw32msvc-cc *.c res.o manifest.o -mwindows -lcomctl32 -o slochehack.exe
