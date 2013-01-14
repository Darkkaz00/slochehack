#include <stdio.h>

int main(void){
	char c;

	while(1){
		c = getchar();
		if(feof(stdin)) break;
		if(c=='\n'){
			printf("<BR>");
		} else 	putchar(c);
	}

	return 0;
}
