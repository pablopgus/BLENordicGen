# Bluetooth Low Energy Nordic Service Generator
This script will generate .h .c pairs for basic BLE Services allowing read, write and subscribe to characteristics.
Supports SDK v16.
This code was tested on a nRF52840 Board (PCA10040). 

## Input File: Example provided <Mixcell.xml>
```xml
<BLE>
    <SERVICE name="power" uuid="0xAF00">
        <CHAR name="status"  uuid="0xC000" type="bool" initial="false" actions="r"></CHAR>
        <CHAR name="control"  uuid="0xC001" type="uint8_t" initial="0x00" actions="rw"></CHAR>
        <CHAR name="battery_level"  uuid="0xC002" type="float" initial="0.0" actions="rw"></CHAR>
    </SERVICE>
    <SERVICE name="obt" uuid="0xAF01">
        <CHAR name="central_frequency"  uuid="0xC100" type="float" initial="1000.0" actions="rw"></CHAR>
        <CHAR name="q_factor"           uuid="0xC101" type="float" initial="10.0"   actions="rw"></CHAR>
        <CHAR name="noise_filter_q"     uuid="0xC102" type="float" initial="10.0"   actions="rw"></CHAR>
        <CHAR name="hysteresis"         uuid="0xC103" type="float" initial="10.0"   actions="rw"></CHAR>
    </SERVICE>
</BLE>
```
This input will generate .h/.c files containing two services (power & obt) which then have several characteristics. 
Actions field currently accounts for "read" and "write" permissions only. Notifications are under development. 

![NordicConnect](https://github.com/pablopgus/BLENordicGen/blob/master/img/NordicConnect.png?raw=true "Nordic Connect")

The code generated has //TODO marks to complete specific entry points such as update values and on write events.  

![OnWrite](https://github.com/pablopgus/BLENordicGen/blob/master/img/OnWrite.png?raw=true "Nordic Connect")

