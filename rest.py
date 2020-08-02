import uvicorn
import asyncio
import base64
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field
from starlette.responses import RedirectResponse
from rest_controller_service import ControllerAxis, SwitchControllerService
from rest_controller_service import ControllerButton
from rest_controller_service import ControllerStick

app = FastAPI()


class ConnectRequest(BaseModel):
    controller_type: str = Field("PRO_CONTROLLER", title="Type of controller to emulate [PRO_CONTROLLER, JOYCON_R, JOYCON_L]", example="PRO_CONTROLLER")
    spi_firm: str = Field(None, title="Controller SPI Firm - base64 encoded", example="")
    reconnect_address: str = Field(None, title="MAC Address of switch - if empty a new pairing attempt will be done", example="E1:3F:54:0B:DE:BB")

    class Config:
        schema_extra = {
            "example":
                {
                        "controller_type": "PRO_CONTROLLER",
                        "reconnect_address": "E1:3F:54:0B:DE:BB"
                }
        }


class NfcData(BaseModel):
    nfc_data: str = Field(None, title="NFC data - base64 encoded", example="")

@app.get("/")
async def redirect_to_documentation():
    return RedirectResponse(url='/docs')

@app.post("/controller/connect")
async def connect_to_switch(cr: ConnectRequest):
    if cr.spi_firm is not None:
        spi_firm_bytes = base64.b64decode(cr.spi_firm)
    else:
        spi_firm_bytes = None

    await app.state.switch_controller.connect(cr.controller_type, cr.reconnect_address, spi_firm_bytes)
    return await controller_status()

@app.get("/controller/disconnect")
async def disconnect_from_switch():
    await app.state.switch_controller.disconnect()
    return await controller_status()

@app.get("/controller/status")
async def controller_status():
    return await app.state.switch_controller.get_status()

@app.patch("/controller/button/tap/{button_name}")
async def press_controller_button_for_300_ms(button_name: ControllerButton):
    await app.state.switch_controller.press_controller_button(button_name)
    # async waiting is a finicky, so we only wait 250ms
    await asyncio.sleep(0.25)
    await app.state.switch_controller.release_controller_button(button_name)
    return await controller_status()

@app.patch("/controller/button/press/{button_name}")
async def press_controller_button(button_name: ControllerButton):
    await app.state.switch_controller.press_controller_button(button_name)
    return await controller_status()

@app.patch("/controller/button/release/{button_name}")
async def release_controller_button(button_name: ControllerButton):
    await app.state.switch_controller.release_controller_button(button_name)
    return await controller_status()

@app.patch("/controller/stick/{stick}/{axis}/{value}")
async def set_stick_axis_state(stick: ControllerStick, axis: ControllerAxis, value: int = Path(..., ge=0, le=4095)):
    await app.state.switch_controller.set_stick_axis(stick, axis, value)
    return await controller_status()

@app.patch("/controller/stick/{stick}/center")
async def center_stick(stick: ControllerStick):
    await app.state.switch_controller.center_stick(stick)
    return await controller_status()

@app.post("/controller/nfc")
async def send_nfc_data(nfc: NfcData):
    nfc_data = base64.b64decode(nfc.nfc_data)
    await app.state.switch_controller.set_nfc_data(nfc_data)
    return await controller_status()

@app.delete("/controller/nfc")
async def remove_nfc_data():
    await app.state.switch_controller.set_nfc_data(None)
    return await controller_status()

@app.on_event("startup")
async def startup():
    app.state.switch_controller = SwitchControllerService()

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run("rest:app", host="0.0.0.0", port=8000, log_level="info", log_config=log_config)
