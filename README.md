# AI Firewall
An AI powered firewall designed to detect mallicious HTTP requests and decide weather to process them or not.

## Usage
&nbsp;
### For Python
```
pip install quasar-firewall
```

```python
from detector_flask import DetectorMiddleware
...
app.wsgi_app = DetectorMiddleware(app.wsgi_app)
...
```

### For Other Languages
*Note: Must have python installed on local machine and added to PATH*

Call `proxy.sh` with paramaters `target` and  `port`
- `target` is the proxy destination
  - defaults to `http://localhost:8080`
- `port` is the local port to run the server on
  - defaults to 5000

Example:
```bash
proxy.sh [target] [port]
```

Redirect requests from original server to proxy server
