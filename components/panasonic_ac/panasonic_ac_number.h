#pragma once

#include "esphome/components/number/number.h"
#include "esphome/core/component.h"

namespace esphome {
namespace panasonic_ac {

class PanasonicACNumber : public number::Number, public Component {
 public:
  template<typename F> void add_on_control_callback(F &&callback) {
    this->control_callback_.add(std::forward<F>(callback));
  }

 protected:
  void control(float value) override { this->control_callback_.call(value); }

  LazyCallbackManager<void(float)> control_callback_;
};

}  // namespace panasonic_ac
}  // namespace esphome
