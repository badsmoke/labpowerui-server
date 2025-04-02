⚠️ Warning: This project is still in early development. Some features may be incomplete, and breaking changes may occur. Contributions and feedback are welcome!



# LabPowerUI - Server

LabPowerUI-Server is a RESTful API for controlling and monitoring lab power supplies such as the **Owon SPE6103** and **SPE3103**, as well as **Kiprim DC310S** and **DC605S** models. It provides endpoints for adjusting voltage, current, and power limits, retrieving real-time data, and managing storage settings.

## Features
- Control and monitor supported lab power supplies
- Store power supply data in Redis
- Adjustable data storage interval and limits
- Support for fake values for testing purposes
- Logging system for debugging
- OpenAPI (Swagger) documentation

## Installation & Usage

### Docker Compose Setup
To deploy the **LabPowerUI-Server** along with **Redis** and the **LabPowerUI** frontend, use the following `docker-compose.yml` setup:

```yaml
version: "3"
services:
  power-supply-server:
    image: badsmoke/labpowerui-server
    ports:
      - "1234:1234"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_DB=0
      - USB_DEVICE=/dev/ttyUSB0
      - STORAGE_TASK=true
      - STORAGE_INTERVAL=1
      - STORAGE_LIMIT=10000
      - FAKE_VALUES=false
      - LOGGING=false
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0
    restart: always

  redis:
    image: redis:7-alpine
    restart: always
    ports:
      - "6379:6379"

  power-supply-ui:
    image: badsmoke/labpowerui
    ports:
      - "80:80"
```

### Running Without Docker
If you prefer running the server locally without Docker, follow these steps:

```sh
git clone https://github.com/badsmoke/LabPowerUI-Server.git
cd LabPowerUI-Server
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python src/main.py
```

## API Documentation
The API follows OpenAPI standards and provides a Swagger UI at:
```
http://localhost:1234/api/docs
```

### Example Endpoints

#### Get Power Supply Values
```http
GET /api/storage/data?limit=1
```
Response:
```json
{
  "status": "success",
  "code": 200,
  "message": "Power supply data retrieved successfully",
  "time": "47:57:238633",
  "device": "fake psu",
  "data": {
    "readingVoltage": 1.7,
    "readingCurrent": 0.7,
    "voltage": 19,
    "current": 5,
    "voltageLimit": 30,
    "currentLimit": 8,
    "power": 1.19,
    "output_status": true
  }
}
```

#### Set Output State
```http
POST /api/set/output
Content-Type: application/json

{
  "output": true
}
```

#### Enable Logging
```http
POST /api/logging
Content-Type: application/json

{
  "logging": true
}
```

Full API documentation is available in the `swagger.yaml` file.

## Configuration
The following environment variables can be set:

| Variable           | Description                           | Default Value |
|-------------------|-----------------------------------|--------------|
| REDIS_HOST       | Redis server hostname             | redis        |
| REDIS_PORT       | Redis port                        | 6379         |
| REDIS_DB         | Redis database index              | 0            |
| USB_DEVICE       | USB device path for PSU           | /dev/ttyUSB0 |
| STORAGE_TASK     | Enable data storage (true/false)  | true         |
| STORAGE_INTERVAL | Interval for storing data (sec)   | 1            |
| STORAGE_LIMIT    | Max number of stored entries      | 10000        |
| FAKE_VALUES      | Use fake PSU values (true/false)  | false        |
| LOGGING          | Enable logging (true/false)       | true         |

## Dependencies
LabPowerUI-Server is built with:
- **[owon-psu-control](https://github.com/robbederks/owon-psu-control)** – Python library for communicating with supported power supplies
- **Flask** – API framework
- **Redis** – Storage for logging and historical data

## Frontend
The **LabPowerUI-Server** is designed to work with the **[LabPowerUI](https://github.com/badsmoke/LabPowerUI)** web frontend. It provides an easy-to-use interface for monitoring and controlling your power supply unit.

#### UI

![alt text](/pictures/desktop.png)

![alt text](/pictures/mobile.png)



## additional

* [pi zero 2 case](https://www.printables.com/model/1240294-raspberry-pi-zero-w-2-minimalist-magnet-case/files)

* [cable for pi zero](https://www.amazon.de/dp/B06XXL8T45?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)

![alt text](/pictures/psu.png)




## License
This project is licensed under the MIT License.

## Contributors
- @badsmoke

## Contact
For issues or contributions, open an issue in the repository or reach out via email.

github@badcloud.eu

