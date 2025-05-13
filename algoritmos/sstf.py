def sstf(start, requests):
    seek_sequence = []
    total = 0
    current = start
    local_requests = requests[:]
    while local_requests:
        next_req = min(local_requests, key=lambda x: abs(x - current))
        total += abs(next_req - current)
        seek_sequence.append(next_req)
        current = next_req
        local_requests.remove(next_req)
    return seek_sequence, total