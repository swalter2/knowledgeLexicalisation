#http://en.wikipedia.org/wiki/Levenshtein_distance

def calculate_normalized_levenshtein_distance(s1, s2):
    """
    Calculates the normalized Levenshtein distance for two given terms
    """
    if len(s1) < len(s2):
        return calculate_normalized_levenshtein_distance(s2, s1)
    if not s1:
        return len(s2)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return (1-(previous_row[-1] / (max(len(s1),len(s2))+0.0)) if previous_row[-1]!=0 else 1.0)


