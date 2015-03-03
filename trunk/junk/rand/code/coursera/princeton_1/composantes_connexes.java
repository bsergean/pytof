public static void main(String[] args)
{
	int N = StdIn.readInt();
	UF uf = new UF(n);
	while (!StdIn.isEmpty()) {
		int p = StdIn.readInt();
		int q = StdIn.readInt();
		if (!uf.connected(p, q)) {
			uf.union(p, q);
			StdOut.println(p + " " + q);
		}
	}
}

/*

0 1 2 3 4 5 6 7 8 9

0 9 6 5 4 2 6 1 0 5

0 9 6 5 4 2 6 1 0 5
  | | | | | | | | |
  1 2 3 4 5 6 7 8 9
+ + + + + 

0   6   4 
|   |     
8   2   
    |
    5       
    |\      
    9 3 
    |
    1
    |
    7
*/
