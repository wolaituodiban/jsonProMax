from cgitb import text
from datetime import datetime
import re
import json
import os
import cProfile
import jsonpromax as jpm
import json_tools
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def process(obj, now):
    tokenizer = jpm.default_tokenizer()
    output = []
    for item in sorted(obj, key=lambda x: x.get('time')):
        new_item = {}
        time = datetime.strptime(item['time'], '%y-%m-%d %H:%M:%S.%f')
        diff = now - time
        new_item['time_diff_second'] = diff.total_seconds()
        new_item['time_month'] = time.month
        new_item['time_day'] = time.day
        new_item['time_hour'] = time.hour
        new_item['time_minute'] = time.minute
        new_item['time_second'] = time.second
        new_item['time_weekday'] = time.weekday()
        if 'text' in item:
            new_item['text'] = tokenizer.lcut(jpm.rm_ascii(item['text']).lower())
        if 'dict' in item:
            if 'a' in item['dict']:
                new_item['dict'] = item['dict']['a']
        if 'list' in item:
            new_item['list'] = item['list'][1:3]
        output.append(new_item)
    return output


if __name__ == '__main__':
    with open('test_data.json', 'r', encoding='utf-8') as file:
        test_data = json.load(file)
    
    timestamp_op = jpm.Timestamp4(
        'time',
        _format='%y-%m-%d %H:%M:%S.%f',
        units=['month', 'day', 'weekday', 'hour', 'minute', 'second'],
        second=True
    )
    processor = jpm.JsonPathTree(
        processors=[
            ('$', jpm.Sorted(key='time')),
            ('$.*', timestamp_op),
            ('$.*', jpm.Delete(['time', 'delete'])),
            ('$.*.text', jpm.RemoveASCII()),
            ('$.*.text', jpm.Lower()),
            ('$.*.text', jpm.Cut()),
            ('$.*.dict', jpm.DictGetter(['a'])),
            ('$.*.list', jpm.Slice(slice(1, 3)))
        ],
        tokenizer=jpm.default_tokenizer(),
        inplace=False,
        error=True,
        warning=True
    )
    now = datetime.now()
    # processor(test_data, now=now) 
    print(processor(test_data, now=now))
    print(process(test_data, now=now))
    # cProfile.run("processor(test_data, now=now)", sort='time')
    