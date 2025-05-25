#pragma once
#include <array>
#include <vector>

using Vec3 = std::array<double,3>;

struct Body {
  double mass;
  Vec3 pos;
  Vec3 vel;
};

/**
* 计算 N 体在 dt 时间后的一步新状态
* @param bodies 使用结构体 Body 构造的天体实例参数。由 mass（质量）、pos（初始位置）、vec（初始速度）三个成员变量组成.
* @param dt 时间步长.
*/ 
void step(std::vector<Body>& bodies, double dt);

