import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import fan, output
from esphome import automation
from esphome.const import (
    CONF_OUTPUT_ID,
    CONF_TARGET,
    CONF_ID,
)

AUTO_LOAD = ["esp32_ble"]
DEPENDENCIES = ["esp32"]

fansmartpro_ns = cg.esphome_ns.namespace('fansmartpro')
FanSmartProFan = fansmartpro_ns.class_('FanSmartProFan', cg.Component)
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
            cv.Optional(CONF_TARGET, default=0): cv.uint32_t,
	}
    ),
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_OUTPUT_ID])
    await cg.register_component(var, config)
    await fan.register_fan(var, config)

    cg.add(var.set_target(config[CONF_TARGET]))

@automation.register_action(
    "fansmartpro.pair", PairAction, ACTION_ON_PAIR_SCHEMA
)
@automation.register_action(
    "fansmartpro.unpair", UnpairAction, ACTION_ON_UNPAIR_SCHEMA
)
async def fansmartpro_pair_to_code(config, action_id, template_arg, args):
    parent = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(action_id, template_arg, parent)
