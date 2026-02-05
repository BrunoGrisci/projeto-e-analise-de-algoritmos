/*
Algoritmo de Par Mais Próximo em 2D usando abordagem de Divisão e Conquista.
https://en.wikipedia.org/wiki/Closest_pair_of_points_problem

Lucas Nunes Alegre
Universidade Federal do Rio Grande do Sul
Instituto de Informática
Departamento de Informática Teórica
*/

#include <bits/stdc++.h>

using namespace std;

struct Point {
    double x, y;
};

double dist(const Point &a, const Point &b) {
    return hypot(a.x - b.x, a.y - b.y);
}

bool cmpX(const Point& a, const Point& b) { 
    return a.x < b.x; 
}

bool cmpY(const Point& a, const Point& b) {
     return a.y < b.y; 
}

double closestPairRecursive(vector<Point>& Px, vector<Point>& Py, int l, int r) {
    if (r - l <= 3) {
        double min_d = DBL_MAX;
        for (int i = l; i <= r; ++i)
            for (int j = i + 1; j <= r; ++j)
                min_d = min(min_d, dist(Px[i], Px[j]));
        return min_d;
    }

    int mid = (r - l) / 2;
    Point midPoint = Px[mid]; // x*

    vector<Point> PyLeft, PyRight;
    for (Point& p : Py) {
        if (p.x <= midPoint.x)
            PyLeft.push_back(p);
        else
            PyRight.push_back(p);
    }

    double dl = closestPairRecursive(Px, PyLeft, l, mid);
    double dr = closestPairRecursive(Px, PyRight, mid + 1, r);
    double d = min(dl, dr);

    // Construir strip: pontos com |x - midPoint.x| < d
    vector<Point> strip; // Sy
    for (Point& p : Py) {
        if (abs(p.x - midPoint.x) < d)
            strip.push_back(p);
    }

    // Comparar cada ponto com no máximo 15 seguintes em y
    for (int i = 0; i < strip.size(); ++i) {
        for (int j = i + 1; j < strip.size() && j <= i + 15; j++) {
            //if ((strip[j].y - strip[i].y) >= d) 
            //    break;
            d = min(d, dist(strip[i], strip[j]));
        }
    }

    return d;
}

double closestPair(vector<Point>& points) {
    vector<Point> Px = points;
    vector<Point> Py = points;

    sort(Px.begin(), Px.end(), cmpX);
    sort(Py.begin(), Py.end(), cmpY);

    return closestPairRecursive(Px, Py, 0, points.size() - 1);
}


int main() {
    vector<Point> points = {{2.1, 3.2}, {12.3, 30.4}, {40.5, 50.6}, {5.7, 1.8}, {12.0, 10.0}, {3.3, 4.4}};

    cout << fixed << setprecision(6);
    cout << "Menor distância: " << closestPair(points) << endl;
    return 0;
}
