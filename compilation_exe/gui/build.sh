windres *.rc -o res.o
cc *.c res.o -mwindows -lcomctl32 -o slochehack.exe