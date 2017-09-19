template<unsigned int N>
struct struct_int : struct_int<N - 1> {
	const static unsigned int count = N;
};
template<>
struct struct_int<0> {
	const static unsigned int count = 0;
};

#define MAX_COUNT 168 // you can increase the number if your compiler affordable

#ifdef _MSC_VER

char (*auto_counter(...))[0+1];

#define EVAL_COUNTER (sizeof(*(auto_counter((struct_int<MAX_COUNT>*)0))) - 1)

template<unsigned int N>
struct eval_counter{
	 static const unsigned int value = N;
	 static const unsigned int next_value = value + 1;	 
	 friend char (*auto_counter(struct_int<next_value>*))[next_value + 1];
};

#else

template<int M>
char (*auto_counter(...))[0+1];

#define EVAL_COUNTER (sizeof(*(auto_counter<0>((struct_int<MAX_COUNT>*)0))) - 1)

template<unsigned int N>
struct eval_counter{
	 static const unsigned int value = N;
	 static const unsigned int next_value = value + 1;
	 template<int M>
	 friend char (*auto_counter(struct_int<next_value>*))[next_value + 1];
};
#endif

#include <stdio.h>
int main(){
	unsigned int i = eval_counter<EVAL_COUNTER>::value;	//i = 0
	unsigned int j = eval_counter<EVAL_COUNTER>::value; //j = 1
	unsigned int k = eval_counter<EVAL_COUNTER>::value; //k = 2
	printf("%u%u%u\n", i, j, k);
    return 0;
}