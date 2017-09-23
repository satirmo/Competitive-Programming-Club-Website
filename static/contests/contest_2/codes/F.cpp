#include <bits/stdc++.h>

using namespace std;

const int maxn = 1000005;

int a[ 15 ];
int dp[ maxn ];

string solve( int n, int m ){
    dp[ 0 ] = 0;

    for( int i = 1; i <= n; i++ ){
        dp[ i ] = 0;

        for( int j = 0; j < m; j++ ){
            if( a[ j ] > i ){
                continue;
            }

            if( dp[ i - a[ j ] ] == 0 ){
                dp[ i ] = 1;
            }
        }
    }

    string ret = ( dp[ n ] ) ? "Stan wins" : "Ollie wins";

    return ret;
}

int main(){
    int n;

    while( cin >> n ){
        int m;
        cin >> m;

        for( int i = 0; i < m; i++ ){
            scanf( "%d", &a[ i ] );
        }

        string ans = solve( n, m );
        printf( "%s\n", ans.c_str() );
    }

    return 0;
}