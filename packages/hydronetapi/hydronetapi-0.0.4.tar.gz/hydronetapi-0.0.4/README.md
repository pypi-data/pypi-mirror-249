 ## Hydronet API

Import library:
```python
from hydronet import wmm
```

Establish connection to a modem:

```python
modem = wmm.wmm(<Modem ID>)
```
 
Send data:
```python
modem.send(<data>)
```

Send data to destination:
```python
modem.send(<data>,<destination>)
```

Receive data:
```python
data = modem.recv()
```