#include "esphome/components/climate/climate.h"
#include "esphome/components/climate/climate_mode.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/core/preferences.h"
#include "esppac.h"
#include "panasonic_ac_button.h"
#include "panasonic_ac_number.h"

namespace esphome {
namespace panasonic_ac {
namespace CNT {

static const uint8_t CTRL_HEADER = 0xF0;  // The header for control frames
static const uint8_t POLL_HEADER = 0x70;  // The header for the poll command

static const int CMD_INTERVAL = 250;    // The interval at which to send commands

enum class ACState {
  Initializing,  // Before first query response is receive
  Ready,         // All done, ready to receive regular packets
};

class PanasonicACCNT : public PanasonicAC {
 public:
  void control(const climate::ClimateCall &call) override;

  void on_horizontal_swing_change(const StringRef &swing) override;
  void on_vertical_swing_change(const StringRef &swing) override;
  void on_nanoex_change(bool nanoex) override;
  void on_eco_change(bool eco) override;
  void on_econavi_change(bool eco) override;
  void on_mild_dry_change(bool mild_dry) override;

  void set_operational_status_sensor(text_sensor::TextSensor *sensor)
  {
    this->operational_status_sensor_ = sensor;
  }
  void set_indoor_humidity_sensor(sensor::Sensor *sensor) { this->indoor_humidity_sensor_ = sensor; }
  void set_diagnostic_temperature_byte_21_sensor(sensor::Sensor *sensor) {
    this->diagnostic_temperature_byte_21_sensor_ = sensor;
  }
  void set_filter_runtime_sensor(sensor::Sensor *sensor) { this->filter_runtime_sensor_ = sensor; }
  void set_filter_remaining_sensor(sensor::Sensor *sensor) { this->filter_remaining_sensor_ = sensor; }
  void set_filter_cleaning_required_sensor(binary_sensor::BinarySensor *sensor) {
    this->filter_cleaning_required_sensor_ = sensor;
  }
  void set_filter_interval_number(PanasonicACNumber *number, float initial_value);
  void set_filter_reset_button(PanasonicACButton *button);

  void setup() override;
  void loop() override;

 protected:
  ACState state_ = ACState::Initializing;  // Stores the internal state of the AC, used during initialization

  // uint8_t data[10];
  std::vector<uint8_t> data = std::vector<uint8_t>(10);  // Stores the data received from the AC
  std::vector<uint8_t> cmd;                              // Used to build next command

  text_sensor::TextSensor *operational_status_sensor_{nullptr};
  sensor::Sensor *indoor_humidity_sensor_{nullptr};
  sensor::Sensor *diagnostic_temperature_byte_21_sensor_{nullptr};
  sensor::Sensor *filter_runtime_sensor_{nullptr};
  sensor::Sensor *filter_remaining_sensor_{nullptr};
  binary_sensor::BinarySensor *filter_cleaning_required_sensor_{nullptr};
  PanasonicACNumber *filter_interval_number_{nullptr};
  PanasonicACButton *filter_reset_button_{nullptr};

  struct FilterMaintenancePreference {
    uint32_t runtime_seconds;
    float interval_hours;
  };

  ESPPreferenceObject filter_maintenance_pref_;
  uint64_t filter_runtime_ms_{0};
  uint32_t filter_last_status_ms_{0};
  uint32_t filter_last_publish_ms_{0};
  uint32_t filter_last_saved_seconds_{0};
  float filter_interval_hours_{200.0f};
  bool filter_status_initialized_{false};
  bool filter_fan_running_{false};

  void handle_poll();
  void handle_cmd();

  void set_data(bool set);

  void send_command(std::vector<uint8_t> command, CommandType type, uint8_t header);
  void send_packet(const std::vector<uint8_t> &command, CommandType type);

  bool verify_packet();
  void handle_packet();
  bool filter_maintenance_enabled() const;
  void setup_filter_maintenance();
  void update_filter_runtime(uint8_t operational_status);
  void publish_filter_maintenance();
  void save_filter_maintenance();
  void set_filter_interval(float interval_hours);
  void reset_filter_runtime();
};

}  // namespace CNT
}  // namespace panasonic_ac
}  // namespace esphome
