import sys
import random
import threading
import time

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivo = arr[len(arr) // 2]
    esquerda = [x for x in arr if x < pivo]
    meio = [x for x in arr if x == pivo]
    direita = [x for x in arr if x > pivo]

    return quicksort(esquerda) + meio + quicksort(direita)

def bubble_sort(lista):
    elementos = len(lista)-1
    ordenado = False
    while not ordenado:
        ordenado = True
        for i in range(elementos):
            if lista[i] > lista[i+1]:
                lista[i], lista[i+1] = lista[i+1],lista[i]
                ordenado = False
    return lista

def sort_segment(arr, sorted_segments, thread_id):
    sorted_segments.append(bubble_sort(arr))
    print(f"Thread ID {thread_id}: Total de Elementos Ordenados {len(arr)}")

def merge(arr1, arr2, merge_array):
    result = []
    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1

    result += arr1[i:] + arr2[j:]
    merge_array.append(result)

def split_array(arr, k):
    start_i = 0
    tam_seg = len(arr) // k
    segments = []

    for i in range(k):
        end_i = start_i + tam_seg
        if i == k - 1:
            end_i = n
        segments.append(arr[start_i:end_i])
        start_i = end_i

    return segments

if __name__ == "__main__":
    k = int(sys.argv[1])
    n = int(sys.argv[2])

    # array aleatorio
    random.seed(100)
    array = [random.randint(1, 10000) for i in range(n)]

    # dividindo o array em k segmentos
    segments_list = split_array(array,k)

    thread_list = []
    sorted_segments = []
    
    start_time = time.time() # inicia a contagem do tempo com threads

    # Ordenacao dos segmentos por threads
    thread_id = 1
    for segment in segments_list:
        thread = threading.Thread(target=sort_segment, args=(segment,sorted_segments,thread_id, ))
        thread_id += 1
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

    # Merge dos segmentos ordenados
    while len(sorted_segments) > 1:
        merge_array = []
        thread_list = []

        for i in range(0, len(sorted_segments) - 1, 2):
            thread = threading.Thread(target=merge, args=(sorted_segments[i], sorted_segments[i + 1], merge_array,))
            thread.start()
            thread_list.append(thread)

        for thread in thread_list:
            thread.join()

        # Merge do último segmento, se houver
        if len(sorted_segments) % 2 == 1:
            merge_array.append(sorted_segments[-1])
            
        sorted_segments = merge_array

    end_time = time.time()  # finaliza a contagem do tempo com threads

    print(f"\nTempo total de execução: {end_time - start_time:.6f} segundos")