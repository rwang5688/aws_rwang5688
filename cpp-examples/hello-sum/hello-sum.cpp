#include <iostream>
#include <stdlib.h>

int main( int argc, char *argv[] )
{
  std::cout << "Hello, Sum!\n";
  std::cout << "Literal: The sum of 2 and 3 is 5.\n";

  if (argc > 2) {
    std::cout << "Calculated: The sum of " << argv[1] << " and " << argv[2]
      << " is " << atoi(argv[1]) + atoi(argv[2]) << ".\n";
  }

  return 0;
}
