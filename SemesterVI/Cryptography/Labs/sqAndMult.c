#include<stdio.h>
#define uint16_t unsigned short int
#define uint32_t unsigned long int
#define uint64_t unsigned long long int
#define uchar_t unsigned char

uint64_t g = 19;
uint32_t p = 2689;

uint32_t sqAndMult(uint32_t x, uint32_t c, uint32_t n){
    uint64_t z = 1;
    uint64_t y = x;
    while(c > 0){
        if(c & 1) z = (z * y) % n;
        y = (y * y) % n;
        c = c >> 1;
    }

    return z & 0xffffffff;
}

int main(){
    uint32_t a;
    uint32_t b;
    printf("Enter a and b: ");
    scanf("%lu %lu", &a, &b);

    printf("a = %lu, b = %lu\n", a, b);
    uint32_t ga = sqAndMult(g, a, p);
    uint32_t gb = sqAndMult(g, b, p);

    printf("ga = %lu, gb = %lu\n", ga, gb);

    uint32_t gab = sqAndMult(ga, b, p);
    uint32_t gba = sqAndMult(gb, a, p);

    printf("gab = %lu, gba = %lu\n", gab, gba);

    printf("\n****%d\n", sqAndMult(1234, 1077,  4189));
    return 0;
}