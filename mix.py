def mix(match1, match2):
    combined = []
    
    for arr1 in match1:
        for arr2 in match2:
            if any(x in arr1 for x in arr2): # if match found
                new = []
                new.extend(arr1)
                new.extend(arr2)
                new = list(dict.fromkeys(new))
                combined.append(new)
                if arr1 in combined:
                    combined.remove(arr1)
                if arr2 in combined:
                    combined.remove(arr2)
            else:
                if arr1 not in combined:
                    combined.append(arr1)
                if arr2 not in combined:
                    combined.append(arr2)
    
    for i in range(len(combined) - 1):
        for j in range(i + 1, (len(combined))):
            if any(m in combined[i] for m in combined[j]):
                combined[i].extend(combined.pop(j))
    
    for idx in range(len(combined)):
        combined[idx] = list(dict.fromkeys(combined[idx]))

    return combined


ar1 = [[9, 10, 11], [12, 13, 14]]
ar2 = [[12, 18, 24], [14, 20, 26]]
print(mix(ar1, ar2))