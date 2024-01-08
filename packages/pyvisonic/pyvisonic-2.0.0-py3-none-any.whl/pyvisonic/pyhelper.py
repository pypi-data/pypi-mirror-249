
import os

# The defaults are set for use in Home Assistant.
#    If using CircuitPython then set these values in the settings.toml file
MicroPython = os.getenv("MICRO_PYTHON")

if MicroPython is not None:
    #import time as datetime
    from adafruit_datetime import datetime, timedelta
    import adafruit_logging as logging
    ABC = object
    Callable = object
    TypedDict = object
    List = object

    class ABC:
        pass

    def abstractmethod(f):
        return f

    # get the current date and time
    def _getUTCTime() -> datetime:
        return datetime.now() # UTC

else:
    import logging
    import datetime
    from abc import abstractmethod
    from datetime import datetime, timedelta
    from typing import Callable, List, TypedDict

    # get the current date and time
    def _getUTCTime() -> datetime:
        return datetime.utcnow()

#if DontUseLogger is None:
log = logging.getLogger(__name__)

import sys
import time
import math
import json
import asyncio
import re
#from time import sleep

try:
    from .pyconst import AlIntEnum, NO_DELAY_SET, PanelConfig, AlConfiguration, AlPanelMode, AlPanelCommand, AlPanelStatus, AlTroubleType, AlAlarmType, AlSensorCondition, AlCommandStatus, AlX10Command, AlCondition, AlPanelInterface, AlSensorDevice, AlLogPanelEvent, AlSensorType, AlSwitchDevice
except:
    from pyconst import AlIntEnum, NO_DELAY_SET, PanelConfig, AlConfiguration, AlPanelMode, AlPanelCommand, AlPanelStatus, AlTroubleType, AlAlarmType, AlSensorCondition, AlCommandStatus, AlX10Command, AlCondition, AlPanelInterface, AlSensorDevice, AlLogPanelEvent, AlSensorType, AlSwitchDevice

# Event Type Constants
EVENT_TYPE_SYSTEM_RESET = 0x60
EVENT_TYPE_FORCE_ARM = 0x59
EVENT_TYPE_DISARM = 0x55
EVENT_TYPE_SENSOR_TAMPER = 0x06
EVENT_TYPE_PANEL_TAMPER = 0x07
EVENT_TYPE_TAMPER_ALARM_A = 0x08
EVENT_TYPE_TAMPER_ALARM_B = 0x09
EVENT_TYPE_ALARM_CANCEL = 0x1B
EVENT_TYPE_FIRE_RESTORE = 0x21
EVENT_TYPE_FLOOD_ALERT_RESTORE = 0x4A
EVENT_TYPE_GAS_TROUBLE_RESTORE = 0x4E
EVENT_TYPE_DELAY_RESTORE = 0x13
EVENT_TYPE_CONFIRM_ALARM = 0x0E


# These 2 dictionaries are subsets of pmLogEvent_t
pmPanelAlarmType_t = {
   0x00 : AlAlarmType.NONE,     0x01 : AlAlarmType.INTRUDER,  0x02 : AlAlarmType.INTRUDER, 0x03 : AlAlarmType.INTRUDER,
   0x04 : AlAlarmType.INTRUDER, 0x05 : AlAlarmType.INTRUDER,  0x06 : AlAlarmType.TAMPER,   0x07 : AlAlarmType.TAMPER,
   0x08 : AlAlarmType.TAMPER,   0x09 : AlAlarmType.TAMPER,    0x0B : AlAlarmType.PANIC,    0x0C : AlAlarmType.PANIC,
   0x20 : AlAlarmType.FIRE,     0x23 : AlAlarmType.EMERGENCY, 0x49 : AlAlarmType.GAS,      0x4D : AlAlarmType.FLOOD,
}

pmPanelTroubleType_t = {
   0x00 : AlTroubleType.NONE,          0x01 : AlTroubleType.GENERAL,   0x0A : AlTroubleType.COMMUNICATION, 0x0F : AlTroubleType.GENERAL,
   0x29 : AlTroubleType.BATTERY,       0x2B : AlTroubleType.POWER,     0x2D : AlTroubleType.BATTERY,       0x2F : AlTroubleType.JAMMING,
   0x31 : AlTroubleType.COMMUNICATION, 0x33 : AlTroubleType.TELEPHONE, 0x36 : AlTroubleType.POWER,         0x38 : AlTroubleType.BATTERY,
   0x3B : AlTroubleType.BATTERY,       0x3C : AlTroubleType.BATTERY,   0x40 : AlTroubleType.BATTERY,       0x43 : AlTroubleType.BATTERY
}

