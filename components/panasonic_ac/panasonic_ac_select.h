#pragma once

#include "esphome/components/select/select.h"
#include "esphome/core/component.h"

namespace esphome {
namespace panasonic_ac {

class PanasonicACSelect : public select::Select, public Component {
 public:
  template<typename F> void add_on_control_callback(F &&callback) {
    this->control_callback_.add(std::forward<F>(callback));
  }

 protected:
  void control(size_t index) override { this->control_callback_.call(index); }

  LazyCallbackManager<void(size_t)> control_callback_;
};

}  // namespace panasonic_ac
}  // namespace esphome
