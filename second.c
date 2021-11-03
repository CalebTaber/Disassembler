#include "second.h"
#include "stdio.h"

void print_hello2() {
    printf("Hello from second!");
}

int return_11() {
    return 11;
}

void function_call() {
    printf("Calling return_11()");
    return_11();
}
