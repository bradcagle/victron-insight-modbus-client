import dbus
import struct
import device
import probe
from register import *


class Battery503(device.SubDevice):
    default_role = 'battery'
    default_instance = 40

    def device_init(self):
        super().device_init()

        self.data_regs = [
            Reg_u32b(512, '/Dc/0/Voltage', 1000, '%.1f V'),
            Reg_s32b(514, '/Dc/0/Current', 1000, '%.1f A'),
            Reg_s32b(516, '/Dc/0/Temperature', 1000, '%.1f C'),
            Reg_s32b(966, '/Dc/0/Power', 1, '%.1f W'),
            Reg_u32b(968, '/Soc', 1, '%.1f SOC'),
        ]


class Insight503(device.ModbusDevice):
    vendor_id = 'schneider'
    vendor_name = 'Schneider'
    productid = 0xB050
    productname = 'Insight Gateway'
    min_timeout = 0.5
    device_type = 'Gateway'
    default_role = 'inverter'
    default_instance = 50

    def device_init(self):
        self.info_regs = [
            Reg_text(30, 10, '/FirmwareVersion'),
            #Reg_text(0,  8,  '/CustomName'),
            Reg_text(43, 8,  '/Serial'),
        ]

        self.name = 'insight_gateway' 

        self.data_regs = [
            Reg_u32b(96,  '/Ac/Out/L1/P', 1, '%.1f W'),
            Reg_u32b(104, '/Ac/Out/L1/V', 1000, '%.1f V'),
            Reg_s32b(108, '/Ac/Out/L1/I', 1000, '%.1f A'),
            Reg_u32b(512, '/Dc/0/Voltage', 1000, '%.1f V'),
        ]

        self.subdevices = [
            Battery503(self, 'battery'),
        ]

    def device_init_late(self):
        super().device_init_late()
        self.dbus.add_path('/State', 9)
        self.dbus.add_path('/Mode', 2)

    def get_unique(self):
        return self.name




class Battery502(device.SubDevice):
    default_role = 'battery'
    default_instance = 40

    def device_init(self):
        super().device_init()

        self.data_regs = [
            Reg_u16(40278, '/Dc/0/Voltage', 100, '%.1f V'),
            Reg_s16(40288, '/Dc/0/Current', 100, '%.1f A'),
            Reg_s16(40291, '/Dc/0/Power', 1, '%.1f W'),
            Reg_u16(40255, '/Soc', 1, '%.1f SOC'),
        ]


class Insight502(device.ModbusDevice):
    vendor_id = 'schneider'
    vendor_name = 'Schneider'
    productid = 0xB051
    productname = 'Insight Gateway'
    min_timeout = 0.5
    device_type = 'Gateway'
    default_role = 'inverter'
    default_instance = 50

    def device_init(self):
        self.info_regs = [
            Reg_text(40044, 8,  '/FirmwareVersion'),
            #Reg_text(40020, 16, '/CustomName'),
            Reg_text(40052, 16, '/Serial'),
        ]

        self.name = 'insight_gateway' 

        self.data_regs = [
            Reg_s16(40084,  '/Ac/Out/L1/P', 1, '%.1f W'),
            Reg_u16(40077, '/Ac/Out/L1/V', 100, '%.1f V'),
            Reg_u16(40072, '/Ac/Out/L1/I', 100, '%.1f A'),
            #Reg_u16(40099, '/Dc/0/Voltage', 1, '%.1f V'),
        ]

        self.subdevices = [
            Battery502(self, 'battery'),
        ]

    def device_init_late(self):
        super().device_init_late()
        self.dbus.add_path('/State', 9)
        self.dbus.add_path('/Mode', 2)

    def get_unique(self):
        return self.name




models = {
    '865-0335': {
        'model': 'Insight',
        'handler': Insight503,
    },
    'Conext Gateway': {
        'model': 'Insight',
        'handler': Insight502,
    }
}


# Port 503 probe
probe.add_handler(probe.ModelRegister(Reg_text(10, 8), models, methods=['tcp'], units=[1]))

# Port 502 probe
probe.add_handler(probe.ModelRegister(Reg_text(40020, 16), models, methods=['tcp'], units=[1]))
