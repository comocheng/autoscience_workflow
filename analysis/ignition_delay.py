import numpy as np


def get_index_of_closest_time(times, t_ref):
    # helper function for converting a time in seconds to an index of the time array
    t_diff = np.abs(np.array(times) - t_ref)
    min_diff = min(t_diff)
    return list(t_diff).index(min_diff)


def check_valid_ignition(P, time_index, threshold_ratio=1.5):
    pressures = P[: time_index + 1]
    return np.max(pressures) / P[0] > threshold_ratio


def get_ignition_delays(times, pressures):
    """
    Returns the ignition delay time given an array of simulation times and pressures (unit agnostic)
    For continuity, this returns (second_ignition, first_ignition)

    where first_ignition is -1 if it's not a two-stage ignition event
    and second_ignition is -1 if no ignition is detected
    """

    # Figure out when a valid ignition is detected
    switch_index = -1
    ignitions = [check_valid_ignition(pressures, i) for i in range(len(times))]
    for i in range(1, len(ignitions)):
        if ignitions[i] and not ignitions[i - 1]:
            switch_index = i
            break


    slopes = np.gradient(pressures, times)
    votes = [0]  # 0 gets to vote for itself
    for i in range(1, len(times)):
        votes.append(np.argmax(slopes[0:i]))
        
    # count up the votes
    totals = np.zeros(len(times))
    for i in range(len(times)):
        totals[i] = np.sum(np.array(votes) == i)
    
    # get top 3 choices
    n = 3
    top_n_indices = []
    sorted(totals)
    for i in range(0, n):
        vote_count = sorted(totals)[-1 - i]
        time_index = list(totals).index(vote_count)
        top_n_indices.append(time_index)

    
    second_ignition_index = max(top_n_indices)
    valid_ignition = check_valid_ignition(pressures, second_ignition_index) or np.isclose(times[second_ignition_index], times[switch_index], rtol=0.05)
    if not valid_ignition:  # no valid ignition detected
        return -1, -1


    # get the first ignition time, which should be the second latest ignition time in the top voted
    first_ignition_index = sorted(top_n_indices)[-2]

    # zoom in on it
    flat_level = np.median(pressures[:second_ignition_index])
    first_entrance = -1
    first_exit = -1
    ratio = 1.1
    for i in range(len(times)):
        if pressures[i] > flat_level / ratio:
            first_entrance = i
            break

    for i in range(first_entrance, len(times)):
        if pressures[i] > flat_level * ratio:
            first_exit = i
            break

    if first_entrance == -1 or first_exit == -1:
        print('could not zoom in on 1st iginition delay')
        return second_ignition_index, -1


    # look at the region between the first and second ignition and see if it's higher than the starting pressure
    sample_times = np.linspace(times[first_entrance], times[first_exit], 101)
    sample_indices = [get_index_of_closest_time(times, t) for t in sample_times]
    sample_Ps = [pressures[i] for i in sample_indices]
    sampled_flat_level = np.median(sample_Ps)
    if sampled_flat_level / pressures[0] > 1.05:
        # This is a two-stage ignition delay
        return times[second_ignition_index], times[first_ignition_index]
    
    return times[second_ignition_index], -1
