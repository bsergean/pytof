uf: main.o NaiveUnionFind.o QuickUnionFind.o WeightedQuickUnionFind.o  
	g++ -o uf *.o

main.o: NaiveUnionFind.h QuickUnionFind.h main.cc
	g++ -c -o main.o main.cc

NaiveUnionFind.o: NaiveUnionFind.cc NaiveUnionFind.h UnionFind.h
	g++ -c -o NaiveUnionFind.o NaiveUnionFind.cc

QuickUnionFind.o: QuickUnionFind.cc QuickUnionFind.h UnionFind.h
	g++ -c -o QuickUnionFind.o QuickUnionFind.cc

WeightedQuickUnionFind.o: WeightedQuickUnionFind.cc WeightedQuickUnionFind.h UnionFind.h
	g++ -c -o WeightedQuickUnionFind.o WeightedQuickUnionFind.cc
all: uf

clean:
	rm *.o uf

test: uf
	./uf
