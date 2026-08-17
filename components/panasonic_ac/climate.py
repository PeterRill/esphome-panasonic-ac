from esphome.const import (
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_DURATION,
    DEVICE_CLASS_PROBLEM,
    DEVICE_CLASS_TEMPERATURE,
    ENTITY_CATEGORY_CONFIG,
    ENTITY_CATEGORY_DIAGNOSTIC,
    DEVICE_CLASS_POWER,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_HOUR,
    UNIT_PERCENT,
    UNIT_WATT,
)
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import (
    uart,
    climate,
    sensor,
    select,
    switch,
    binary_sensor,
    text_sensor,
    number,
    button,
)

AUTO_LOAD = ["switch", "sensor", "select", "binary_sensor", "text_sensor", "number", "button"]
DEPENDENCIES = ["uart"]

panasonic_ac_ns = cg.esphome_ns.namespace("panasonic_ac")
PanasonicAC = panasonic_ac_ns.class_(
    "PanasonicAC", cg.Component, uart.UARTDevice, climate.Climate
)
panasonic_ac_cnt_ns = panasonic_ac_ns.namespace("CNT")
PanasonicACCNT = panasonic_ac_cnt_ns.class_("PanasonicACCNT", PanasonicAC)
panasonic_ac_wlan_ns = panasonic_ac_ns.namespace("WLAN")
PanasonicACWLAN = panasonic_ac_wlan_ns.class_("PanasonicACWLAN", PanasonicAC)

PanasonicACSwitch = panasonic_ac_ns.class_(
    "PanasonicACSwitch", switch.Switch, cg.Component
)
PanasonicACSelect = panasonic_ac_ns.class_(
    "PanasonicACSelect", select.Select, cg.Component
)
PanasonicACNumber = panasonic_ac_ns.class_(
    "PanasonicACNumber", number.Number, cg.Component
)
PanasonicACButton = panasonic_ac_ns.class_(
    "PanasonicACButton", button.Button, cg.Component
)


CONF_HORIZONTAL_SWING_SELECT = "horizontal_swing_select"
CONF_VERTICAL_SWING_SELECT = "vertical_swing_select"
CONF_OUTSIDE_TEMPERATURE = "outside_temperature"
CONF_OUTSIDE_TEMPERATURE_OFFSET = "outside_temperature_offset"
CONF_CURRENT_TEMPERATURE_SENSOR = "current_temperature_sensor"
CONF_CURRENT_TEMPERATURE_OFFSET = "current_temperature_offset"
CONF_NANOEX_SWITCH = "nanoex_switch"
CONF_ECO_SWITCH = "eco_switch"
CONF_ECONAVI_SWITCH = "econavi_switch"
CONF_MILD_DRY_SWITCH = "mild_dry_switch"
CONF_CURRENT_POWER_CONSUMPTION = "current_power_consumption"
CONF_DEFROST_SENSOR = "defrost_sensor"
CONF_WLAN = "wlan"
CONF_CNT = "cnt"
CONF_OPERATIONAL_STATUS = "operational_status"
CONF_INDOOR_HUMIDITY = "indoor_humidity"
CONF_DIAGNOSTIC_TEMPERATURE_BYTE_21 = "diagnostic_temperature_byte_21"
CONF_OPTION_LABELS = "option_labels"
CONF_LIMIT_VERTICAL_SWING_COOL = "limit_vertical_swing_cool"
CONF_LIMIT_VERTICAL_SWING_HEAT = "limit_vertical_swing_heat"
CONF_POLL_INTERVAL = "poll_interval"
CONF_FILTER_MAINTENANCE = "filter_maintenance"
CONF_FILTER_RUNTIME = "runtime"
CONF_FILTER_REMAINING = "remaining"
CONF_FILTER_CLEANING_REQUIRED = "cleaning_required"
CONF_FILTER_INTERVAL = "interval"
CONF_FILTER_RESET = "reset"
CONF_INITIAL_VALUE = "initial_value"

HORIZONTAL_SWING_OPTIONS = ["auto", "left", "left_center", "center", "right_center", "right"]

VERTICAL_SWING_OPTIONS = ["swing", "auto", "up", "up_center", "center", "down_center", "down"]


def validate_vertical_swing_limit(value):
    options = cv.ensure_list(cv.one_of(*VERTICAL_SWING_OPTIONS, lower=True))(value)
    if not options:
        raise cv.Invalid("At least one vertical swing option must be allowed")
    if len(options) != len(set(options)):
        raise cv.Invalid("Vertical swing limit options must not contain duplicates")
    return options


def validate_vertical_swing_limits(config):
    if (
        CONF_LIMIT_VERTICAL_SWING_COOL in config
        or CONF_LIMIT_VERTICAL_SWING_HEAT in config
    ) and CONF_VERTICAL_SWING_SELECT not in config:
        raise cv.Invalid(
            "vertical_swing_select is required when a vertical swing limit is configured"
        )
    return config

