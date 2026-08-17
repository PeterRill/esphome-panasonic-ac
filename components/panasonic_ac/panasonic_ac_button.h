#pragma once

#include "esphome/components/button/button.h"
#include "esphome/core/component.h"

namespace esphome {
namespace panasonic_ac {

class PanasonicACButton : public button::Button, public Component {
 public:
  template<typename F> void add_on_action_callback(F &&callback) {
    this->action_callback_.add(std::forward<F>(callback));
  }

 protected:
  void press_action() override { this->action_callback_.call(); }

  LazyCallbackManager<void()> action_callback_;
};

}  // namespace panasonic_ac
}  // namespace esphome
