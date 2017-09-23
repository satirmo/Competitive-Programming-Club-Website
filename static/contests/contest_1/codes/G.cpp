#include <bits/stdc++.h>

using namespace std;

const int maxn = 1000005;

int id[ maxn ];

void make_set(){
	for( int i = 0; i < maxn; i++ ){
		id[ i ] = i;
	}
}

int find( int x ){
	while( x != id[ x ] ){
		int p = id[ x ];
		id[ x ] = id[ p ];
		x = id[ x ];
	}
	return x;
}

void unite( int p, int q ){
	int pr = find( p );
	int qr = find( q );
	id[ pr ] = qr;
}

int main(){
	int n, q;
	scanf( "%d %d\n", &n, &q );
	make_set();

	while( q-- ){
		int a, b;
		char qt;
		scanf( "%c %d %d\n", &qt, &a, &b );

		if( qt == '=' ){
			unite( a, b );
		}

		else{
			int sa = find( a );
			int sb = find( b );

			cout << ( sa == sb ? "yes" : "no" ) << endl;
		}
	}
	return 0;
}