from queue import Queue

def rr(data, tq):
    """
    Round Robin scheduling.
    data: lista de dicts con 'no','at','bt';
    tq: time quantum
    Devuelve { 'table': [...], 'gantt': [...] }
    """
    # hacemos copia para no mutar el original
    process = { 'table': [dict(p) for p in data], 'gantt': [] }
    Q    = Queue()
    time = 0
    left = len(process['table'])

    # ordenamos por llegada
    procs = sorted(process['table'], key=lambda x: x['at'])
    idx   = 0

    while left > 0:
        # encolamos los recién llegados
        while idx < len(procs) and procs[idx]['at'] <= time:
            Q.put(procs[idx]); idx += 1

        if not Q.empty():
            curr  = Q.get()
            start = time
            run   = min(curr['bt'], tq)
            time += run
            curr['bt'] -= run
            stop  = time
            process['gantt'].append({'no': curr['no'], 'start': start, 'stop': stop})

            # encolamos nuevas llegadas durante la ejecución
            while idx < len(procs) and procs[idx]['at'] <= time:
                Q.put(procs[idx]); idx += 1

            if curr['bt'] > 0:
                Q.put(curr)
            else:
                curr['ct']  = time
                curr['tat'] = curr['ct'] - curr['at']
                # wt = tat - burst original
                orig_bt     = curr.get('original_bt', curr['tat'] - curr['at'])
                curr['wt']  = curr['tat'] - orig_bt
                left -= 1
        else:
            # CPU idle
            process['gantt'].append({'no': -1, 'start': time, 'stop': time + 1})
            time += 1

    return process
