# currency_conv.py
Minimal currency converter using ECB data (updated regularly):

```python
from currency_conv import convert
assert convert(1, 'USD', 'NOK') < 10
assert convert(10, 'DKK', 'EUR') < 2
```

40 LoC for your pleasure, just copy-paste it into your project and BAM!