#include "second.h"
#include "stdio.h"

int three = 3;
int eleven;

int main() {
    printf("Hello, world!");
    print_hello2();
    printf("%d", return_11());
    function_call();
    recurse(0);
    loop();
    printf("%d\n", three);
    eleven = 7 + three;
    printf("%d\n", eleven);
    return 0;
}
