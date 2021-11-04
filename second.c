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

void recurse (int c) {
    if (c == 5) return;
    else recurse(++c);
}

void loop() {
    for (int i = 0; i < 10; i++) {
        printf("Loop %d\n", i);
    }
}

int multiple_return_stmts(int input) {
    if (input % 2 == 1) return 1;
    else return 0;
}
