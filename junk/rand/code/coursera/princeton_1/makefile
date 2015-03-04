uf: main.o NaiveUnionFind.o
	g++ -o uf *.o

main.o: NaiveUnionFind.h
	g++ -c -o main.o main.cc

NaiveUnionFind.o: NaiveUnionFind.cc NaiveUnionFind.h UnionFind.h
	g++ -c -o NaiveUnionFind.o NaiveUnionFind.cc

all: uf

clean:
	rm *.o uf

test: uf
	./uf
