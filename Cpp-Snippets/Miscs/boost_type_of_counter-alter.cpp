template<unsigned int N>
struct struct_int : struct_int<N - 1> {};
template<>
struct struct_int<0> {};
#define MAX_COUNT 168 // you can increase the number if your compiler affordable

#define EVAL_COUNTER(counter) (sizeof(*counter((struct_int<MAX_COUNT>*)0)) \
          - sizeof(*counter((void*)0)))
//We can change the result of EVAL_COUNTER if we use INCREASE_COUNTER or SET_COUNTER

#define INCREASE_COUNTER(counter, delta)  char (*counter(struct_int<EVAL_COUNTER(counter) + 1>*))[EVAL_COUNTER(counter) + sizeof(*counter((void*)0)) + (delta)]; 

#define SET_COUNTER(counter, value)  char (*counter(struct_int<EVAL_COUNTER(counter) + 1>*))[value + sizeof(*counter((void*)0))]; 

#include <stdio.h>
int main(){
   char (*first_counter(...))[1];  // It declares a function. No space cost.
   char (*second_counter(...))[1]; // It declares a function. No space cost.
    
//For all the counter, the init value must be zero.
   static const unsigned int i1 = EVAL_COUNTER(first_counter); //i1=0
   INCREASE_COUNTER(first_counter, 2);
   static const unsigned int i2 = EVAL_COUNTER(first_counter); //i2=0+2
   INCREASE_COUNTER(first_counter, 1);
   static const unsigned int i3 = EVAL_COUNTER(first_counter); //i3=2+1
   //INCREASE_COUNTER(first_counter, -1);  negative increase is not enabled
   SET_COUNTER(first_counter, 6);
   static const unsigned int i4 = EVAL_COUNTER(first_counter); //i4=6
   //SET_COUNTER(first_counter, 6);  we can not set counter to number that not greater than its max
   
//For all the counter, the init value must be zero.
   static const unsigned int j1 = EVAL_COUNTER(second_counter); //j1=0
   INCREASE_COUNTER(second_counter, 2);
   static const unsigned int j2 = EVAL_COUNTER(second_counter); //j2=0+2
   INCREASE_COUNTER(second_counter, 1);
   static const unsigned int j3 = EVAL_COUNTER(second_counter); //j3=2+1
    
   printf("%u%u%u%u\n%u%u%u\n", i1, i2, i3, i4 ,j1, j2, j3 );
   return 0;
}