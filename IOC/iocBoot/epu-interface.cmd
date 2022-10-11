#!../bin/linux-arm/streamApp
# Environment variables
epicsEnvSet("EPICS_BASE", "/opt/epics-R3.15.7/base")
epicsEnvSet("ASYN", "/opt/epics-R3.15.7/modules/asyn4-35")
epicsEnvSet("TOP", "/opt/epics-R3.15.7/modules/StreamDevice_2_8_8")
epicsEnvSet("ARCH", "linux-arm")
epicsEnvSet("STREAM_PROTOCOL_PATH", "$(TOP)/protocol")
epicsEnvSet("EPICS_CA_SERVER_PORT", "5064")
epicsEnvSet("EPICS_IOC_LOG_INET", "10.128.255.4")
epicsEnvSet("EPICS_IOC_LOG_PORT", "7011")

# Database definition file
cd ${TOP}
dbLoadDatabase("dbd/streamApp.dbd")
streamApp_registerRecordDeviceDriver(pdbbase)

# Bind to socat
drvAsynIPPortConfigure("IPPort0","10.0.6.71:5050", 100, 0, 0)

# General UPS records
dbLoadRecords("database/ca_eaton_ups.db", "PORT=IPPort0, BSMP_ID=0, PV_NAME=, SCAN_RATE=.2 second")
dbLoadRecords("database/ca_eaton_ups.db", "PORT=IPPort0, BSMP_ID=1, PV_NAME=, SCAN_RATE=.2 second")

# Effectively initializes the IOC
cd iocBoot
iocInit
