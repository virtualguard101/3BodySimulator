#include "three_body.h"
#include <cmath>

void step(std::vector<Body>& bodies, double dt) {
  const double G = 6.67430e-11;

  // 简单欧拉积分
  for (auto& bi : bodies) {
    Vec3 acc{0,0,0};
    for (auto& bj : bodies) {
      if (&bi == &bj) continue;

      Vec3 diff;
      for (int i=0;i<3;i++) {
        diff[i]=bj.pos[i]-bi.pos[i];
      }

      double r2 = diff[0]*diff[0]+diff[1]*diff[1]+diff[2]*diff[2];
      double invr3 = 1.0/(std::sqrt(r2)*r2 + 1e-10);

      for(int i=0;i<3;i++) {
        acc[i]+=G * bj.mass * diff[i]*invr3;
      }
    }

    for(int i=0;i<3;i++) {
        bi.vel[i]+=acc[i]*dt;
    }
  }

  for(auto& b: bodies)
    for(int i=0;i<3;i++)
      b.pos[i]+=b.vel[i]*dt;
}

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(three_body, m) {
  py::class_<Body>(m, "Body")
    .def(py::init<>())
    .def_readwrite("mass", &Body::mass)
    .def_readwrite("pos", &Body::pos)
    .def_readwrite("vel", &Body::vel);

  m.def("step", &step, "Perform one simulation step",
        py::arg("bodies"), py::arg("dt"));
}
