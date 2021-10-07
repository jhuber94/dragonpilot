# flake8: noqa

from collections import defaultdict
from typing import Dict

from cereal import car
from selfdrive.car import dbc_dict

Ecu = car.CarParams.Ecu
NetworkLocation = car.CarParams.NetworkLocation
TransmissionType = car.CarParams.TransmissionType
GearShifter = car.CarState.GearShifter

class CarControllerParams:
  HCA_STEP = 2                   # HCA_01 message frequency 50Hz
  LDW_STEP = 10                  # LDW_02 message frequency 10Hz
  GRA_ACC_STEP = 3               # GRA_ACC_01 message frequency 33Hz

  GRA_VBP_STEP = 100             # Send ACC virtual button presses once a second
  GRA_VBP_COUNT = 16             # Send VBP messages for ~0.5s (GRA_ACC_STEP * 16)

  # Observed documented MQB limits: 3.00 Nm max, rate of change 5.00 Nm/sec.
  # Limiting rate-of-change based on real-world testing and Comma's safety
  # requirements for minimum time to lane departure.
  STEER_MAX = 300                # Max heading control assist torque 3.00 Nm
  STEER_DELTA_UP = 4             # Max HCA reached in 1.50s (STEER_MAX / (50Hz * 1.50))
  STEER_DELTA_DOWN = 10          # Min HCA reached in 0.60s (STEER_MAX / (50Hz * 0.60))
  STEER_DRIVER_ALLOWANCE = 80
  STEER_DRIVER_MULTIPLIER = 3    # weight driver torque heavily
  STEER_DRIVER_FACTOR = 1        # from dbc

class CANBUS:
  pt = 0
  cam = 2

class DBC_FILES:
  mqb = "vw_mqb_2010"  # Used for all cars with MQB-style CAN messaging

DBC = defaultdict(lambda: dbc_dict(DBC_FILES.mqb, None))  # type: Dict[str, Dict[str, str]]

BUTTON_STATES = {
  "accelCruise": False,
  "decelCruise": False,
  "cancel": False,
  "setCruise": False,
  "resumeCruise": False,
  "gapAdjustCruise": False
}

MQB_LDW_MESSAGES = {
  "none": 0,                            # Nothing to display
  "laneAssistUnavailChime": 1,          # "Lane Assist currently not available." with chime
  "laneAssistUnavailNoSensorChime": 3,  # "Lane Assist not available. No sensor view." with chime
  "laneAssistTakeOverUrgent": 4,        # "Lane Assist: Please Take Over Steering" with urgent beep
  "emergencyAssistUrgent": 6,           # "Emergency Assist: Please Take Over Steering" with urgent beep
  "laneAssistTakeOverChime": 7,         # "Lane Assist: Please Take Over Steering" with chime
  "laneAssistTakeOverSilent": 8,        # "Lane Assist: Please Take Over Steering" silent
  "emergencyAssistChangingLanes": 9,    # "Emergency Assist: Changing lanes..." with urgent beep
  "laneAssistDeactivated": 10,          # "Lane Assist deactivated." silent with persistent icon afterward
}

# Check the 7th and 8th characters of the VIN before adding a new CAR. If the
# chassis code is already listed below, don't add a new CAR, just add to the
# FW_VERSIONS for that existing CAR.
# Exception: SEAT Leon and SEAT Ateca share a chassis code

class CAR:
  ATLAS_MK1 = "VOLKSWAGEN ATLAS 1ST GEN"      # Chassis CA, Mk1 VW Atlas and Atlas Cross Sport
  GOLF_MK7 = "VOLKSWAGEN GOLF 7TH GEN"        # Chassis 5G/AU/BA/BE, Mk7 VW Golf and variants
  JETTA_MK7 = "VOLKSWAGEN JETTA 7TH GEN"      # Chassis BU, Mk7 Jetta
  PASSAT_MK8 = "VOLKSWAGEN PASSAT 8TH GEN"    # Chassis 3G, Mk8 Passat and variants
  TCROSS_MK1 = "VOLKSWAGEN T-CROSS 1ST GEN"   # Chassis C1, Mk1 VW T-Cross SWB and LWB variants
  TIGUAN_MK2 = "VOLKSWAGEN TIGUAN 2ND GEN"    # Chassis AD/BW, Mk2 VW Tiguan and variants
  TOURAN_MK2 = "VOLKSWAGEN TOURAN 2ND GEN"    # Chassis 1T, Mk2 VW Touran and variants
  AUDI_A3_MK3 = "AUDI A3 3RD GEN"             # Chassis 8V/FF, Mk3 Audi A3 and variants
  AUDI_Q2_MK1 = "AUDI Q2 1ST GEN"             # Chassis GA, Mk1 Audi Q2 (RoW) and Q2L (China only)
  SEAT_ATECA_MK1 = "SEAT ATECA 1ST GEN"       # Chassis 5F, Mk1 SEAT Ateca and CUPRA Ateca
  SEAT_LEON_MK3 = "SEAT LEON 3RD GEN"         # Chassis 5F, Mk3 SEAT Leon and variants
  SKODA_KODIAQ_MK1 = "SKODA KODIAQ 1ST GEN"   # Chassis NS, Mk1 Skoda Kodiaq
  SKODA_SCALA_MK1 = "SKODA SCALA 1ST GEN"     # Chassis NW, Mk1 Skoda Scala and Skoda Kamiq
  SKODA_SUPERB_MK3 = "SKODA SUPERB 3RD GEN"   # Chassis 3V/NP, Mk3 Skoda Superb and variants
  SKODA_OCTAVIA_MK3 = "SKODA OCTAVIA 3RD GEN" # Chassis NE, Mk3 Skoda Octavia and variants

