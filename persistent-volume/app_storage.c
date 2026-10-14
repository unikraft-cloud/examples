#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    const char *file_path = "/data/counter.txt";
    int counter = 0;

    FILE *f = fopen(file_path, "r");
    if (f != NULL) {
        char buf[64] = {0};
        if (fgets(buf, sizeof(buf), f) != NULL) {
            counter = atoi(buf);
        }
        fclose(f);
    }

    counter++;
    printf("[SUCCESS] C reading persistent volume! Run count: %d\n", counter);

    f = fopen(file_path, "a+");
    if (f == NULL) {
      perror("Error opening volume for writing");
        return 1;
    }

    if (fprintf(f, "%d\n", counter) < 0) {
    	perror("Error writing counter");
	fclose(f);
	return 1;
    }

    fclose(f);

    return 0;
}
