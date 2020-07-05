""" InfluxDB helper module
"""


class SeriesHelper():
    """ Helper to write points to the backend
    """
    def __init__(self, client, series: str, fields: list, tags=None):
        self.client = client
        self.series = series
        self.fields = fields
        self.tags = tags
        self.points = []

    def add_point(self, item):
        """ Add single series
        """
        fields = {f: to_num(item.get(f)) for f in self.fields}
        tags = {t: item.get(t) for t in self.tags} if self.tags else {}

        self.points.append({'measurement': self.series,
                            'fields': fields,
                            'tags': tags})

    def add_points(self, items):
        """ Add multiply serires
        """
        for item in items:
            self.add_point(item)


    def write_points(self, **options):
        """ Write series
        """
        self.client.write_points(self.points, **options)


def to_num(num):
    """ Convert string to float or integer
    """
    if isinstance(num, str):
        return float(num) if '.' in num else int(num)

    return num
