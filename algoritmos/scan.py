def scan(start, previous, requests, cylinders):
    seek_sequence = []
    total = 0
    direction = 1 if start > previous else -1
    requests = sorted(requests)
    lower = [r for r in requests if r < start]
    upper = [r for r in requests if r >= start]

    if direction == 1:
        for r in upper:
            seek_sequence.append(r)
            total += abs(r - start)
            start = r
        for r in reversed(lower):
            seek_sequence.append(r)
            total += abs(r - start)
            start = r
    else:
        for r in reversed(lower):
            seek_sequence.append(r)
            total += abs(r - start)
            start = r
        for r in upper:
            seek_sequence.append(r)
            total += abs(r - start)
            start = r

    return seek_sequence, total