#include <list>
using std::list;
#include <stdio.h>

void new_test(const char* test)
{
	printf("-- Now testing : %s --\n", test);
}

int main()
{
	list<int> L1;
	//L1.push_back(1);
	//L1.push_back(2);
	//L1.push_back(3);
	
	new_test("HOWTO access the first elem");
	list<int>::iterator it = L1.begin();
	printf("List first elem = %d\n", *it);

	new_test("HOWTO walk 2 lists in one loop");
	list<int> L2;
 	L2.push_back(4);
	L2.push_back(5);
	L2.push_back(6);
	
	it = L1.begin();
	while (it != L2.end())
	{
		if (it == L1.end())
			it = L2.begin();
		if (it == L2.end())
			break;
			
		printf("%d ", *it);
		++it;
	}
	puts("");

	new_test("HOWTO walk 2 lists in one loop and add 1 elem in front of the first list");
	// We have to create a new tmp list.
	int x = 0;
	list<int> L_tmp = L1;
	L_tmp.push_front(x);
	
	it = L_tmp.begin();
	while (it != L2.end())
	{
		if (it == L_tmp.end())
			it = L2.begin();
		if (it == L2.end())
			break;
			
		printf("%d ", *it);
		++it;
	}
	puts("");

	new_test("HOWTO walk 2 lists in one loop, add 1 elem in front of the first list, and make a different process for the first elem and the 2nd list than for the first list");
	// We have to create a new tmp list.
	x = 0;
	bool processing_second_list = false;
	L_tmp = L1;
	L_tmp.push_front(x);
	
	it = L_tmp.begin();
	while (it != L2.end())
	{
		if (it == L_tmp.end()) {
			it = L2.begin();
			processing_second_list = true;
		}
		if (it == L2.end())
			break;

		if (it == L_tmp.begin() || processing_second_list)
		  printf("[%d] ", *it);
		else
		  printf("(%d) ", *it);
		
		++it;
	}
	puts("");


	// END
	return 0;
}