SWITCH_SCHEMA = switch.switch_schema(PanasonicACSwitch).extend(cv.COMPONENT_SCHEMA)

HORIZONTAL_SWING_SELECT_SCHEMA = select.select_schema(
    PanasonicACSelect, icon="mdi:arrow-left-right"
).extend(
    {
        cv.Optional(CONF_OPTION_LABELS): cv.Schema(
            {cv.Optional(option): cv.string_strict for option in HORIZONTAL_SWING_OPTIONS}
        )
    }
)

VERTICAL_SWING_SELECT_SCHEMA = select.select_schema(
    PanasonicACSelect, icon="mdi:arrow-up-down"
).extend(
    {
        cv.Optional(CONF_OPTION_LABELS): cv.Schema(
            {cv.Optional(option): cv.string_strict for option in VERTICAL_SWING_OPTIONS}
        )
    }
)

FILTER_INTERVAL_SCHEMA = number.number_schema(
    PanasonicACNumber,
    icon="mdi:timer-cog-outline",
    entity_category=ENTITY_CATEGORY_CONFIG,
).extend(
    {
        cv.Optional(CONF_INITIAL_VALUE, default=200): cv.float_range(min=50, max=1000),
    }
).extend(cv.COMPONENT_SCHEMA)

FILTER_MAINTENANCE_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_FILTER_RUNTIME): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOUR,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_DURATION,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:air-filter",
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        cv.Required(CONF_FILTER_REMAINING): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOUR,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_DURATION,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:timer-sand",
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        cv.Required(CONF_FILTER_CLEANING_REQUIRED): binary_sensor.binary_sensor_schema(
            device_class=DEVICE_CLASS_PROBLEM,
            icon="mdi:air-filter",
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        cv.Required(CONF_FILTER_INTERVAL): FILTER_INTERVAL_SCHEMA,
        cv.Required(CONF_FILTER_RESET): button.button_schema(
            PanasonicACButton,
            icon="mdi:air-filter",
            entity_category=ENTITY_CATEGORY_CONFIG,
        ).extend(cv.COMPONENT_SCHEMA),
    }
)

PANASONIC_COMMON_SCHEMA = {
    cv.Optional(CONF_HORIZONTAL_SWING_SELECT): HORIZONTAL_SWING_SELECT_SCHEMA,
    cv.Optional(CONF_VERTICAL_SWING_SELECT): VERTICAL_SWING_SELECT_SCHEMA,
    cv.Optional(CONF_LIMIT_VERTICAL_SWING_COOL): validate_vertical_swing_limit,
    cv.Optional(CONF_LIMIT_VERTICAL_SWING_HEAT): validate_vertical_swing_limit,
    cv.Optional(CONF_OUTSIDE_TEMPERATURE): sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_DEFROST_SENSOR): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_NANOEX_SWITCH): SWITCH_SCHEMA,
    cv.Optional(CONF_OUTSIDE_TEMPERATURE_OFFSET): cv.int_range(min=-15, max=15),
    cv.Optional(CONF_CURRENT_TEMPERATURE_OFFSET): cv.int_range(min=-15, max=15),
}

PANASONIC_CNT_SCHEMA = {
    cv.Optional(CONF_ECO_SWITCH): SWITCH_SCHEMA,
    cv.Optional(CONF_ECONAVI_SWITCH): SWITCH_SCHEMA,
    cv.Optional(CONF_MILD_DRY_SWITCH): SWITCH_SCHEMA,
    cv.Optional(CONF_CURRENT_TEMPERATURE_SENSOR): cv.use_id(sensor.Sensor),
    cv.Optional(CONF_CURRENT_POWER_CONSUMPTION): sensor.sensor_schema(
        unit_of_measurement=UNIT_WATT,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_OPERATIONAL_STATUS): text_sensor.text_sensor_schema(),
    cv.Optional(CONF_INDOOR_HUMIDITY): sensor.sensor_schema(
        unit_of_measurement=UNIT_PERCENT,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_HUMIDITY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_DIAGNOSTIC_TEMPERATURE_BYTE_21): sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_FILTER_MAINTENANCE): FILTER_MAINTENANCE_SCHEMA,
}

CONFIG_SCHEMA = cv.All(
    cv.typed_schema(
        {
            CONF_WLAN: climate.climate_schema(PanasonicACWLAN)
            .extend(PANASONIC_COMMON_SCHEMA)
            .extend(
                {
                    cv.Optional(CONF_POLL_INTERVAL, default="30s"): cv.positive_time_period_milliseconds,
                }
            )
            .extend(uart.UART_DEVICE_SCHEMA),
            CONF_CNT: climate.climate_schema(PanasonicACCNT)
            .extend(PANASONIC_COMMON_SCHEMA)
            .extend(PANASONIC_CNT_SCHEMA)
            .extend(
                {
                    cv.Optional(CONF_POLL_INTERVAL, default="5s"): cv.positive_time_period_milliseconds,
                }
            )
            .extend(uart.UART_DEVICE_SCHEMA),
        }
    ),
    validate_vertical_swing_limits,
)


