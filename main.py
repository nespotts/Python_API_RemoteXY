from fastapi import FastAPI
import json
app = FastAPI()


variables = {
  "connect_flag": 0,
}

def cache_variables(variables):
  with open("variables.txt", "w") as f:
    for key, value in variables.items():
      f.write(f"{key}={value}\n")
      
def load_variables(variables):
  with open("variables.txt", "r") as f:
    for line in f:
      key, value = line.strip().split("=")
      try:
        value = float(value)
      except ValueError as e:
        print(e)
      variables[key] = value
      
load_variables(variables)

@app.get("/")
def root():
  return {"message": "Hello World"}


@app.get("/get_value/{key}")
def get_value(key: str):
  if key not in variables:
    return {"error": "Key not found"}
  return variables[key]


@app.get("/set_value/{key}/{value}")
def set_value(key: str, value):
  if key not in variables:
    return {"error": "Key not found"}
  variables[key] = value
  cache_variables(variables)
  return variables[key]


@app.get("/get_all")
def get_all():
  return variables


@app.get("/set_value")
def set_value2(key: str, value):
  if key not in variables:
    return {"error": "Key not found"}
  variables[key] = value
  cache_variables(variables)
  return variables[key]


@app.get("/set_bms_params/{bms_id}/{voltage}/{current}/{state_of_charge}/{state_of_charge_1}/{discharge_status}/{charge_status}/{battery_temperature}/{bms_temperature}/{balance_capacity}/{rate_capacity}/{cell1_voltage}/{cell2_voltage}/{cell3_voltage}/{cell4_voltage}/{cell1_balance_enabled}/{cell2_balance_enabled}/{cell3_balance_enabled}/{cell4_balance_enabled}/{cycle_count}/{fault_count}/{max_cell_delta}")
def set_bms_parameters(bms_id, voltage, current, state_of_charge, state_of_charge_1, discharge_status, charge_status, battery_temperature, bms_temperature, balance_capacity, rate_capacity, cell1_voltage, cell2_voltage, cell3_voltage, cell4_voltage, cell1_balance_enabled, cell2_balance_enabled, cell3_balance_enabled, cell4_balance_enabled, cycle_count, fault_count, max_cell_delta):
  parameters = {
      f"bms{bms_id}_{key}": value for key, value in locals().items() if key != "bms_id"
  }
  variables.update(parameters)
  cache_variables(variables)
  return variables

@app.get("/set_battery_params/{voltage}/{current}/{power}/{state_of_charge}/{state_of_charge_percent}")
def set_battery_params(voltage, current, power, state_of_charge, state_of_charge_percent):
  variables["battery_voltage"] = voltage
  variables["battery_current"] = current
  variables["battery_power"] = power
  variables["battery_state_of_charge"] = state_of_charge
  variables["battery_state_of_charge_percent"] = state_of_charge_percent
  cache_variables(variables)
  return variables


@app.get("/set_solar_params/{solar_id}/{voltage}/{current}/{power}/{battery_voltage}/{battery_current}/{state_of_charge}/{controller_temp}")
def set_solar_params(solar_id, voltage, current, power, battery_voltage, battery_current, state_of_charge, controller_temp):
  variables[f"solar{solar_id}_voltage"] = voltage
  variables[f"solar{solar_id}_current"] = current
  variables[f"solar{solar_id}_power"] = power
  variables[f"solar{solar_id}_battery_voltage"] = battery_voltage
  variables[f"solar{solar_id}_battery_current"] = battery_current
  variables[f"solar{solar_id}_state_of_charge"] = state_of_charge
  variables[f"solar{solar_id}_controller_temp"] = controller_temp
  cache_variables(variables)
  return variables


@app.get("/set_temps/{inside_temperature}/{outside_temperature}/{electrical_cabinet_temperature}")
def set_temps(inside_temperature, outside_temperature, electrical_cabinet_temperature):
  variables["inside_temperature"] = inside_temperature
  variables["outside_temperature"] = outside_temperature
  variables["electrical_cabinet_temperature"] = electrical_cabinet_temperature
  cache_variables(variables)
  return variables

  
