"""Deterministic timestamp lookup helpers for the approved temporal protocol."""
import numpy as np

def latest_history_index(times, query_time, max_age=5.0):
    """Latest time <= query, accepting only query-time in [0,max_age] after it."""
    i=int(np.searchsorted(times,query_time,side='right'))-1
    if i<0 or query_time-times[i] < 0 or query_time-times[i] > max_age:
        return -1
    return i

def seasonal_reference_index(times, values, issue_time, reference_time, max_age=5.0):
    """Historical-only seasonal lookup; reference must be no later than issue."""
    if reference_time > issue_time:
        return -1
    i=latest_history_index(times,reference_time,max_age)
    if i<0 or not np.isfinite(values[i]) or times[i]>issue_time:
        return -1
    return i

def lag_feature_index(times, values, issue_time, lag_seconds, max_age=5.0, max_gap=60.0):
    """Point-in-time lag lookup; all adjacent gaps from chosen sample through issue must be allowed."""
    requested=issue_time-lag_seconds
    if requested>issue_time or lag_seconds<0:
        return -1
    i=latest_history_index(times,requested,max_age)
    if i<0 or not np.isfinite(values[i]):
        return -1
    end=int(np.searchsorted(times,issue_time,side='right'))-1
    if end<0 or end<i or times[end]>issue_time:
        return -1
    if end>i and np.any(np.diff(times[i:end+1])>max_gap):
        return -1
    return i
