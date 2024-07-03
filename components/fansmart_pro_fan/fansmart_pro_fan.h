#pragma once

#include "esphome.h"
#ifdef USE_API
#include "esphome/components/api/custom_api_device.h"
#endif
#include "esphome/components/fan/fan.h"

#define CMD_PAIR (0x28)
#define CMD_UNPAIR (0x45)

#define CMD_TURN_ON (0x10)
#define CMD_TURN_OFF (0x11)
#define CMD_DIM (0x21)


#define CMD_GENERIC_ONOFF (0x6f)
#define CMD_DIRECTION (0x15)
#define CMD_SPEED (0x31)
#define CMD_FAN_MODE (0x33)
#define CMD_VENTILATION (0x67)
#define CMD_SWAY (0x16)
#define CMD_SWING (0xb0)

namespace esphome {
// namespace fan {
namespace fansmartpro {

class FanSmartProFan : public fan::Fan, public Component
#ifdef USE_API
  , public api::CustomAPIDevice
#endif
{
public:
  void setup() override;
  void dump_config() override;

  void write_state_();
  virtual void control(const fan::FanCall &call);
  virtual fan::FanTraits get_traits();
  void set_target(uint32_t target) { target_ = target; }

  void on_pair();
  void on_unpair();

protected:
  void send_packet(uint16_t cmd, uint8_t param1, uint8_t param2, uint8_t param3 = 0, uint8_t param4 = 0);
  uint8_t tx_count_;
  uint32_t tx_duration_;
  fan::Fan *fan_state_;
  fan::FanTraits traits_;

  uint32_t target_{0};

  bool old_state_{false};
  int old_speed_{0};
  esphome::fan::FanDirection old_direction_{esphome::fan::FanDirection::FORWARD};
  bool old_oscillating_{false};
};

template<typename... Ts> class PairAction : public Action<Ts...> {
 public:
  explicit PairAction(esphome::fan::Fan *state) : state_(state) {}

  void play(Ts... x) override {
    ((FanSmartProFan *)this->state_)->on_pair();
  }

 protected:
  esphome::fan::Fan *state_;
};

template<typename... Ts> class UnpairAction : public Action<Ts...> {
 public:
  explicit UnpairAction(esphome::fan::Fan *state) : state_(state) {}

  void play(Ts... x) override {
    ((FanSmartProFan *)this->state_)->on_unpair();
  }

 protected:
  esphome::fan::Fan *state_;
};

} //namespace fansmartpro
// } //namespace fan
} //namespace esphome
