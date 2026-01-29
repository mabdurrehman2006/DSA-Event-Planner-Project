from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple

@dataclass(frozen=True)
class Activity:
    name: str
    time: int          
    cost: float        
    enjoyment: int     

def brute_force_optimal_plan(
    activities: List[Activity],
    max_time: Optional[int] = None,
    max_budget: Optional[float] = None
) -> Dict[str, Any]:
    """
    Brute-force search over all 2^n subsets of activities.

    Requirements satisfied:
    - Generates all subsets (2^n) via bitmasks.
    - Checks feasibility against time and/or budget constraints.
    - Computes total enjoyment for feasible subsets.
    - Tracks and returns the best feasible subset (max enjoyment).
    - Returns chosen activities, total enjoyment, time used, and cost.

    If max_time is None, time is unconstrained.
    If max_budget is None, budget is unconstrained.
    """

    n = len(activities)

    best_subset: List[Activity] = []
    best_enjoyment = float("-inf")
    best_time = 0
    best_cost = 0.0

    # Enumerate all subsets: masks 0..(2^n - 1)
    for mask in range(1 << n):
        subset: List[Activity] = []
        total_time = 0
        total_cost = 0.0
        total_enjoyment = 0

        # Build subset and compute totals
        for i in range(n):
            if mask & (1 << i):  # bit i is set => include activity i
                a = activities[i]
                subset.append(a)
                total_time += a.time
                total_cost += a.cost
                total_enjoyment += a.enjoyment

        # Feasibility check
        if max_time is not None and total_time > max_time:
            continue
        if max_budget is not None and total_cost > max_budget:
            continue

        if total_enjoyment > best_enjoyment:
            best_enjoyment = total_enjoyment
            best_subset = subset
            best_time = total_time
            best_cost = total_cost

    # Handle the case where nothing is feasible
    if best_enjoyment == float("-inf"):
        return {
            "activities": [],
            "total_enjoyment": 0,
            "time_used": 0,
            "cost": 0.0,
            "note": "No feasible subset found under the given constraints."
        }

    return {
        "activities": [a.name for a in best_subset],
        "total_enjoyment": int(best_enjoyment),
        "time_used": best_time,
        "cost": float(best_cost),
    }


# Example usage:
if __name__ == "__main__":
    activities = [
        Activity("Museum", time=3, cost=12.0, enjoyment=8),
        Activity("Park", time=2, cost=0.0, enjoyment=5),
        Activity("Concert", time=4, cost=30.0, enjoyment=10),
        Activity("Cafe", time=1, cost=8.0, enjoyment=4),
    ]

    result = brute_force_optimal_plan(activities, max_time=6, max_budget=20.0)
    print(result)

