// g++ -shared -I "C:\Program Files\Python36\include" -std=c++11 monauralize.cpp "C:\Program Files\Python36\libs\libpython36.a" -o monauralize.pyd
#include <string.h>
#include <cmath>
namespace std {
    float _hypot(float x, float y) {
        return std::hypot(x, y);
    }
    double _hypot(double x, double y) {
        return std::hypot(x, y);
    }
    long double _hypot(long double x, long double y) {
        return std::hypot(x, y);
    }
}
char* strdup(const char* s) {
    const auto len = strlen(s);
    char* p = new char[len];
    if (p == NULL) {
        return p;
    }
    memcpy(p, s, len);
    return p;
}

//code from here
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdio.h>
#include <vector>

namespace py = pybind11;

std::vector<int> monauralize(std::vector<int> &list, int nframe, int channels) {
    int i, j, ave;
    std::vector<int> monauralized;
    if (channels == 2) {
        for (i=0; i<nframe; i+=2) {
            monauralized.push_back((list[i]+list[i+1])/2);
        }
    } else {
        for (i=0; i<nframe; ++i) {
            ave = 0;
            for (j=0; j<channels; ++j) {
                ave += list[i*channels+j];
            }
            monauralized.push_back(ave / channels);
        }
    }
    return monauralized;
}

// don't forget to write pyplugin

PYBIND11_PLUGIN(monauralize){
    py::module m("monauralize", "monauralize audio data");
    m.def("monauralize", &monauralize, "monauralize audio data: f(double *audio_data, int nframe, int channels) -> double *audio_data");
    return m.ptr();
}