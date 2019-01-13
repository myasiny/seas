import json
from decimal import Decimal as D

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, D):
            return float(obj)
        return json.JSONEncoder.default(self, obj)