""" InfluxDB helper module
"""


class SeriesHelper():
    """ Helper to write points to the backend
    """
    def __init__(self, client, measurement: str, tags=None):
        self.client = client
        self.measurement = measurement
        self.tags = tags or []
        self.points = []

    def add_point(self, item):
        """ Add single series
        """
        tags = {t: item.get(t) for t in self.tags} if self.tags else {}
        fields = {k: to_num(v) for k, v in item.items() if k not in self.tags}

        self.points.append({
            'measurement': self.measurement,
            'fields': fields,
            'tags': tags
        })

    def add_points(self, items):
        """ Add multiply series
        """
        for item in items:
            self.add_point(item)

    def write_points(self, **kwargs):
        """ Write series
        """
        self.client.write_points(self.points, **kwargs)


def to_num(num):
    """ Convert string to float or integer
    """
    if isinstance(num, str):
        return float(num) if '.' in num else int(num)

    return num
