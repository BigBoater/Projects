#include <stdio.h>
#include <stdint.h>  //replacement for #include <cstdint>

struct S {
    int i; double d; char c;
};

int main(void){
    unsigned char bad_buff[sizeof(struct S)];
    _Alignas(struct S) unsigned char good_buff[sizeof(struct S)];

    struct S *bad_s_ptr = (struct S *)bad_buff;
    struct S *good_s_ptr = (struct S *)good_buff;

extern unsigned int ui, sum;
if (sum + ui > UINT8_MAX)
    too_big();
else
    sum = sum + ui;
}