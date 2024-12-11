
from ..k_means_handler.distance import euclidean_distance_with_weights_2

def mean_euclid_distance_of_room(room_member_ids, weights):
    d = euclidean_distance_with_weights_2(room_member_ids, weights)
    return sum(sum(d2.values()) for d2 in d.values())/(len(room_member_ids)**2)
