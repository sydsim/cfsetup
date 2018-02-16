#include <cstdio>
#include <algorithm>
#include <cstring>

using namespace std;




int main(int argc, char **argv) {
  if (argc == 2) {
    char input_file[20];
    sprintf(input_file, "input/input_%s", argv[1]);
    freopen(input_file, "r", stdin);
  }

  return 0;
}
