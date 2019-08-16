def merge_findings(ranges):
    result = []
    current_start = -1
    current_stop = -1

    for start, stop in sorted(ranges):
        if start > current_stop:
            result.append( (start, stop) )
            current_start, current_stop = start, stop
        else:
            result[-1] = (current_start, max(current_stop, stop))
            current_stop = max(current_stop, stop)

    return result