def toBool(val) -> bool:
    if type(val) == bool:
        return val
    elif type(val) == int:
        return val != 0
    elif type(val) == str:
        v = val.lower()
        return not (v == "no" or v == "false" or v == "0")
    #print("Visonic unable to decode boolean value {val}    type is {type(val)}")
    return False

def capitalize(s):
    return s[0].upper() + s[1:]

def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda word: capitalize(word.group(0)), s)

class AlSensorDeviceHelper(AlSensorDevice):

    def __init__(self, **kwargs):
        self._callback = []
        self.id = kwargs.get("id", -1)  # int   device id
        self.stype = kwargs.get("stype", AlSensorType.UNKNOWN)  # AlSensorType  sensor type
        self.ztypeName = kwargs.get("ztypeName", None)  # str   Zone Type Name
        self.sid = kwargs.get("sid", 0)  # int   sensor id
        self.ztype = kwargs.get("ztype", 0)  # int   zone type
        self.zname = kwargs.get("zname", None)  # str   zone name
        self.zchime = kwargs.get("zchime", None)  # str   zone chime
        self.partition = kwargs.get("partition", 0)  # set   partition set (could be in more than one partition)
        self.bypass = kwargs.get("bypass", False)  # bool  if bypass is set on this sensor
        self.lowbatt = kwargs.get("lowbatt", False)  # bool  if this sensor has a low battery
        self.status = kwargs.get("status", False)  # bool  status, as returned by the A5 message
        self.tamper = kwargs.get("tamper", False)  # bool  tamper, as returned by the A5 message
        self.ztamper = kwargs.get("ztamper", False)  # bool  zone tamper, as returned by the A5 message
        self.ztrip = kwargs.get("ztrip", False)  # bool  zone trip, as returned by the A5 message
        self.enrolled = kwargs.get("enrolled", False)  # bool  enrolled, as returned by the A5 message
        self.triggered = kwargs.get("triggered", False)  # bool  triggered, as returned by the A5 message
        self.utctriggertime = None  # datetime  This is used to time out the triggered value and set it back to false
        self.triggertime = None     # datetime  This is used to time stamp in local time the occurance of the trigger
        self.model = kwargs.get("model", None)  # str   device model
        self.motiondelaytime = kwargs.get("motiondelaytime", None)  # int   device model

    def __str__(self):
        stypestr = ""
        if self.stype != AlSensorType.UNKNOWN:
            stypestr = titlecase(str(self.stype).replace("_"," "))
        elif self.sid is not None:
            stypestr = "Unk " + str(self.sid)
        else:
            stypestr = "Unknown"
        strn = ""
        strn = strn + ("id=None" if self.id == None else "id={0:<2}".format(self.id))
        #strn = strn + (" Zone=None" if self.dname == None else " Zone={0:<4}".format(self.dname[:4]))
        strn = strn + (" Type={0:<8}".format(stypestr))
        # temporarily miss it out to shorten the line in debug messages        strn = strn + (" model=None" if self.model == None else " model={0:<8}".format(self.model[:14]))
        # temporarily miss it out to shorten the line in debug messages        strn = strn + (" sid=None"       if self.sid == None else       " sid={0:<3}".format(self.sid, type(self.sid)))
        # temporarily miss it out to shorten the line in debug messages        strn = strn + (" ztype=None"     if self.ztype == None else     " ztype={0:<2}".format(self.ztype, type(self.ztype)))
        strn = strn + (" Loc=None          " if self.zname == None else " Loc={0:<14}".format(self.zname[:14]))
        strn = strn + (" ztypeName=None" if self.ztypeName == None else " ztypeName={0:<10}".format(self.ztypeName[:10]))
        strn = strn + (" ztamper=None" if self.ztamper == None else " ztamper={0:<2}".format(self.ztamper))
        strn = strn + (" ztrip=None" if self.ztrip == None else " ztrip={0:<2}".format(self.ztrip))
        # temporarily miss it out to shorten the line in debug messages        strn = strn + (" zchime=None"    if self.zchime == None else    " zchime={0:<12}".format(self.zchime, type(self.zchime)))
        # temporarily miss it out to shorten the line in debug messages        strn = strn + (" partition=None" if self.partition == None else " partition={0}".format(self.partition, type(self.partition)))
        strn = strn + (" bypass=None" if self.bypass == None else " bypass={0:<2}".format(self.bypass))
        strn = strn + (" lowbatt=None" if self.lowbatt == None else " lowbatt={0:<2}".format(self.lowbatt))
        strn = strn + (" status=None" if self.status == None else " status={0:<2}".format(self.status))
        strn = strn + (" tamper=None" if self.tamper == None else " tamper={0:<2}".format(self.tamper))
        strn = strn + (" enrolled=None" if self.enrolled == None else " enrolled={0:<2}".format(self.enrolled))
        strn = strn + (" triggered=None" if self.triggered == None else " triggered={0:<2}".format(self.triggered))

        if self.motiondelaytime is not None and (self.stype == AlSensorType.MOTION or self.stype == AlSensorType.CAMERA):
            strn = strn + (" delay={0:<7}".format("Not Set" if self.motiondelaytime == 0xFFFF else str(self.motiondelaytime)))

        return strn

    def __eq__(self, other):
        if other is None:
            return False
        if self is None:
            return False
        return (
            self.id == other.id
            and self.stype == other.stype
            and self.sid == other.sid
            and self.model == other.model
            and self.ztype == other.ztype
            and self.zname == other.zname
            and self.zchime == other.zchime
            and self.partition == other.partition
            and self.bypass == other.bypass
            and self.lowbatt == other.lowbatt
            and self.status == other.status
            and self.tamper == other.tamper
            and self.ztypeName == other.ztypeName
            and self.ztamper == other.ztamper
            and self.ztrip == other.ztrip
            and self.enrolled == other.enrolled
            and self.triggered == other.triggered
            #and self.utctriggertime == other.utctriggertime
            #and self.triggertime == other.triggertime
            and self.motiondelaytime == other.motiondelaytime
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def getDeviceID(self):
        return self.id

    def isTriggered(self) -> bool:
        return self.triggered

    def isOpen(self) -> bool:
        return self.status

    def isEnrolled(self) -> bool:
        return self.enrolled

    def isBypass(self) -> bool:
        return self.bypass

    def isLowBattery(self) -> bool:
        return self.lowbatt

    def getSensorModel(self) -> str:
        if self.model is not None:
            return self.model
        return "Unknown"

    def getSensorType(self) -> AlSensorType:
        return self.stype

    def getLastTriggerTime(self) -> datetime:
        return self.triggertime

    def getZoneLocation(self) -> str:
        return self.zname

    def getZoneType(self) -> str:
        return self.ztypeName

    def getChimeType(self) -> str:
        return self.zchime

    # Not abstract but implement if possible
    def isTamper(self) -> bool:
        return self.tamper

    # Not abstract but implement if possible
    def isZoneTamper(self) -> bool:
        return self.ztamper

    # Not abstract but implement if possible
    def getRawSensorIdentifier(self) -> int:
        return self.sid

    # Not abstract but implement if possible
    #    This is only applicable to PowerMaster Panels. It is the motion off time per sensor.
    def getMotionDelayTime(self) -> str:
        if self.motiondelaytime is not None and (self.getSensorType() == AlSensorType.MOTION or self.getSensorType() == AlSensorType.CAMERA):
            return NO_DELAY_SET if self.motiondelaytime == 0xFFFF else str(self.motiondelaytime)
        return NO_DELAY_SET

    def onChange(self, callback : Callable = None):
        self._callback.append(callback)

    def pushChange(self, s : AlSensorCondition):
        for cb in self._callback:
            cb(self, s)

    def fromJSON(self, decode):
#        self.id = kwargs.get("id", None)  # int   device id
#        #self.dname = kwargs.get("dname", None)  # str   device name
#        self.sid = kwargs.get("sid", None)  # int   sensor id
#        self.ztype = kwargs.get("ztype", None)  # int   zone type
#        self.ztypeName = kwargs.get("ztypeName", None)  # str   Zone Type Name
#        self.partition = kwargs.get("partition", None)  # set   partition set (could be in more than one partition)
#        self.ztrip = kwargs.get("ztrip", False)  # bool  zone trip, as returned by the A5 message

        #log.debug("   In sensor fromJSON start {0}".format(self))
        if "triggered" in decode:
            self.triggered = toBool(decode["triggered"])
        if "open" in decode:
            self.status = toBool(decode["open"])
        if "bypass" in decode:
            self.bypass = toBool(decode["bypass"])
        if "low_battery" in decode:
            self.lowbatt = toBool(decode["low_battery"])
        if "enrolled" in decode:
            self.enrolled = toBool(decode["enrolled"])
        if "sensor_type" in decode:
            st = decode["sensor_type"]
            self.stype = AlSensorType.value_of(st.upper())
        if "trigger_time" in decode:
            self.utctriggertime = datetime.fromisoformat(decode["trigger_time"]) if str(decode["trigger_time"]) != "" else None
        if "location" in decode:
            self.zname = titlecase(decode["location"])
        if "zone_type" in decode:
            self.ztypeName = titlecase(decode["zone_type"])
        if "device_tamper" in decode:
            self.tamper = toBool(decode["device_tamper"])
        if "zone_tamper" in decode:
            self.ztamper = toBool(decode["zone_tamper"])
        if "chime" in decode:
            self.zchime = titlecase(decode["chime"])
        if "sensor_model" in decode:
            self.model = titlecase(decode["sensor_model"])
        if "motion_delay_time" in decode:
            self.motiondelaytime = titlecase(decode["motion_delay_time"])
        #log.debug("   In sensor fromJSON end   {0}".format(self))

    def toJSON(self) -> dict:
        dd=json.dumps({
             "zone": self.getDeviceID(),
             "triggered": self.isTriggered(),
             "open": self.isOpen(),
             "bypass": self.isBypass(),
             "low_battery": self.isLowBattery(),
             "enrolled": self.isEnrolled(),
             "sensor_type": str(self.getSensorType()),
             "trigger_time": datetime.isoformat(self.getLastTriggerTime()) if self.getLastTriggerTime() is not None else "",
             "location": str(self.getZoneLocation()),
             "zone_type": str(self.getZoneType()),
             "device_tamper": self.isTamper(),
             "zone_tamper": self.isZoneTamper(),
             "sensor_model": str(self.getSensorModel()),
             "motion_delay_time": "" if self.getMotionDelayTime() is None else self.getMotionDelayTime(),
             "chime":  str(self.getChimeType()) })    # , ensure_ascii=True
        return dd


class AlSwitchDeviceHelper(AlSwitchDevice):

    def __init__(self, **kwargs):
        self._callback = []
        self.enabled = True #kwargs.get("enabled", False)  # bool  enabled
        self.id = kwargs.get("id", None)  # int   device id
        #self.name = kwargs.get("name", None)  # str   name
        self.type = kwargs.get("type", None)  # str   type
        self.location = kwargs.get("location", None)  # str   location
        self.state = False

    def __str__(self):
        strn = ""
        strn = strn + ("id=None" if self.id == None else "id={0:<2}".format(self.id))
        #strn = strn + (" name=None" if self.name == None else " name={0:<4}".format(self.name))
        strn = strn + (" type=None" if self.type == None else " type={0:<15}".format(self.type))
        strn = strn + (" location=None" if self.location == None else " location={0:<14}".format(self.location))
        strn = strn + (" enabled=None" if self.enabled == None else " enabled={0:<2}".format(self.enabled))
        strn = strn + (" state=None" if self.state == None else " state={0:<8}".format(self.state))
        return strn

    def __eq__(self, other):
        if other is None:
            return False
        if self is None:
            return False
        return (
            self.id == other.id
            and self.enabled == other.enabled
            #and self.name == other.name
            and self.type == other.type
            and self.location == other.location
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def getDeviceID(self):
        return self.id

    def isEnabled(self):
        return self.enabled

    def getType(self) -> str:
        return self.type

    def getLocation(self) -> str:
        return self.location

    def isOn(self) -> bool:
        return self.state #

    def onChange(self, callback : Callable = None):
        self._callback.append(callback)

    def pushChange(self):
        for cb in self._callback:
            cb(self)

    def fromJSON(self, decode):
        if "enabled" in decode:
            self.enabled = toBool(decode["enabled"])
        if "type" in decode:
            self.type = titlecase(decode["type"])
        if "location" in decode:
            self.location = titlecase(decode["location"])
        if "state" in decode:
            s = AlX10Command.value_of(decode["state"].upper())
            self.state = (s == AlX10Command.ON or s == AlX10Command.BRIGHTEN or s == AlX10Command.DIM)

    def toJSON(self) -> dict:
        dd=json.dumps({
             #"name": str(switch.createFriendlyName()),
             "id": self.getDeviceID(),
             "enabled": self.isEnabled(),
             "type": str(self.getType()),
             "location": str(self.getLocation()),
             "state":  "On" if self.state else "Off" })  # , ensure_ascii=True
        return dd


class AlPanelInterfaceHelper(AlPanelInterface):

    def __init__(self):
        """Initialize class."""
        super().__init__()
        # Class Variables
        self.suspendAllOperations = False

        # set the event callback handlers to None
        self.onPanelChangeHandler = None
        self.onNewSensorHandler = None
        self.onNewSwitchHandler = None
        self.onDisconnectHandler = None
        self.onPanelLogHandler = None

        ########################################################################
        # Global Variables that define the overall panel status
        ########################################################################
        self.PanelMode = AlPanelMode.UNKNOWN

        self.PanelState = AlPanelStatus.UNKNOWN
        self.PanelReady = False
        self.PanelTamper = False
        self.PanelAlertInMemory = False
        self.PanelBypass = False
        self.SirenActive = False

        self.PanelAlarmStatus = AlAlarmType.NONE
        self.PanelTroubleStatus = AlTroubleType.NONE
        self.PanelLastEvent = "Unknown"

        # Keep a dict of the sensors so we know if its new or existing
        self.SensorList = { }
        # Keep a dict of the switches so we know if its new or existing
        self.SwitchList = { }

        self.setLastPanelEventData()

        # Whether its a powermax or powermaster
        self.PowerMaster = None
        # Define model type to be unknown
        self.PanelModel = "Unknown"
        self.PanelType = None

        self.PanelLastEventData = self.setLastEventData()

    def getPanelModel(self):
        return self.PanelModel

    def updateSettings(self, newdata: PanelConfig):
        pass

    def isSirenActive(self) -> bool:
        if not self.suspendAllOperations:
            return self.SirenActive
        return False

    def getPanelStatus(self) -> AlPanelStatus:
        if not self.suspendAllOperations:
            return self.PanelState
        return AlPanelStatus.UNKNOWN

    def getPanelMode(self) -> AlPanelMode:
        if not self.suspendAllOperations:
            return self.PanelMode
        return AlPanelMode.UNKNOWN

    def isPanelReady(self) -> bool:
        """ Get the panel ready state """
        if not self.suspendAllOperations:
            return self.PanelReady
        return False

    def getPanelTrouble(self) -> AlTroubleType:
        """ Get the panel trouble state """
        if not self.suspendAllOperations:
            return self.PanelTroubleStatus
        return AlTroubleType.UNKNOWN

    def isPanelBypass(self) -> bool:
        """ Get the panel bypass state """
        if not self.suspendAllOperations:
            return self.PanelBypass
        return False

    def getPanelLastEvent(self) -> str:
        return self.PanelLastEvent

    #def getPanelTroubleStatus(self) -> str:
    #    """ Get the panel trouble state string """
    #    return pmPanelTroubleType_t[self.PanelTroubleStatus]

    def requestArm(self, state : AlPanelCommand, code : str = "") -> AlCommandStatus:
        """ Send a request to the panel to Arm/Disarm """
        return AlCommandStatus.FAIL_ABSTRACT_CLASS_NOT_IMPLEMENTED

    # device in range 0 to 15 (inclusive), 0=PGM, 1 to 15 are X10 devices
    # state is the X10 state to set the switch
    def setX10(self, device : int, state : AlX10Command) -> AlCommandStatus:
        """ Se the state of an X10 switch. """
        return AlCommandStatus.FAIL_ABSTRACT_CLASS_NOT_IMPLEMENTED

    # Set the Sensor Bypass to Arm/Bypass individual sensors
    # sensor in range 1 to 31 for PowerMax and 1 to 63 for PowerMaster (inclusive) depending on alarm
    # bypassValue is False to Arm the Sensor and True to Bypass the sensor
    # Set code to:
    #    None when we are in Powerlink or Standard Plus and to use the code code from EPROM
    #    "1234" a 4 digit code for any panel mode to use that code
    #    anything else to use code "0000" (this is unlikely to work on any panel)
    def setSensorBypassState(self, sensor : int, bypassValue : bool, code : str = "") -> AlCommandStatus:
        """ Set or Clear Sensor Bypass """
        return AlCommandStatus.FAIL_ABSTRACT_CLASS_NOT_IMPLEMENTED

    # Get the panels event log
    # Set code to:
    #    None when we are in Powerlink or Standard Plus and to use the code code from EPROM
    #    "1234" a 4 digit code for any panel mode to use that code
    #    anything else to use code "0000" (this is unlikely to work on any panel)
    def getEventLog(self, code : str = "") -> AlCommandStatus:
        """ Get Panel Event Log """
        return AlCommandStatus.FAIL_ABSTRACT_CLASS_NOT_IMPLEMENTED

    # Convert byte array to a string of hex values
    def _toString(self, array_alpha: bytearray):
        return "".join("%02x " % b for b in array_alpha)

    # get the current date and time
    def _getTimeFunction(self) -> datetime:
        return datetime.now()

    # get the current date and time
    def _getUTCTimeFunction(self) -> datetime:
        return _getUTCTime()

    def setLastPanelEventData(self, count=0, type=[ ], event=[ ], zonemode=[ ], name=[ ]) -> dict:
        datadict = {}
        datadict["event_count"] = count
        if count > 0:
            datadict["event_time"] = self._getTimeFunction().isoformat()
        else:
            datadict["event_time"] = ""
        datadict["event_type"] = type
        datadict["event_event"] = event
        datadict["event_mode"] = zonemode
        datadict["event_name"] = name
        self.LastPanelEventData = datadict

        if count > 0:
            self.PanelLastEvent = zonemode[0] + "/" + name[0]

        log.debug(f"Last event {datadict}")
        return datadict

    def setLastEventData(self, reset : bool = False) -> dict:
        datadict = {}
        datadict["mode"] = titlecase(self.PanelMode.name.replace("_"," ").lower())
        datadict["state"] = "Triggered" if self.SirenActive else titlecase(self.PanelState.name.replace("_"," ").lower())
        datadict["ready"] = self.PanelReady
        datadict["tamper"] = self.PanelTamper
        datadict["memory"] = self.PanelAlertInMemory
        datadict["siren"] = self.SirenActive
        datadict["bypass"] = self.PanelBypass
        datadict["reset"] = reset
        datadict["alarm"] = titlecase(self.PanelAlarmStatus.name.replace("_"," "))
        datadict["trouble"] = titlecase(self.PanelTroubleStatus.name.replace("_"," "))
        datadict.update(self.LastPanelEventData)
        return datadict

    # Set the onDisconnect callback handlers
    def onDisconnect(self, fn : Callable):             # onDisconnect ( exception or string or None )
        self.onDisconnectHandler = fn

    # Set the onNewSensor callback handlers
    def onNewSensor(self, fn : Callable):             # onNewSensor ( device : AlSensorDevice )
        self.onNewSensorHandler = fn

    # Set the onNewSwitch callback handlers
    def onNewSwitch(self, fn : Callable):             # onNewSwitch ( sensor : AlSwitchDevice )
        self.onNewSwitchHandler = fn

    # Set the onPanelLog callback handlers
    def onPanelLog(self, fn : Callable):             # onPanelLog ( event_log_entry : AlLogPanelEvent )
        self.onPanelLogHandler = fn

    # Set the onPanelEvent callback handlers
    def onPanelChange(self, fn : Callable):             # onPanelChange ( datadictionary : dict )
        self.onPanelChangeHandler = fn

    def sendPanelUpdate(self, ev : AlCondition):
        if self.onPanelChangeHandler is not None:
            self.onPanelChangeHandler(ev)

    def _searchDict(self, dict, v_search):
        for k, v in dict.items():
            if v == v_search:
                return k
        return None

    # decodes json to set the variables and returns true if any of the booleans have changed state
    def fromJSON(self, decode) -> bool:
        # Not currently processed:     "zone": 0, "reset": false,
        oldSirenActive = self.SirenActive
        oldPanelState = self.PanelState
        oldPanelMode = self.PanelMode
        #oldPowerMaster = self.PowerMaster
        oldPanelReady = self.PanelReady
        oldPanelTrouble = self.PanelTroubleStatus
        oldPanelBypass = self.PanelBypass
        oldPanelAlarm = self.PanelAlarmStatus

        if "mode" in decode:
            d = decode["mode"].replace(" ","_").upper()
            log.debug("Mode="+str(d))
            self.PanelMode = AlPanelMode.value_of(d)
        if "status" in decode:
            d = decode["status"].replace(" ","_").upper()
            self.PanelState = AlPanelStatus.value_of(d)
        if "alarm" in decode:
            d = decode["alarm"].replace(" ","_").upper()
            self.PanelAlarmStatus = AlAlarmType.value_of(d)
        if "trouble" in decode:
            d = decode["trouble"].replace(" ","_").upper()
            self.PanelTroubleStatus = AlTroubleType.value_of(d)
        if "ready" in decode:
            self.PanelReady = toBool(decode["ready"])
        if "tamper" in decode:
            self.PanelTamper = toBool(decode["tamper"])
        if "memory" in decode:
            self.PanelAlertInMemory = toBool(decode["memory"])
        if "siren" in decode:
            self.SirenActive = toBool(decode["siren"])
        if "bypass" in decode:
            self.PanelBypass = toBool(decode["bypass"])
        #if "powermaster" in decode:
        #    self.PowerMaster = decode["powermaster"]

        if "event_count" in decode:
            c = decode["event_count"]
            if c > 0:
                t = decode["event_type"]
                e = decode["event_event"]
                m = decode["event_mode"]
                n = decode["event_name"]
                log.debug(f"Got Zone Event {c} {t} {e} {m} {n}")
                self.setLastPanelEventData(count=c, type=t, event=e, zonemode=m, name=n)

        return oldPanelState != self.PanelState or \
               oldPanelMode != self.PanelMode or \
               oldPanelReady != self.PanelReady or \
               oldPanelTrouble != self.PanelTroubleStatus or \
               oldPanelAlarm != self.PanelAlarmStatus or \
               oldPanelBypass != self.PanelBypass

    def merge(self, a : dict, b : dict, path=None, update=True):
        "http://stackoverflow.com/questions/7204805/python-dictionaries-of-dictionaries-merge"
        "merges b into a"
        if path is None: path = []
        #log.debug("[merge] type a={0} type b={1}".format(type(a), type(b)))
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self.merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass # same leaf value
                elif isinstance(a[key], list) and isinstance(b[key], list):
                    for idx, val in enumerate(b[key]):
                        a[key][idx] = self.merge(a[key][idx], b[key][idx], path + [str(key), str(idx)], update=update)
                elif update:
                    a[key] = b[key]
                else:
                    raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
            else:
                a[key] = b[key]
        return a

    def getPanelFixedDict(self) -> dict:
        pm = "Unknown"
        if self.PowerMaster is not None:
            if self.PowerMaster: # PowerMaster models
                pm = "Yes"
            else:
                pm = "No"
        return {
            "Panel Model": self.PanelModel,
            "Power Master": pm
            #"Model Type": self.ModelType
        }

    def shutdownOperation(self):
        if not self.suspendAllOperations:
            self.suspendAllOperations = True
            self.PanelMode = AlPanelMode.STOPPED
            self.PanelState = AlPanelStatus.UNKNOWN
            self.PanelStatus = {}
        self.PanelLastEventData = self.setLastEventData()

    def dumpSensorsToStringList(self) -> list:
        retval = list()
        for key, sensor in self.SensorList.items():
            retval.append("key {0:<2} Sensor {1}".format(key, sensor))
        return retval

    def dumpSwitchesToStringList(self) -> list:
        retval = list()
        for key, switch in self.SwitchList.items():
            retval.append("key {0:<2} Switch {1}".format(key, switch))
        return retval
