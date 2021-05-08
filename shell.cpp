#include <iostream>
#include <vector>
#include <algorithm>

struct Edge;

struct Face;

struct Point {
    int x = 0;
    int y = 0;
    int z = 0;
    int id = 0;
    Edge* dup = nullptr;
    Point() = default;
    Point(const int& x, const int& y, const int& z, const int& id) : x(x), y(y), z(z), id(id) {}
    Point(Point begin, Point end) : x(end.x - begin.x), y(end.y - begin.y), z(end.z - begin.z) {}
    bool operator == (const Point& other) const {
        return (other.x == x) && (other.y == y) && (other.z == z);
    }
};


double OrintVolume(const Point& v1, const Point& v2, const Point& v3) {
    return v1.x * (v2.y * v3.z - v2.z * v3.y) - v1.y * (v2.x * v3.z - v3.x * v2.z) + v1.z * (v2.x * v3.y - v2.y * v3.x);
}


struct Edge {
    std::vector<int> ends;
    std::vector<Face*> neigh;
    Edge* prev = nullptr;
    Edge* next = nullptr;
    Edge(const Point& p1, const Point& p2) : ends(2), neigh(2) {
        ends[0] = p1.id;
        ends[1] = p2.id;
    }
};


struct Face {
    std::vector<int> points;
    Face* prev = nullptr;
    Face* next = nullptr;
    bool visible = false;
    Face(const Point& p1, const Point& p2, const Point& p3, const Point& init_point) : points(3) {
        Point v1(p1, p2);
        Point v2(p1, p3);
        Point v_init(p1, init_point);
        double volume = OrintVolume(v1, v2, v_init);
        if (volume > 0) {
            points = {p1.id, p3.id, p2.id};
        } else {
            points = {p1.id, p2.id, p3.id};
        }
    }
    int OtherPoint(const int& p1, const int& p2) {
        if (p1 != points[0] && p2 != points[0]) return points[0];
        else if (p1 != points[1] && p2 != points[1]) return points[1];
        else return points[2];
    }
};


struct OutputFormater {
    int id1 = 0;
    int id2 = 0;
    int id3 = 0;
    explicit OutputFormater(const Face& f) {
        std::vector<int> output;
        if (f.points[0] == std::min(std::min(f.points[0], f.points[1]), f.points[2])) {
            output = {f.points[0], f.points[1], f.points[2]};
        } else if (f.points[1] == std::min(std::min(f.points[0], f.points[1]), f.points[2])) {
            output = {f.points[1], f.points[2], f.points[0]};
        } else output = {f.points[2], f.points[0], f.points[1]};
        id1 = output[0];
        id2 = output[1];
        id3 = output[2];
    }
};


bool Comp(const OutputFormater& f1, const OutputFormater& f2) {
    return (f1.id1 < f2.id1) || (f1.id1 == f2.id1 && f1.id2 < f2.id2) || (f1.id1 == f2.id1 && f1.id2 == f2.id2 && f1.id3 < f2.id3);
}


class ShellBuilder {
private:
    std::vector<Point> points_;
    Edge* edges_ = nullptr;
    Face* faces_ = nullptr;
    Edge* edges_end_ = nullptr;
    Face* faces_end_ = nullptr;
    int points_ptr_ = 0;

    void AddEdge(const Point& p1, const Point& p2) {
        Edge* e = new Edge(p1, p2);
        edges_end_->next = e;
        e->prev = edges_end_;
        edges_end_ = edges_end_ -> next;
    }

    void AddFace(const Point& p1, const Point& p2, const Point& p3, const Point& p_init) {
        Face* f = new Face(p1, p2, p3, p_init);
        faces_end_->next = f;
        f->prev = faces_end_;
        faces_end_ = faces_end_->next;
    }

    void DeleteEdge(Edge* e_ptr) {
        if (e_ptr->prev == nullptr && e_ptr->next != nullptr) {
            e_ptr->next->prev = nullptr;
            edges_ = e_ptr->next;
        } else if (e_ptr->next == nullptr && e_ptr->prev != nullptr) {
            e_ptr->prev->next = nullptr;
            edges_end_ = e_ptr->prev;
        } else if (e_ptr->next != nullptr && e_ptr->prev != nullptr) {
            Edge* ptr = e_ptr->next;
            ptr->prev = ptr->prev->prev;
            e_ptr->prev->next = ptr;
        }
        delete e_ptr;
    }

    void DeleteFace(Face* f_ptr) {
        if (f_ptr->prev == nullptr && f_ptr->next != nullptr) {
            f_ptr->next->prev = nullptr;
            faces_ = f_ptr->next;
        } else if (f_ptr->next == nullptr && f_ptr->prev != nullptr) {
            f_ptr->prev->next = nullptr;
            faces_end_ = f_ptr->prev;
        } else if (f_ptr->next != nullptr && f_ptr->prev != nullptr) {
            Face* ptr = f_ptr->next;
            ptr->prev = ptr->prev->prev;
            f_ptr->prev->next = ptr;
        }
        delete f_ptr;
    }

