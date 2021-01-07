
extern "C" int mycppfun(void);

#include <iostream>

class MyClass {
  public:
    int myNum;
};

int mycppfun() {
  // arbitrary example c++ code
  MyClass myObj1, myObj2; 
  myObj1.myNum = 15;
  myObj2.myNum = 11; 
  std::cout << "Inside 'mycppfun()' C++ function";
  return myObj1.myNum + myObj2.myNum;
}
