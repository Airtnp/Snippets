// ref: https://news.ycombinator.com/item?id=11879464
#include <climits>

struct foo;

__asm__(".symver foo_do_v1_1,foo_do@@v1.1");
long foo_do_v1_1(struct foo *F, int arg1, int arg2) {
  ...
}

__asm__(".symver foo_do_v1_0,foo_do@v1.0");
int foo_do_v1_0(struct foo *F, int arg1) {
  long rv = foo_do_v1_1(F, arg1, 0);
  assert(rv >= INT_MIN && rv <= INT_MAX);
  return rv;
}