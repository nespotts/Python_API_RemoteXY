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


@app.get("/set_bms_params/{bms}/{voltage}/{current}/{state_of_charge}/{state_of_charge1}/{discharge_status}/{charge_status}/{battery_temp}/{bms_temp}/{balance_capacity}/{rate_capacity}/{cell1_voltage}/{cell2_voltage}/{cell3_voltage}/{cell4_voltage}/{cell1_bal_en}/{cell2_bal_en}/{cell3_bal_en}/{cell4_bal_en}/{cycle_count}/{fault_count}/{max_cell_delta}")
def set_bms_params(bms, voltage, current, state_of_charge, state_of_charge1, discharge_status, charge_status, battery_temp, bms_temp, balance_capacity, rate_capacity, cell1_voltage, cell2_voltage, cell3_voltage, cell4_voltage, cell1_bal_en, cell2_bal_en, cell3_bal_en, cell4_bal_en, cycle_count, fault_count, max_cell_delta):
  parameters = locals()
  parameters.pop("bms")
  for key,value in parameters.items():
    key = f"bms{bms}_{key}"
    # print(key, value)
    variables[key] = value
  cache_variables(variables)
  return variables