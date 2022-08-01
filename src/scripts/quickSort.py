def partition(array, key, low, high, asc):
  pivot = array[high]
  i = low - 1

  for j in range(low, high):
    if (asc):
        if array[j][key] <= pivot[key]:
            i = i + 1

            (array[i], array[j]) = (array[j], array[i])

    else:
        if array[j][key] >= pivot[key]:
            i = i + 1

            (array[i], array[j]) = (array[j], array[i])


  (array[i + 1], array[high]) = (array[high], array[i + 1])

  return i + 1

def quickSort(array, key, low, high, asc = True):
  if low < high:

    pi = partition(array, key, low, high, asc)

    quickSort(array, key, low, pi - 1, asc)
    quickSort(array, key, pi + 1, high, asc)
