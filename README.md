> Note: Still under development, use at your own risk

# Quasar Firewall
An AI powered firewall designed to detect mallicious HTTP requests and decide weather to process them or not.

## Python CLI Reference
**Syntax:**
```bash
python -m quasar [-h] [-t | -s target port]
```

- `options`
  - `-s` or `--serve` to start the proxy server
  - `-t` or `--train` to train the model

These options are mutually exclusive

## Training the Models
*Note: Must have python3 installed on local machine and added to PATH*

### With Bash
Call `train.sh`

Example:
```bash
train.sh
```

### With Python Module
Example:
```bash
python3 -m quasar -t
```

## Using the Firewall
There are two main ways to use Quasar, as a proxy server and as a middleware for Flask.

### As Flask Middleware
*Note: Model must be trained before starting proxy server*
```python
from quasar import DetectorMiddleware
...
app.wsgi_app = DetectorMiddleware(app.wsgi_app)
...
```

### As Proxy Server
*Note: Must have python installed on local machine and added to PATH*<br>
*Note: Model must be trained before starting proxy server*

#### **With Bash**
Call `proxy.sh` with paramaters `target` and  `port`
- `target` is the proxy destination
  - defaults to `http://localhost:8080`
- `port` is the local port to run the server on
  - defaults to 5000

Example:
```bash
proxy.sh [target] [port]
```

## Known Limitations
- Most SQL keywords in the query string or body make the model think the request is an attack
- Hangs after verifying a POST request

## Future
- [ ] Rework the whole model from the beginning
- [ ] Use NEAT algorithm based on Tensorflow or other popular AI database
- [ ] Consider re-writing parts in Rust, Go, or other languages for performance reasons
- [ ] Make cross-platform executable with configuration options
