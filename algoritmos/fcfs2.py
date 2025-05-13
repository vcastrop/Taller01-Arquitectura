def fcfs2(start, requests):
    seek_sequence = []
    total = 0
    current = start
    for req in requests:
        seek_sequence.append(req)
        total += abs(req - current)
        current = req
    return seek_sequence, total