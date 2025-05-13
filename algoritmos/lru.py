def lru(data):
	cache_size = data["size"]
	requests = data["requests"]
	cache = [-1 for _ in range(cache_size)]


	output = {}
	output["states"] = [];

	victim = 0
	hit = 0
	n = len(requests)
	indx = -1
	last_used = [ -1 for _ in range(cache_size)]
	time = 0
	fill = 0

	for request in requests:
		try:
			indx = cache.index(request)
		except ValueError:
			indx = -1

		if( indx != -1):
			hit = hit + 1;
			last_used[indx] = time
			state = { "status": "H",
					  "cache": " ".join(str(e) for e in cache) ,
					  "lru": " ".join(str(e) for e in last_used) }
			output["states"].append(state)


		else:
			if(-1 in cache):
				victim = cache.index(-1)
			else:
				victim = last_used.index(min(last_used))

			cache[victim] = request
			last_used[victim] = time

			state = { "status": "M",
					  "cache": " ".join(str(e) for e in cache) ,
					  "lru": " ".join(str(e) for e in last_used) }
			output["states"].append(state)

		time = time + 1

	output["hits"] = hit
	output["miss"] = n - hit
	output["hit-ratio"] = round(float(hit)/n,2);

	return output