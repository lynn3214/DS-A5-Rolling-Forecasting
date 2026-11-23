import numpy as np

from scripts.verify_student_review_findings import scalar_lookup, tail_components


def test_tail_summary_keeps_signed_and_absolute_contributions_separate():
    d = np.array([-10.0, 1.0, 2.0, 3.0])
    result = tail_components(d, 0.25)
    assert result["selected_count"] == 1
    assert result["signed_sum"] == -10.0
    assert result["absolute_sum"] == 10.0
    assert result["signed_share_of_net"] == 2.5
    assert result["absolute_share_of_absolute_total"] == 10.0 / 16.0


def test_scalar_lookup_is_past_only_and_obeys_five_second_tolerance():
    ts = np.array([0, 10, 20, 30], dtype=np.int64) * 1_000_000_000
    values = np.arange(4, dtype=float)
    # At issue=30s, lag=10s requests 20s and matches exactly.
    j, age, reason, eligible = scalar_lookup(ts, values, 3, 10)
    assert (j, age, reason, eligible) == (2, 0.0, "eligible", True)
    # At issue=30s, lag=15s requests 15s; the latest past row is 10s, age 5s.
    j, age, reason, eligible = scalar_lookup(ts, values, 3, 15)
    assert (j, age, reason, eligible) == (1, 5.0, "eligible", True)
    # A 4s age is not available from this grid; request is 14s, latest past is 10s.
    j, age, reason, eligible = scalar_lookup(ts, values, 3, 16)
    assert (j, age, reason, eligible) == (1, 4.0, "eligible", True)


def test_scalar_lookup_rejects_stale_observation_and_history_gap():
    ts = np.array([0, 10, 20, 100], dtype=np.int64) * 1_000_000_000
    values = np.arange(4, dtype=float)
    # Requested 95s, last record is 20s (age 75s).
    j, age, reason, eligible = scalar_lookup(ts, values, 3, 5)
    assert (j, age, reason, eligible) == (2, 75.0, "stale_over_5s", False)
    # Selected row is recent, but a >60s gap lies within its history segment.
    ts2 = np.array([0, 70, 140], dtype=np.int64) * 1_000_000_000
    j, age, reason, eligible = scalar_lookup(ts2, values, 2, 70)
    assert (j, age, reason, eligible) == (1, 0.0, "history_gap_over_60s", False)
