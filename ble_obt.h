#ifndef BLE_OBT_H__
#define BLE_OBT_H__

#include <stdint.h>
#include <stdbool.h>
#include "ble.h"
#include "ble_srv_common.h"
#include "nrf_sdh_ble.h"
#include "nrf_ble_gatt.h"

/* Characteristics UUID Definitions. */
#define BLE_UUID_CENTRAL_FREQUENCY		0xC000
#define BLE_UUID_Q_FACTOR		0xC001

/* Enable OBT Module */
#define BLE_OBT_ENABLED 1

#ifdef __cplusplus
extern "C" {
#endif

/** @brief Macro for defining a ble_obt instance. 
* @param _name Name of the instance.
* @hideinitializer        */
#define BLE_OBT_DEF(_name) 	static ble_obt_t _name; NRF_SDH_BLE_OBSERVER(_name  ## _obs,BLE_OBT_BLE_OBSERVER_PRIO,ble_obt_on_ble_evt, &_name) 

/**@brief OBT Service event type. */
typedef enum
{
	BLE_OBT_EVT_NOTIFICATION_ENABLED, /**< OBT value notification enabled event. */
	BLE_OBT_EVT_NOTIFICATION_DISABLED /**< OBT value notification disabled event. */
} ble_obt_evt_type_t;

/**@brief OBT Service event. */
typedef struct
{
	ble_obt_evt_type_t evt_type;    /**< Type of event. */
	uint16_t           conn_handle; /**< Connection handle. */
} ble_obt_evt_t;

// Forward declaration of the ble_obt_t type.
typedef struct ble_obt_s ble_obt_t;

/**@brief OBT Service event handler type. */
typedef void (* ble_obt_evt_handler_t) (ble_obt_t * p_obt, ble_obt_evt_t * p_evt);

/**@brief OBT Service init structure. This contains all options and data needed for initialization of the service.*/
typedef struct
{
	ble_obt_evt_handler_t  evt_handler;                    /**< Event handler to be called for handling events in the OBT Service. */
	float 	 default_central_frequency;
	float 	 default_q_factor;
	security_req_t 	 central_frequency_rd_sec;
	security_req_t 	 central_frequency_cccd_wr_sec;
	security_req_t 	 q_factor_rd_sec;
	security_req_t 	 q_factor_cccd_wr_sec;
} ble_obt_init_t;

/**@brief OBT Service structure. This contains various status information for the service. */
struct ble_obt_s
{
	ble_obt_evt_handler_t evt_handler;
	uint16_t service_handle;
	ble_gatts_char_handles_t central_frequency_handles;
	ble_gatts_char_handles_t q_factor_handles;
	uint16_t conn_handle;
	float central_frequency;
	float q_factor;
};

/**@brief Function for initializing the OBT Service.
 *
 * @param[out]  p_obt       OBT Service structure. This structure will have to be supplied by
 *                          the application. It will be initialized by this function, and will later
 *                          be used to identify this particular service instance.
 * @param[in]   p_obt_init  Information needed to initialize the service.
 *
 * @return      NRF_SUCCESS on successful initialization of service, otherwise an error code.*/
ret_code_t ble_obt_init(ble_obt_t * p_obt, const ble_obt_init_t * p_obt_init);

/**@brief Function for handling the Application's BLE Stack events.
 *
 * @details Handles all events from the BLE stack of interest to the obt Service.
 *
 * @note For the requirements in the obt specification to be fulfilled,
 *       ble_obt_update() must be called upon reconnection if the obt parameters
 *       have changed while the service has been disconnected from a bonded client.
 *
 * @param[in]   p_ble_evt   Event received from the BLE stack.
 * @param[in]   p_context   obt Service structure.
 */
void ble_obt_on_ble_evt(ble_evt_t const * p_ble_evt, void * p_context);

#ifdef __cplusplus
}
#endif

#endif