    void ShellInit() {
        Face* f1 = new Face(points_[0], points_[1], points_[2], points_[3]);
        faces_end_ = f1;
        AddFace(points_[0], points_[1], points_[3], points_[2]);
        Face* f2 = f1->next;
        AddFace(points_[0], points_[2], points_[3], points_[1]);
        Face* f3 = f2->next;
        AddFace(points_[1], points_[2], points_[3], points_[0]);
        Face* f4 = f3->next;

        Edge* e = new Edge(points_[0], points_[1]);
        e->neigh[0] = f1;
        e->neigh[1] = f2;

        edges_ = e;
        edges_end_ = e;

        AddEdge(points_[1], points_[2]);
        e = e->next;
        e->neigh[0] = f1;
        e->neigh[1] = f4;
        AddEdge(points_[2], points_[0]);
        e = e->next;
        e->neigh[0] = f1;
        e->neigh[1] = f3;
        AddEdge(points_[1], points_[3]);
        e = e->next;
        e->neigh[0] = f2;
        e->neigh[1] = f4;
        AddEdge(points_[0], points_[3]);
        e = e->next;
        e->neigh[0] = f2;
        e->neigh[1] = f3;
        AddEdge(points_[2], points_[3]);
        e = e->next;
        e->neigh[0] = f3;
        e->neigh[1] = f4;

        faces_ = f1;
        points_ptr_ = 4;
    }

public:
    explicit ShellBuilder(std::vector<Point>&& points) : points_(points) {}

    ~ShellBuilder() {
        while (faces_->next != nullptr) {
            faces_ = faces_ -> next;
            delete faces_->prev;
        }
        delete faces_;
        while (edges_->next != nullptr) {
            edges_ = edges_ -> next;
            delete edges_->prev;
        }
        delete edges_;
    }

    void BuildShell() {
        ShellInit();
        for (int i = points_ptr_; i < points_.size(); ++i) {
            Face* f_ptr = faces_;
            while (f_ptr != nullptr) {
                Point v1(points_[f_ptr->points[0]], points_[f_ptr->points[1]]);
                Point v2(points_[f_ptr->points[0]], points_[f_ptr->points[2]]);
                Point v3(points_[f_ptr->points[0]], points_[i]);
                if (OrintVolume(v1, v2, v3) > 0) f_ptr->visible = true;
                f_ptr = f_ptr->next;
            }
            Edge* e_ptr = edges_;
            while (e_ptr != nullptr) {
                if (!e_ptr->neigh[0]->visible && !e_ptr->neigh[1]->visible) {
                    e_ptr = e_ptr->next;
                    continue;
                } else if (e_ptr->neigh[0]->visible && e_ptr->neigh[1]->visible) {
                    Edge* ptr = e_ptr->next;
                    DeleteEdge(e_ptr);
                    e_ptr = ptr;
                } else if ((e_ptr->neigh[0]->visible && !e_ptr->neigh[1]->visible) || (!e_ptr->neigh[0]->visible && e_ptr->neigh[1]->visible)) {
                    Face* f;
                    if (!e_ptr->neigh[0]->visible) f = e_ptr->neigh[0];
                    else f = e_ptr->neigh[1];
                    Point p_init = points_[f->OtherPoint(e_ptr->ends[0], e_ptr->ends[1])];
                    AddFace(points_[e_ptr->ends[0]], points_[e_ptr->ends[1]], points_[i], p_init);
                    if (e_ptr->neigh[0] == f) e_ptr->neigh[1] = faces_end_;
                    else e_ptr->neigh[0] = faces_end_;
                    for (int j = 0; j < 2; ++j) {
                        if (points_[e_ptr->ends[j]].dup == nullptr) {
                            AddEdge(points_[e_ptr->ends[j]], points_[i]);
                            points_[edges_end_->ends[0]].dup = edges_end_;
                            edges_end_->neigh[0] = faces_end_;
                        } else {
                            points_[e_ptr->ends[j]].dup->neigh[1] = faces_end_;
                        }
                    }
                    e_ptr = e_ptr->next;
                }
            }
            f_ptr = faces_;
            while (f_ptr != nullptr) {
                if (f_ptr->visible) {
                    Face* ptr = f_ptr->next;
                    DeleteFace(f_ptr);
                    f_ptr = ptr;
                } else {
                    f_ptr = f_ptr->next;
                }
            }
            for (int j = 0; j < points_.size(); ++j) {
                points_[j].dup = nullptr;
            }
        }
        PrintFaces();
    }

    void PrintFaces() {
        std::vector<OutputFormater> formater;
        Face* f_ptr = faces_;
        while (f_ptr != nullptr) {
            OutputFormater f(*f_ptr);
            formater.push_back(f);
            f_ptr = f_ptr -> next;
        }
        std::sort(formater.begin(), formater.end(), Comp);
        std::cout << formater.size() << std::endl;
        for (int i = 0; i < formater.size(); ++i) {
            std::cout<< 3 << " " << formater[i].id1 << " " << formater[i].id2 << " " << formater[i].id3 << std::endl;
        }
    }
};


int main() {
    int64_t m = 0;
    std::cin >> m;
    for (int i = 0; i < m; ++i) {
        int n = 0;
        std::cin >> n;
        std::vector<Point> points(n);
        for (int j = 0; j < n; ++j) {
            int x = 0;
            int y = 0;
            int z = 0;
            std::cin >> x >> y >> z;
            Point p(x, y, z, j);
            points[j] = p;
        }
        ShellBuilder builder(std::move(points));
        builder.BuildShell();
    }
    return 0;
}