async def to_code(config):
    var = await climate.new_climate(config)
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
    cg.add(var.set_poll_interval(config[CONF_POLL_INTERVAL].total_milliseconds))

    if CONF_HORIZONTAL_SWING_SELECT in config:
        conf = config[CONF_HORIZONTAL_SWING_SELECT]
        labels = conf.get(CONF_OPTION_LABELS, {})
        options = [labels.get(option, option) for option in HORIZONTAL_SWING_OPTIONS]
        swing_select = await select.new_select(conf, options=options)
        await cg.register_component(swing_select, conf)
        cg.add(var.set_horizontal_swing_select(swing_select))

    if CONF_VERTICAL_SWING_SELECT in config:
        conf = config[CONF_VERTICAL_SWING_SELECT]
        labels = conf.get(CONF_OPTION_LABELS, {})
        options = [labels.get(option, option) for option in VERTICAL_SWING_OPTIONS]
        swing_select = await select.new_select(conf, options=options)
        await cg.register_component(swing_select, conf)
        cg.add(var.set_vertical_swing_select(swing_select))

    for option in config.get(CONF_LIMIT_VERTICAL_SWING_COOL, []):
        cg.add(var.add_vertical_swing_cool_limit(VERTICAL_SWING_OPTIONS.index(option)))

    for option in config.get(CONF_LIMIT_VERTICAL_SWING_HEAT, []):
        cg.add(var.add_vertical_swing_heat_limit(VERTICAL_SWING_OPTIONS.index(option)))

    if CONF_OUTSIDE_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_OUTSIDE_TEMPERATURE])
        cg.add(var.set_outside_temperature_sensor(sens))

    if CONF_DEFROST_SENSOR in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_DEFROST_SENSOR])
        cg.add(var.set_defrost_sensor(sens))

    if CONF_OUTSIDE_TEMPERATURE_OFFSET in config:
        cg.add(var.set_outside_temperature_offset(config[CONF_OUTSIDE_TEMPERATURE_OFFSET]))

    for s in [CONF_ECO_SWITCH, CONF_NANOEX_SWITCH, CONF_MILD_DRY_SWITCH, CONF_ECONAVI_SWITCH]:
        if s in config:
            conf = config[s]
            a_switch = await switch.new_switch(conf)
            await cg.register_component(a_switch, conf)
            cg.add(getattr(var, f"set_{s}")(a_switch))

    if CONF_CURRENT_TEMPERATURE_SENSOR in config:
        sens = await cg.get_variable(config[CONF_CURRENT_TEMPERATURE_SENSOR])
        cg.add(var.set_current_temperature_sensor(sens))

    if CONF_CURRENT_TEMPERATURE_OFFSET in config:
        cg.add(var.set_current_temperature_offset(config[CONF_CURRENT_TEMPERATURE_OFFSET]))

    if CONF_CURRENT_POWER_CONSUMPTION in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT_POWER_CONSUMPTION])
        cg.add(var.set_current_power_consumption_sensor(sens))

    if CONF_OPERATIONAL_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_OPERATIONAL_STATUS])
        cg.add(var.set_operational_status_sensor(sens))

    if CONF_INDOOR_HUMIDITY in config:
        sens = await sensor.new_sensor(config[CONF_INDOOR_HUMIDITY])
        cg.add(var.set_indoor_humidity_sensor(sens))

    if CONF_DIAGNOSTIC_TEMPERATURE_BYTE_21 in config:
        sens = await sensor.new_sensor(config[CONF_DIAGNOSTIC_TEMPERATURE_BYTE_21])
        cg.add(var.set_diagnostic_temperature_byte_21_sensor(sens))

    if CONF_FILTER_MAINTENANCE in config:
        conf = config[CONF_FILTER_MAINTENANCE]

        runtime = await sensor.new_sensor(conf[CONF_FILTER_RUNTIME])
        cg.add(var.set_filter_runtime_sensor(runtime))

        remaining = await sensor.new_sensor(conf[CONF_FILTER_REMAINING])
        cg.add(var.set_filter_remaining_sensor(remaining))

        due = await binary_sensor.new_binary_sensor(conf[CONF_FILTER_CLEANING_REQUIRED])
        cg.add(var.set_filter_cleaning_required_sensor(due))

        interval_conf = conf[CONF_FILTER_INTERVAL]
        interval = await number.new_number(
            interval_conf, min_value=50, max_value=1000, step=25
        )
        await cg.register_component(interval, interval_conf)
        cg.add(
            var.set_filter_interval_number(
                interval, interval_conf[CONF_INITIAL_VALUE]
            )
        )

        reset_conf = conf[CONF_FILTER_RESET]
        reset = await button.new_button(reset_conf)
        await cg.register_component(reset, reset_conf)
        cg.add(var.set_filter_reset_button(reset))
