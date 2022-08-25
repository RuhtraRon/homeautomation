#!/usr/bin/env python3


import datetime
import logging

import shc.log.in_memory
from shc.datatypes import RangeFloat1, RGBUInt8
from shc.interfaces.mqtt import MQTTClientInterface
from shc.interfaces.tasmota import TasmotaInterface
from shc.web.log_widgets import LogListDataSpec
from shc.web.widgets import Switch, Slider, DisplayButton, ButtonGroup, icon, TextDisplay

mqtt = MQTTClientInterface('10.0.0.23')
# a tasmota RGB (or RGBW) lamp/LED strip with IR receiver
# tasmota_led = TasmotaInterface(mqtt, 'my_tasmota_device_topic')
tasmota_washer = TasmotaInterface(mqtt, 'washer')
tasmota_patio = TasmotaInterface(mqtt, 'patio')

# Create a Web server with a single index page
web_server = shc.web.WebServer('', 8081, index_name='index')
index_page = web_server.page('index', 'Home', menu_entry=True, menu_icon='home')

# Create an in-memory log for the IR commands received in the last 10 minutes
# ir_log = shc.log.in_memory.InMemoryPersistenceVariable(str, keep=datetime.timedelta(minutes=10))
# Show the logged IR commands in a list view on the web page
# index_page.add_item(shc.web.log_widgets.LogListWidget(datetime.timedelta(minutes=5), [
#     LogListDataSpec(ir_log)
# ]))
# Send the IR commands received by the Tasmota device to the in-memory log
# tasmota_led.ir_receiver().connect(ir_log, convert=(lambda v: v.hex(), lambda x: x))

# State variables for on/off, dimmer and RGB color of the Tasmota device
washer_power = shc.Variable(bool)\
    .connect(tasmota_washer.power())
washer_online = shc.Variable(bool)\
    .connect(tasmota_washer.online())
patio_power = shc.Variable(bool)\
    .connect(tasmota_patio.power())
patio_online = shc.Variable(bool)\
    .connect(tasmota_patio.online())
# dimmer = shc.Variable(RangeFloat1)\
#     .connect(tasmota_washer.dimmer(), convert=True)
en_power = shc.Variable(float)\
    .connect(tasmota_washer.energy_power())
en_current = shc.Variable(float)\
    .connect(tasmota_washer.energy_current())
en_voltage = shc.Variable(float)\
    .connect(tasmota_washer.energy_voltage())
# color = shc.Variable(RGBUInt8)\
#     .connect(tasmota_washer.color_rgb())

index_page.new_segment('Devices')
# Show an indicator for the MQTT connection state of the Tasmota device on the web page
index_page.add_item(ButtonGroup("Washer Online?", [
    DisplayButton(label=icon('plug'), color="teal").connect(washer_online),
]))
index_page.add_item(ButtonGroup("Patio Online?", [
    DisplayButton(label=icon('plug'), color="teal").connect(patio_online),
]))

# Add UI controls for the on/off state and the dimmer value
index_page.add_item(Switch("Patio Power").connect(patio_power))
# index_page.add_item(Slider("Dimmer").connect(dimmer))


# Add UI controls for the the RGB color components
index_page.new_segment('Washer')
index_page.add_item(Switch("Power").connect(washer_power))
index_page.add_item(TextDisplay(float, '{:.2f}', "Current").connect(en_current))
index_page.add_item(TextDisplay(float, '{:.2f}', "Voltage").connect(en_voltage))
index_page.add_item(TextDisplay(float, '{:.2f}', "Power").connect(en_power))
# index_page.add_item(Slider("Rot", color='red').connect(color.field('red'), convert=True))
# index_page.add_item(Slider("Grün", color='green').connect(color.field('green'), convert=True))
# index_page.add_item(Slider("Blau", color='blue').connect(color.field('blue'), convert=True))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    shc.main()
