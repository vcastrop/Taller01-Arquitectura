from operator import itemgetter

def fcfs(data):
    process = {}
    process['table'] = sorted(data, key=itemgetter('at'))
    process['gantt'] = []
    time = process['table'][0]['at'] if process['table'] else 0

    for p in process['table']:
        entry = {'no': p['no'], 'start': max(time, p['at'])}
        time = entry['start'] + p['bt']
        p['ct']  = time
        p['tat'] = p['ct'] - p['at']
        p['wt']  = p['tat'] - p['bt']
        entry['stop'] = time
        process['gantt'].append(entry)

    return process
