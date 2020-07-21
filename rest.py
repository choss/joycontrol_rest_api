import uvicorn
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field
from starlette.responses import RedirectResponse
from rest_controller_service import ControllerAxis
from rest_controller_service import ControllerButton
from rest_controller_service import ControllerStick

app = FastAPI()


class ConnectRequest(BaseModel):
    spi_firm: str = Field(None, title="Controller SPI Firm - base64 encoded", example="")
    reconnect: bool = Field(..., title="Reconnect to already paired switch", example=False)
    reconnect_address: str = Field(None, title="MAC Address of switch", example="E1:3F:54:0B:DE:BB")
    controller_type: str = Field("PRO_CONTROLLER", title="Type of controller to emulate [PRO_CONTROLLER, JOYCON_R, JOYCON_L]", example="PRO_CONTROLLER")


class NfcData(BaseModel):
    nfc_data: str = Field(None, title="NFC data - base64 encoded", example="")

@app.get("/")
async def redirect_to_documentation():
    return RedirectResponse(url='/docs')

@app.get("/controller/status")
async def controller_status():
    return dict()

@app.patch("/controller/button/press/{button_name}")
async def press_controller_button(button_name: ControllerButton):
    return button_name

@app.patch("/controller/button/release/{button_name}")
async def release_controller_button(button_name: ControllerButton):
    return button_name

@app.patch("/controller/stick/{stick}/{axis}/{value}")
async def set_stick_axis_state(stick: ControllerStick, axis: ControllerAxis, value: int = Path(..., ge=0, le=4095)):
    return {"stick": stick, "axis": axis, "value": value}

@app.patch("/controller/stick/{stick}/center")
async def center_stick(stick: ControllerStick):
    return {"stick": stick }

@app.post("/controller/connect")
async def connect_to_switch(cr: ConnectRequest):
    return cr

@app.post("/controller/nfc")
async def send_nfc_data(nf: NfcData):
    return { "result" : "OK"}

@app.delete("/controller/nfc")
async def remove_nfc_data():
    return { "result" : "OK"}

@app.on_event("startup")
async def startup():
    app.state.switch_controller = None

if __name__ == "__main__":
    uvicorn.run("rest:app", host="127.0.0.1", port=8000, log_level="info")
