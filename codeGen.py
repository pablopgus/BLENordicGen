
class codeGen():
    def __init__(self, blemap):
        self.map = blemap

    def run(self):
        for service in self.map:
            self.generate_H(service)
            self.generate_C(service)

    def generate_C(self, service):
        pass

    def generate_H(self, service):
        filename = "ble_"+service.name+".h"
        f = open(filename, "w")
        f.write("#ifndef BLE_"+service.name.upper()+"_H__\n#define BLE_"+service.name.upper()+"_H__\n\n")

        f.write("#include <stdint.h>\n#include <stdbool.h>\n#include \"ble.h\"\n#include \"ble_srv_common.h\"\n#include \"nrf_sdh_ble.h\"\n#include \"nrf_ble_gatt.h\"\n\n")
        f.write("/* Characteristics UUID Definitions. */\n")
        for ch in service.charL:
            f.write("#define BLE_UUID_"+ch.name.upper()+"\t\t"+ch.uuid+"\n")
        f.write("\n")

        f.write("/* Enable "+service.name.upper()+" Module */\n")
        f.write("#define BLE_"+service.name.upper()+"_ENABLED 1\n")
        f.write("\n")

        f.write("#ifdef __cplusplus\nextern \"C\" {\n#endif\n")
        f.write("\n")

        f.write("/** @brief Macro for defining a ble_"+service.name+" instance. \n* @param _name Name of the instance.\n* @hideinitializer        */\n")
        f.write("#define BLE_"+service.name.upper()+"_DEF(_name) \tstatic ble_"+service.name+"_t _name; NRF_SDH_BLE_OBSERVER(_name  ## _obs,BLE_"+service.name.upper()+"_BLE_OBSERVER_PRIO,ble_"+service.name+"_on_ble_evt, &_name) \n")
        f.write("\n")

        f.write("/**@brief "+service.name.upper()+" Service event type. */\n")
        f.write("typedef enum\n{\n\tBLE_"+service.name.upper()+"_EVT_NOTIFICATION_ENABLED, /**< "+service.name.upper()+" value notification enabled event. */\n\tBLE_"+service.name.upper()+"_EVT_NOTIFICATION_DISABLED /**< "+service.name.upper()+" value notification disabled event. */\n} ble_"+service.name+"_evt_type_t;\n\n")
        f.write("/**@brief "+service.name.upper()+" Service event. */\n")
        f.write("typedef struct\n{\n\tble_"+service.name+"_evt_type_t evt_type;    /**< Type of event. */\n\tuint16_t           conn_handle; /**< Connection handle. */\n} ble_"+service.name+"_evt_t;\n")
        f.write("\n")

        f.write("// Forward declaration of the ble_"+service.name+"_t type.\n")
        f.write("typedef struct ble_"+service.name+"_s ble_"+service.name+"_t;\n")
        f.write("\n")

        f.write("/**@brief "+service.name.upper()+" Service event handler type. */\n")
        f.write("typedef void (* ble_"+service.name+"_evt_handler_t) (ble_"+service.name+"_t * p_"+service.name+", ble_"+service.name+"_evt_t * p_evt);\n")
        f.write("\n")

        # Service INIT.
        f.write("/**@brief "+service.name.upper()+" Service init structure. This contains all options and data needed for initialization of the service.*/\n")
        f.write("typedef struct\n{\n\tble_"+service.name+"_evt_handler_t  evt_handler;                    /**< Event handler to be called for handling events in the "+service.name.upper()+" Service. */\n")

        default_str = ""
        security_str = ""
        for ch in service.charL:
            default_str += "\t"+ch.type+ " \t default_"+ch.name+";\n"
            if('r' in ch.actions):
                security_str += "\tsecurity_req_t \t "+ch.name+"_rd_sec;\n"
            if('r' in ch.actions):
                security_str += "\tsecurity_req_t \t "+ch.name+"_cccd_wr_sec;\n"

        f.write(default_str)
        f.write(security_str)
        f.write("} ble_"+service.name+"_init_t;\n")
        f.write("\n")

        # Service Structure
        f.write("/**@brief "+service.name.upper()+" Service structure. This contains various status information for the service. */\n")
        f.write("struct ble_"+service.name+"_s\n{\n")
        f.write("\tble_"+service.name+"_evt_handler_t evt_handler;\n")
        f.write("\tuint16_t service_handle;\n")

        handles_str = ""
        var_str = ""
        for ch in service.charL:
            handles_str += "\tble_gatts_char_handles_t "+ch.name+"_handles;\n"
            var_str += "\t"+ch.type+" "+ch.name+";\n"
        f.write(handles_str)
        f.write("\tuint16_t conn_handle;\n")
        f.write(var_str)
        f.write("};\n")
        f.write("\n")

        # INIT
        f.write("/**@brief Function for initializing the "+service.name.upper()+" Service.\n *\n * @param[out]  p_"+service.name+"       "+service.name.upper()+" Service structure. This structure will have to be supplied by\n *                          the application. It will be initialized by this function, and will later\n *                          be used to identify this particular service instance.\n * @param[in]   p_"+service.name+"_init  Information needed to initialize the service.\n *\n * @return      NRF_SUCCESS on successful initialization of service, otherwise an error code.*/\n")
        f.write("ret_code_t ble_"+service.name+"_init(ble_"+service.name+"_t * p_"+service.name+", const ble_"+service.name+"_init_t * p_"+service.name+"_init);\n")
        f.write("\n")

        f.write("/**@brief Function for handling the Application's BLE Stack events.\n *\n * @details Handles all events from the BLE stack of interest to the "+service.name+" Service.\n *\n * @note For the requirements in the "+service.name+" specification to be fulfilled,\n *       ble_"+service.name+"_update() must be called upon reconnection if the "+service.name+" parameters\n *       have changed while the service has been disconnected from a bonded client.\n *\n * @param[in]   p_ble_evt   Event received from the BLE stack.\n * @param[in]   p_context   "+service.name+" Service structure.\n */\n")
        f.write("void ble_"+service.name+"_on_ble_evt(ble_evt_t const * p_ble_evt, void * p_context);\n")

        f.write("\n")
        f.write("#ifdef __cplusplus\n")
        f.write("}\n")
        f.write("#endif\n")

        f.write("\n")
        f.write("#endif\n")
        f.close()