# All supported cars should return FW from the engine, srs, eps, and fwdRadar. Cars
# with a manual trans won't return transmission firmware, but all other cars will.
#
# The 0xF187 SW part number query should return in the form of N[NX][NX] NNN NNN [X[X]],
# where N=number, X=letter, and the trailing two letters are optional. Performance
# tuners sometimes tamper with that field (e.g. 8V0 9C0 BB0 1 from COBB/EQT). Tampered
# ECU SW part numbers are invalid for vehicle ID and compatibility checks. Try to have
# them repaired by the tuner before including them in openpilot.

FINGERPRINTS = {
  CAR.SKODA_OCTAVIA_MK3: [
    {178: 8, 1600: 8, 1601: 8, 1603: 8, 1605: 8, 695: 8, 1624: 8, 1626: 8, 1629: 8, 1631: 8, 1122: 8, 1123: 8,
     1124: 8, 1646: 8, 1648: 8, 1153: 8, 134: 8, 1162: 8, 1175: 8, 159: 8, 795: 8, 679: 8, 681: 8, 173: 8, 1712: 6,
     1714: 8, 1716: 8, 1717: 8, 1719: 8, 1720: 8, 1721: 8, 1312: 8, 806: 8, 253: 8, 1792: 8, 257: 8, 260: 8, 262: 8,
     897: 8, 264: 8, 779: 8, 780: 8, 783: 8, 278: 8, 279: 8, 792: 8, 283: 8, 285: 8, 286: 8, 901: 8, 288: 8, 289: 8,
     290: 8, 804: 8, 294: 8, 807: 8, 808: 8, 809: 8, 299: 8, 302: 8, 1351: 8, 346: 8, 870: 8, 1385: 8, 896: 8, 64: 8,
     898: 8, 1413: 8, 917: 8, 919: 8, 927: 8, 1440: 5, 929: 8, 930: 8, 427: 8, 949: 8, 958: 8, 960: 4, 418: 8, 981: 8,
     987: 8, 988: 8, 991: 8, 997: 8, 1000: 8, 1514: 8, 1515: 8, 1520: 8, 1019: 8, 385: 8, 668: 8, 1120: 8,
     1438: 8, 1461: 8, 391: 8, 1511: 8, 1516: 8, 568: 8, 569: 8, 826: 8, 827: 8, 1156: 8, 1157: 8, 1158: 8, 1471: 8,
     1635: 8, 376: 8, 295: 8, 791: 8, 799: 8, 838: 8, 389: 8, 840: 8, 841: 8, 842: 8, 843: 8, 844: 8, 845: 8,
     314: 8, 787: 8, 788: 8, 789: 8, 802: 8, 839: 8, 1332: 8, 1872: 8, 1976: 8, 1977: 8, 1985: 8, 2015: 8, 592: 8,
     593: 8, 594: 8, 595: 8, 596: 8, 684: 8
     }
  ],
  SKODA_SUPERB_MK3: [
    {64: 8, 134: 8, 159: 8, 173: 8, 178: 8, 253: 8, 257: 8, 260: 8, 262: 8, 278: 8, 279: 8, 283: 8, 286: 8, 288: 8, 289: 8, 290: 8, 294: 8, 299: 8, 302: 8, 346: 8, 376: 8, 385: 8, 391: 8, 418: 8, 427: 8, 605: 8, 619: 8, 668: 8, 679: 8, 681: 8, 695: 8, 779: 8, 780: 8, 783: 8, 787: 8, 788: 8, 789: 8, 791: 8, 792: 8, 795: 8, 799: 8, 804: 8, 806: 8, 807: 8, 808: 8, 809: 8, 828: 8, 838: 8, 839: 8, 840: 8, 841: 8, 842: 8, 843: 8, 846: 8, 847: 8, 870: 8, 873: 8, 879: 8, 884: 8, 888: 8, 891: 8, 896: 8, 897: 8, 898: 8, 901: 8, 913: 8, 917: 8, 919: 8, 927: 8, 949: 8, 958: 8, 960: 4, 981: 8, 987: 8, 988: 8, 991: 8, 997: 8, 1000: 8, 1019: 8, 1120: 8, 1122: 8, 1123: 8, 1124: 8, 1153: 8, 1156: 8, 1157: 8, 1158: 8, 1162: 8, 1175: 8, 1312: 8, 1343: 8, 1385: 8, 1413: 8, 1440: 5, 1471: 4, 1514: 8, 1515: 8, 1520: 8, 1600: 8, 1601: 8, 1603: 8, 1624: 8, 1626: 8, 1629: 8, 1631: 8, 1635: 8, 1646: 8, 1648: 8, 1712: 6, 1714: 8, 1716: 8, 1717: 8, 1719: 8, 1720: 8, 1721: 8
     },
  ],
}
