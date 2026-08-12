Schneider insight gateway modbus tcp victron client
put insight.py in /opt/victronenergy/dbus-modbus-client

nano /opt/victronenergy/dbus-modbus-client/dbus-modbus-client.py

Scroll down to this section:

import abb
import carlo_gavazzi
import comap
import cre
import deif
import dse
import ev_charger
import smappee
import victron_em
import insight
^^^ Add this include, and save
