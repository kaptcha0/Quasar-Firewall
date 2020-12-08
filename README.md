# Quasar Firewall
An AI powered firewall designed to detect mallicious HTTP requests and decide weather to process them or not.

```
pip install quasar-project-firewall
```

# Usage
## As Flask Middleware
*Note: Model must be trained before starting proxy server*
```python
from detector_flask import DetectorMiddleware
...
app.wsgi_app = DetectorMiddleware(app.wsgi_app)
...
```
## Starting Proxy From Command Line
*Note: Must have python installed on local machine and added to PATH*<br>
*Note: Model must be trained before starting proxy server*

### **With Bash**
Call `proxy.sh` with paramaters `target` and  `port`
- `target` is the proxy destination
  - defaults to `http://localhost:8080`
- `port` is the local port to run the server on
  - defaults to 5000

Example:
```bash
proxy.sh [target] [port]
```

### **As Python Module**
- `options`
  - `-s` or `--serve` to start the proxy server
  - `-t` or `--train` to train the model
    - Default
Example:
```bash
python -m quasar_firewall [options] [target] [port]
```

Redirect requests from original server to proxy server


## Training the Model
*Note: Must have python installed on local machine and added to PATH*

### **With Bash**
Call `train.sh`

Example:
```bash
train.sh
```

### **As Python Module**
Example:
```bash
python -m quasar_firewall -t
```

