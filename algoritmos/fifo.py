def fifo(data):
    print("reached here")
    cache_size = data["size"]
    requests = data["requests"]
    cache = [-1 for _ in range(cache_size)]



    output = {}
    output["states"] = [];

    victim = 0
    hit = 0
    n = len(requests)
    indx = -1

    for request in requests:
    	try:
    		indx = cache.index(request)
    	except ValueError:
    		indx = -1

    	if( indx != -1):

    		state = { "status": "H",
    				  "cache": " ".join(str(e) for e in cache)  }

    		hit = hit + 1;

    	else:
    		cache[victim] = request
    		victim = (victim + 1) % cache_size

    		state = { "status": "M",
    				  "cache": " ".join(str(e) for e in cache)  }


    	output["states"].append(state)
    output["hits"] = hit
    output["miss"] = n - hit
    output["hit-ratio"] = round(float(hit)/n,2);

    return output