#include <bits/stdc++.h>
using namespace std;


class TAS {
public:
	// each memeber is a pair : (name_of_glue, strength)
	vector<  pair<string, int> > glue_alphabet;
	// each member is a 4-tuple(N, E, S, W), having the index in the glue alphabet
	vector< vector<int> > tile_types;
	// temperature
	int temperature;
	// seed configuration
	vector< vector<int> > V;
	void check(int x, int y, int k) {
		int n = V.size(), gs = 0;
		if(V[x][y] != -1)
			return;
		vector< vector<int> > dir = {{-1,0, 1, 3}, {0, -1, 0, 2}, {1, 0, 3, 1}, {0, 1, 2, 0}};
		for(int i = 0; i < 4; i++) {
			if(x + dir[i][0] >= 0 && x + dir[i][0] < n && y + dir[i][1] >=0 && y + dir[i][1] < n)
				if(V[x + dir[i][0]][y + dir[i][1]] != -1)
					if(tile_types[k][dir[i][3]] != -1 && tile_types[V[x + dir[i][0]][y + dir[i][1]]][dir[i][2]] == tile_types[k][dir[i][3]])
						gs += glue_alphabet[tile_types[k][dir[i][3]]].second;
		}
		if(gs >= temperature)
			V[x][y] = k;
	}

    void simulate(int MAX_ITER) {
    	int s = V.size();
    	int n = tile_types.size();
    	for(int i = 0; i < MAX_ITER; i++) {
    		cout << i << endl;
    		int x = rand()%s;
    		int y = rand()%s;
    		int k = rand()%n;
    		check(x, y, k);
    	}
    	for(int i = 0; i < s; i++) {
    		for(int j = 0; j < s; j++)
    			cout << V[i][j] << " " ;
    		cout << endl;
    	}
    }

    TAS(vector< pair<string, int> > g, vector< vector<int> > t, int temp, vector< vector<int> > seed) {
    	glue_alphabet = g;
    	tile_types = t;
    	temperature = temp;
    	V = seed;
    }
};


int main() {
	vector< vector<int> > t = {{1, 0, -1, -1}, {6, 3, -1, 0}, {6, -1, -1, 3}, {2, 5, 1, -1}, {-1, 5, 2, -1}, {6, 5, 6, 5}};
	vector< pair<string, int> > g = {{"a", 2}, {"b", 2}, {"c", 2}, {"d", 2}, {"e", 2}, {"x", 1}, {"y", 1}};
	vector< vector<int> > seed(50, vector<int>(50, -1));
	seed[0][0] = 0;
	TAS* tas = new TAS(g, t, 2, seed);
	tas->simulate(100);
}