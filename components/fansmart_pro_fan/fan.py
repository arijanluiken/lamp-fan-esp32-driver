import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import fan, output
from esphome import automation
from esphome.const import (
    CONF_DURATION,
    CONF_CONSTANT_BRIGHTNESS,
    CONF_OUTPUT_ID,
    CONF_COLD_WHITE_COLOR_TEMPERATURE,
    CONF_WARM_WHITE_COLOR_TEMPERATURE,
    CONF_REVERSED,
    CONF_MIN_BRIGHTNESS, # New in 2023.5
    CONF_ID,
)

AUTO_LOAD = ["esp32_ble"]
DEPENDENCIES = ["esp32"]

fansmartpro_ns = cg.esphome_ns.namespace('fansmartpro')
FanSmartProFan = fansmartpro_ns.class_('FanSmartProFan', cg.Component, fan.FanOutput)
PairAction = fansmartpro_ns.class_("PairAction", automation.Action)
UnpairAction = fansmartpro_ns.class_("UnpairAction", automation.Action)


ACTION_ON_PAIR_SCHEMA = cv.All(
    automation.maybe_simple_id(
        {
            cv.Required(CONF_ID): cv.use_id(fan.FanState),
        }
    )
)

ACTION_ON_UNPAIR_SCHEMA = cv.All(
    automation.maybe_simple_id(
        {
            cv.Required(CONF_ID): cv.use_id(fan.FanState),
        }
    )
)

CONFIG_SCHEMA = cv.All(
    fan.FAN_SCHEMA.extend(
        {
            cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(FanSmartProFan),
	}
    ),
#    fan.RGB_LIGHT_SCHEMA.extend(
#        {
#            cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(FanSmartProFan),
#            cv.Optional(CONF_DURATION, default=100): cv.positive_int,
#            cv.Optional(CONF_COLD_WHITE_COLOR_TEMPERATURE): cv.color_temperature,
#            cv.Optional(CONF_WARM_WHITE_COLOR_TEMPERATURE): cv.color_temperature,
#            cv.Optional(CONF_CONSTANT_BRIGHTNESS, default=False): cv.boolean,
#            cv.Optional(CONF_REVERSED, default=False): cv.boolean,
#            cv.Optional(CONF_MIN_BRIGHTNESS, default=0x7): cv.hex_uint8_t,
#        }
#    ),
#    cv.has_none_or_all_keys(
#        [CONF_COLD_WHITE_COLOR_TEMPERATURE, CONF_WARM_WHITE_COLOR_TEMPERATURE]
#    ),
#    fan.validate_color_temperature_channels,
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_OUTPUT_ID])
    await cg.register_component(var, config)
    await fan.register_fan(var, config)

#    if CONF_COLD_WHITE_COLOR_TEMPERATURE in config:
#        cg.add(
#            var.set_cold_white_temperature(config[CONF_COLD_WHITE_COLOR_TEMPERATURE])
#        )

#    if CONF_WARM_WHITE_COLOR_TEMPERATURE in config:
#        cg.add(
#            var.set_warm_white_temperature(config[CONF_WARM_WHITE_COLOR_TEMPERATURE])
#        )

#    cg.add(var.set_constant_brightness(config[CONF_CONSTANT_BRIGHTNESS]))
#    cg.add(var.set_reversed(config[CONF_REVERSED]))
#    cg.add(var.set_min_brightness(config[CONF_MIN_BRIGHTNESS]))
#    cg.add(var.set_tx_duration(config[CONF_DURATION]))


@automation.register_action(
    "fansmartpro.pair", PairAction, ACTION_ON_PAIR_SCHEMA
)
@automation.register_action(
    "fansmartpro.unpair", UnpairAction, ACTION_ON_UNPAIR_SCHEMA
)
async def fansmartpro_pair_to_code(config, action_id, template_arg, args):
    parent = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(action_id, template_arg, parent)
