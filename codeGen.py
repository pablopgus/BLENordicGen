import string


class codeGen():
    def __init__(self, blemap):
        self.map = blemap

    def run(self):
        for service in self.map:
            self.generate_H(service)
            self.generate_C(service)
        self.generate_Services_init_function()

    def generate_Services_init_function(self):
        filename = "ble_service_init_function.c"
        f = open(filename, "w")

        for service in self.map:
            f.write("#include \"ble_"+service.name+".h\"\n")
        f.write("\n")

        f.write("NRF_BLE_QWR_DEF(m_qwr);\n")
        for service in self.map:
            f.write("BLE_"+service.name.upper()+"_DEF(m_"+service.name+");\n")
        f.write("\n")

        f.write("static ble_uuid_t m_adv_uuids[] = /** < Universally unique service identifiers. */\n{\n")
        f.write("\t{BLE_UUID_DEVICE_INFORMATION_SERVICE, BLE_UUID_TYPE_BLE},\n")

        for service in self.map:
            f.write("\t{"+service.uuid+", BLE_UUID_TYPE_BLE},\n")

        f.write("};\n")
        f.write("\n")


        f.write("/**@brief Function for initializing services that will be used by the application.\n *\n * @details Initialize the Heart Rate, Battery and Device Information services.\n */\n")
        f.write("void services_init(void)\n{\n")

        f.write("\tret_code_t         err_code;\n\tnrf_ble_qwr_init_t qwr_init = {0};\n")
        f.write("\tble_dis_init_t     dis_init;\n")
        for service in self.map:
            f.write("\tble_"+service.name+"_init_t     "+service.name+"_init;\n")
        f.write("\n")

        f.write("\t// Initialize Queued Write Module.\n\tqwr_init.error_handler = nrf_qwr_error_handler;\n\terr_code = nrf_ble_qwr_init( & m_qwr, & qwr_init);\n\tAPP_ERROR_CHECK(err_code);\n")
        f.write("\n")

        f.write("\t// Initialize Device Information Service.\n\tmemset(&dis_init, 0, sizeof(dis_init));\n\tble_srv_ascii_to_utf8(&dis_init.manufact_name_str, (char *)MANUFACTURER_NAME);\n\tdis_init.dis_char_rd_sec = SEC_OPEN;\n\terr_code = ble_dis_init(&dis_init);\n\tAPP_ERROR_CHECK(err_code);\n")
        f.write("\n")


        for service in self.map:
            f.write("\tmemset( & "+service.name+"_init, 0, sizeof("+service.name+"_init));\n\t"+service.name+"_init.evt_handler = NULL;\n")
            for ch in service.charL:
                f.write("\t//TODO Set default variable values.\n")
                f.write("\t//"+service.name+"_init.default_"+ch.name+" = "+ch.default+";\n")
                if('r' in ch.actions):
                    f.write("\t" + service.name + "_init."+ch.name+"_rd_sec = SEC_OPEN;\n")
                if('w' in ch.actions):
                    f.write("\t" + service.name + "_init."+ch.name+"_cccd_wr_sec = SEC_OPEN;\n")

            f.write("\terr_code = ble_"+service.name+"_init( & m_"+service.name+", & "+service.name+"_init);\n\tAPP_ERROR_CHECK(err_code);\n")
            f.write("\n")
        f.write("}\n")

    def replaceTokens(self, strF, service, char):
        t_ = strF.replace("<SERVICE.NAME>", service.name.upper())
        t_ = t_.replace("<service.name>", service.name)
        t_ = t_.replace("<CHAR.NAME>", char.name.upper())
        t_ = t_.replace("<char.name>", char.name)
        t_ = t_.replace("<char.type>", char.type)
        return t_

    def generate_C(self, service):
        filename = "ble_"+service.name+".c"
        f = open(filename, "w")
        f.write("#include \"ble_"+service.name.upper()+".h\"\n#include \"sdk_common.h\"\n#if NRF_MODULE_ENABLED(BLE_"+service.name.upper()+")\n#include \"ble_"+service.name+".h\"\n#include <string.h>\n#include \"ble_srv_common.h\"\n#include \"ble_conn_state.h\"\n")
        f.write("\n")

        f.write("#define NRF_LOG_MODULE_NAME ble_"+service.name+"\n")
        f.write("#if BLE_"+service.name.upper()+"_CONFIG_LOG_ENABLED\n#define NRF_LOG_LEVEL       BLE_"+service.name.upper()+"_CONFIG_LOG_LEVEL\n#define NRF_LOG_INFO_COLOR  BLE_"+service.name.upper()+"_CONFIG_INFO_COLOR\n#define NRF_LOG_DEBUG_COLOR BLE_"+service.name.upper()+"_CONFIG_DEBUG_COLOR\n#else // BLE_"+service.name.upper()+"_CONFIG_LOG_ENABLED\n#define NRF_LOG_LEVEL       0\n#endif // BLE_"+service.name.upper()+"_CONFIG_LOG_ENABLED\n")
        f.write("\n")
        f.write("#include \"nrf_log.h\"\nNRF_LOG_MODULE_REGISTER();\n")
        f.write("\n")

        ### Custom Code.
        f.write("/** ==================== TODO CODE ==================== */\n\n")

        tf = open("templates/on_connect", "r")
        on_connect_str = tf.read()
        for ch in service.charL:
            t_ = self.replaceTokens(on_connect_str, service, ch)
        f.write(t_)
        f.write("\n")

        tf = open("templates/on_write1", "r")
        on_write_str = tf.read()
        for ch in service.charL:
            t_ = self.replaceTokens(on_write_str, service, ch)
        f.write(t_)

        # Iterate over the chars to add the catch points.
        i = 0
        for ch in service.charL:
            if (i == 0):
                f.write("\tif(p_evt_write->handle == p_"+service.name+"->"+ch.name+"_handles.value_handle)\n\t{\n\t\t//TODO: "+ch.name+"\n\t}\n")
            else:
                f.write("\telse if(p_evt_write->handle == p_"+service.name+"->"+ch.name+"_handles.value_handle)\n\t{\n\t\t//TODO: "+ch.name+"\n\t}\n")
            i = i + 1

        f.write("}\n")

        f.write("\n")

        tf = open("templates/update", "r")
        update_str = tf.read()
        for ch in service.charL:
            t_ = self.replaceTokens(update_str, service, ch)
            f.write(t_)

        f.write("\n")

        ### Static Code.

        f.write("/** ==================== STATIC CODE ==================== */\n\n")

        tf = open("templates/ble_event", "r")
        event_str = tf.read()
        for ch in service.charL:
            t_ = self.replaceTokens(event_str, service, ch)
        f.write(t_)
        f.write("\n")

        f.write("\n")

        # Char inits.
        tf = open("templates/char_add.1", "r")
        add_char1_str = tf.read()
        tf = open("templates/char_add.2", "r")
        add_char2_str = tf.read()

        for ch in service.charL:
            t_ = self.replaceTokens(add_char1_str, service, ch)
            f.write(t_)

            if('r' in ch.actions):
                f.write("\tadd_char_params.read_access = p_"+service.name+"_init->"+ch.name+"_rd_sec;\n")
            if('w' in ch.actions):
                f.write("\tadd_char_params.cccd_write_access = p_"+service.name+"_init->"+ch.name+"_cccd_wr_sec;\n")

            t_ = self.replaceTokens(add_char2_str, service, ch)
            f.write(t_)
        f.write("\n")

        # Service init.
        f.write("ret_code_t ble_"+service.name+"_init(ble_"+service.name+"_t * p_"+service.name+", const ble_"+service.name+"_init_t * p_"+service.name+"_init)\n{\n")
        f.write("\tif (p_"+service.name+" == NULL || p_"+service.name+"_init == NULL)\n\t{\n\t\treturn NRF_ERROR_NULL;\n\t}\n")
        f.write("\tret_code_t err_code;\n\tble_uuid_t ble_uuid;\n\n")
        f.write("\t// Initialize service structure\n\tp_"+service.name+"->evt_handler               = p_"+service.name+"_init->evt_handler;\n")

        for ch in service.charL:
            f.write("\tp_"+service.name+"->"+ch.name+"         = "+ch.default+";\n")

        f.write("\n")

        f.write("\t// Add service\n\tBLE_UUID_BLE_ASSIGN(ble_uuid, "+service.uuid+");\n\n\terr_code = sd_ble_gatts_service_add(BLE_GATTS_SRVC_TYPE_PRIMARY, & ble_uuid, & p_"+service.name+"->service_handle);\n")
        f.write("\tVERIFY_SUCCESS(err_code);\n")
        f.write("\n")

        for ch in service.charL:
            f.write("\terr_code = "+ch.name+"_char_add(p_"+service.name+", p_"+service.name+"_init);\n")

        f.write("\treturn err_code;\n")

        f.write("}\n")
        f.write("\n")
        f.write("#endif // NRF_MODULE_ENABLED(BLE_"+service.name.upper()+")")

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
        f.write("#define BLE_"+service.name.upper()+"_ENABLED 1\n#define BLE_"+service.name.upper()+"_BLE_OBSERVER_PRIO 2\n")
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
            if('w' in ch.actions):
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

