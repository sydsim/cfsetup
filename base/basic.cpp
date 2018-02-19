#include <cstdio>
#include <algorithm>
#include <cstring>

using namespace std;

void run() {
  // implement here!
}

int main(int argc, char **argv) {
  if (argc == 4) {
    char input_file[50];
    sprintf(input_file, "contest/%s/%s/input/input_%s", argv[1], argv[2], argv[3]);
    freopen(input_file, "r", stdin);
  }

  run();

  return 0;
}
