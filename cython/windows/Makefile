CYTHON=cython

INCDIR=c:/python27/include
LIBDIR1=c:/mingw/lib
LIBDIR2=c:/python27/libs
PYLIB=python27

CC=wine gcc
LINKCC=wine gcc

CFLAGS=-Wall -O3
LDFLAGS=-mwindows

all: imsasrv.exe getserial.exe

imsasrv.exe: imsasrv.o
	$(LINKCC) -o $@ $^ -L$(LIBDIR1) -L$(LIBDIR2) -l$(PYLIB) $(CFLAGS) $(LDFLAGS)

imsasrv.o: imsasrv.c
	$(CC) -c $^ -I$(INCDIR)

imsasrv.c: imsasrv.py
	@$(CYTHON) --embed $^

getserial.exe: getserial.o
	$(LINKCC) -o $@ $^ -L$(LIBDIR1) -L$(LIBDIR2) -l$(PYLIB) $(CFLAGS) $(LDFLAGS)

getserial.o: getserial.c
	$(CC) -c $^ -I$(INCDIR)

getserial.c: getserial.py
	@$(CYTHON) --embed $^

clean:
	@rm -f *~ *.o *.so *.c imsasrv.exe getserial.exe

