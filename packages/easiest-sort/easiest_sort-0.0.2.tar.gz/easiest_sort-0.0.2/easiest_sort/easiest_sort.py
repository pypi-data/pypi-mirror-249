#Bubble Sort
def bubble_sort(arr, order=True):
    n = len(arr)

    for i in range(n - 1):
        swapped = False

        for j in range(0, n - i - 1):
            
            compare_result = arr[j] - arr[j + 1] if order else arr[j + 1] - arr[j]

            if compare_result > 0:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break



#Merge Sort
def merge_sort(arr, order=True):
    if len(arr) > 1:
        mid = len(arr) // 2  
        left_half = arr[:mid]  
        right_half = arr[mid:]

        merge_sort(left_half, order)  
        merge_sort(right_half, order)  

        i = j = k = 0
  
        while i < len(left_half) and j < len(right_half):
            compare_result = left_half[i] - right_half[j] if order else right_half[j] - left_half[i]

            if compare_result < 0:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1




#Quick Sort
def quick_sort(arr, order=True):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]  
        less = [x for x in arr[1:] if x <= pivot]
        greater = [x for x in arr[1:] if x > pivot]

        sorted_less = quick_sort(less, order)
        sorted_greater = quick_sort(greater, order)

        return sorted_less + [pivot] + sorted_greater if order else sorted_greater + [pivot] + sorted_less




#Insertion Sort
def insertion_sort(arr, order=True):
    for i in range(1, len(arr)):
        current_value = arr[i]
        position = i

        while position > 0 and (arr[position - 1] > current_value if order else arr[position - 1] < current_value):
            arr[position] = arr[position - 1]
            position -= 1

        arr[position] = current_value



#Heap Sort
def _heapify(arr, n, i, order=True):
    largest = i  
    left_child = 2 * i + 1
    right_child = 2 * i + 2
   
    if left_child < n and (arr[left_child] > arr[largest] if order else arr[left_child] < arr[largest]):
        largest = left_child

    if right_child < n and (arr[right_child] > arr[largest] if order else arr[right_child] < arr[largest]):
        largest = right_child

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  
        _heapify(arr, n, largest, order)

def heap_sort(arr, order=True):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i, order)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i] 
        _heapify(arr, i, 0, order) 



#Shell Sort
def shell_sort(arr, order=True):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i

            while j >= gap and (arr[j - gap] > temp if order else arr[j - gap] < temp):
                arr[j] = arr[j - gap]
                j -= gap

            arr[j] = temp

        gap //= 2



#Partial Sort
def partial_sort(arr, k, top=True, reverse=False):
    sorted_part = sorted(arr[:k], reverse=reverse) if top else sorted(arr[-k:], reverse=reverse)
    return sorted_part + arr[k:] if top else arr[:-k] + sorted_part



#Sort Dataframe






