#pragma once
#include <array>
#include <vector>

using Vec3 = std::array<double,3>;

struct Body {
  double mass;
  Vec3 pos;
  Vec3 vel;
};

// 计算 N 体在 dt 时间后的一步新状态
void step(std::vector<Body>& bodies, double dt);

