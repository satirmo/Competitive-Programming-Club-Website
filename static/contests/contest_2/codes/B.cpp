#include <bits/stdc++.h>

using namespace std;

string display(int n) {
    string ret = (n < 9 ? " " : "") + to_string(n);
    return ret;
}

int main() {
    int hr, min;
    cin >> hr >> min;

    int normal = 60 * hr + min;
    int before = (normal + 1395) % 1440;

    string ans = display(before / 60) + " " + display(before % 60);
    cout << ans << endl;

    return 0;
}