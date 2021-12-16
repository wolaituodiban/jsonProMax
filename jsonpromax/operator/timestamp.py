import sys
from datetime import datetime
from .operator import Operator


class Timestamp(Operator):
    def __init__(self, name, _format, units, second=False, inplace=False):
        print('Timestamp is depreciated', file=sys.stderr)
        super().__init__(inplace=inplace)
        self.name = name
        self.format = _format
        self.units = {
            unit: '{}_{}'.format(self.name, unit) for unit in units
        }
        self.second = second

    def _call_inplace(self, obj, now: datetime = None, **kwargs):
        if self.name in obj:
            date_string = obj[self.name]
            time = datetime.strptime(date_string, self.format)
            if now is not None:
                diff = now - time
                if self.second:
                    obj['diff_second'] = diff.total_seconds()
                else:
                    obj['diff_day'] = diff.days + int(diff.seconds > 0)
            for unit, feat_name in self.units.items():
                if unit == 'weekday':
                    obj[feat_name] = time.weekday()
                elif hasattr(time, unit):
                    obj[feat_name] = getattr(time, unit)
        return obj

    def _call(self, obj, now: datetime = None, **kwargs):
        output = {}
        for k, v in obj.items():
            output[k] = v
            if k == self.name:
                date_string = obj[self.name]
                time = datetime.strptime(date_string, self.format)
                if now is not None:
                    diff = now - time
                    if self.second:
                        output['diff_second'] = diff.total_seconds()
                    else:
                        output['diff_day'] = diff.days + int(diff.seconds > 0)
                for unit, feat_name in self.units.items():
                    if unit == 'weekday':
                        output[feat_name] = time.weekday()
                    elif hasattr(time, unit):
                        output[feat_name] = getattr(time, unit)
        return output

    def extra_repr(self):
        return "name='{}', units={}, diff_units='{}'".format(
            self.name, list(self.units), 'second' if self.second else 'day')


class Timestamp2(Operator):
    def __init__(self, _format, units, second=True, inplace=False):
        super().__init__(inplace=inplace)
        self.format = _format
        self.units = units
        self.second = second

    def __call__(self, obj, now: datetime = None, **kwargs):
        output = {}
        time = datetime.strptime(obj, self.format)
        if now is not None:
            diff = now - time
            if self.second:
                output['diff_second'] = diff.total_seconds()
            else:
                output['diff_day'] = diff.days + int(diff.seconds > 0)
        for unit in self.units:
            if unit == 'weekday':
                output[unit] = time.weekday()
            elif hasattr(time, unit):
                output[unit] = getattr(time, unit)
        return output

    def extra_repr(self):
        return "units='{}', second={}".format(list(self.units), self.second)


class Timestamp3(Operator):
    def __init__(self, name, _format, units, second=True, inplace=False):
        super().__init__(inplace=inplace)
        self.name = name
        self.format = _format
        self.units = list(units)
        self.second = second

    def _call_inplace(self, obj, now: datetime = None, **kwargs):
        if self.name in obj:
            date_string = obj[self.name]
            time = datetime.strptime(date_string, self.format)

            if now is not None:
                diff = now - time
                if self.second:
                    obj['diff_second'] = diff.total_seconds()
                else:
                    obj['diff_day'] = diff.days + int(diff.seconds > 0)
            for unit in self.units:
                if unit == 'weekday':
                    obj[unit] = time.weekday()
                elif hasattr(time, unit):
                    obj[unit] = getattr(time, unit)
        return obj

    def _call(self, obj, now: datetime = None, **kwargs):
        output = {}
        for k, v in obj.items():
            output[k] = v
            if k == self.name:
                date_string = obj[self.name]
                time = datetime.strptime(date_string, self.format)
                if now is not None:
                    diff = now - time
                    if self.second:
                        output['diff_second'] = diff.total_seconds()
                    else:
                        output['diff_day'] = diff.days + int(diff.seconds > 0)
                for unit in self.units:
                    if unit == 'weekday':
                        output[unit] = time.weekday()
                    elif hasattr(time, unit):
                        output[unit] = getattr(time, unit)
        return output

    def extra_repr(self) -> str:
        return "name='{}', units={}, diff_units='{}'".format(
            self.name, list(self.units), 'second' if self.second else 'day')


class Timestamp4(Operator):
    def __init__(self, name, _format, units, second=False, inplace=False):
        super().__init__(inplace=inplace)
        self.name = name
        self.format = _format
        self.units = {
            unit: '{}_{}'.format(self.name, unit) for unit in units
        }
        self.second = second

    def _call_inplace(self, obj, now: datetime = None, **kwargs):
        if self.name in obj:
            date_string = obj[self.name]
            time = datetime.strptime(date_string, self.format)

            if now is not None:
                diff = now - time
                if self.second:
                    obj['{}_diff_second'.format(self.name)] = diff.total_seconds()
                else:
                    obj['{}_diff_day'.format(self.name)] = diff.days + int(diff.seconds > 0)
            for unit, feat_name in self.units.items():
                if unit == 'weekday':
                    obj[feat_name] = time.weekday()
                elif hasattr(time, unit):
                    obj[feat_name] = getattr(time, unit)
        return obj

    def _call(self, obj, now: datetime = None, **kwargs):
        output = {}
        for k, v in obj.items():
            output[k] = v
            if k == self.name:
                date_string = obj[self.name]
                time = datetime.strptime(date_string, self.format)

                if now is not None:
                    diff = now - time
                    if self.second:
                        output['{}_diff_second'.format(self.name)] = diff.total_seconds()
                    else:
                        output['{}_diff_day'.format(self.name)] = diff.days + int(diff.seconds > 0)
                for unit, feat_name in self.units.items():
                    if unit == 'weekday':
                        output[feat_name] = time.weekday()
                    elif hasattr(time, unit):
                        output[feat_name] = getattr(time, unit)
        return output

    def extra_repr(self) -> str:
        return "name='{}', units={}, diff_units='{}'".format(
            self.name, list(self.units), 'second' if self.second else 'day')
