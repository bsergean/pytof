FLAGS = -g

uf: main.o NaiveUnionFind.o QuickUnionFind.o WeightedQuickUnionFind.o UnionFind.o
	g++ ${FLAGS} -o uf *.o

main.o: NaiveUnionFind.h QuickUnionFind.h main.cc UnionFind.h
	g++ ${FLAGS} -c -o main.o main.cc

UnionFind.cc: UnionFind.h
	g++ ${FLAGS} -c -o UnionFind.o UnionFind.cc

NaiveUnionFind.o: NaiveUnionFind.cc NaiveUnionFind.h UnionFind.h
	g++ ${FLAGS} -c -o NaiveUnionFind.o NaiveUnionFind.cc

QuickUnionFind.o: QuickUnionFind.cc QuickUnionFind.h UnionFind.h
	g++ ${FLAGS} -c -o QuickUnionFind.o QuickUnionFind.cc

WeightedQuickUnionFind.o: WeightedQuickUnionFind.cc WeightedQuickUnionFind.h UnionFind.h
	g++ ${FLAGS} -c -o WeightedQuickUnionFind.o WeightedQuickUnionFind.cc
all: uf

clean:
	rm *.o uf

test: uf
	./uf
