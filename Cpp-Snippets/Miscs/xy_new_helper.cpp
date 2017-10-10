// ref: https://www.zhihu.com/question/65848349/answer/238791300

#include <iostream>
#include <new>

class NewHelper {
 public:
  NewHelper(const char* file, int line) : file_(file), line_(line) {}

  template <class T>
  T* operator ->* (T* ptr) {
    std::cout << "Allocated a variable of size " << sizeof(T)
              << " at " << file_ << ":" << line_ << std::endl;
    return ptr;
  }

 private:
  const char* file_;
  const int line_;
};

#define new NewHelper(__FILE__, __LINE__) ->* new

int main() {
  int *p = new int;
  int *q = new (std::nothrow) int;
  return 0;
}