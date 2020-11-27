import time
import random

# start = time.time()
# print("hello")
# end = time.time()
# print(end - start)

def printArray(array):
    for element in array:
        print(element, end=' ')


def generateRandomNumbers(size):
    randomnumersarray = []
    for i in range(0, size):
        randNumber = random.randint(1000, 9999)
        randomnumersarray.append(randNumber)
    return randomnumersarray
    # print(randomnumersarray)

rand50Numbers = generateRandomNumbers(50)
rand100Numbers = generateRandomNumbers(100)


def BubbleSort(array):


    for j in range(len(array)):

        for k in range(len(array)-j-1):

            if array[k] > array[k+1]:
                temp = array[k]
                array[k] = array[k+1]
                array[k+1] = temp





unsortedArray = rand50Numbers
print("Before Bubble Sort: ")
printArray(unsortedArray)
start = time.time()
BubbleSort(unsortedArray)
end = time.time()
print("\n After Bubble Sort: ")
printArray(unsortedArray)
print('\nTime Taken: ',end - start, ' seconds')
print("\n____________________________")



def MergeSort(array):

    if len(array) > 1:

        array_middle = len(array) // 2

        Left_array = array[:array_middle]
        Right_array = array[array_middle:]

        MergeSort(Left_array)
        MergeSort(Right_array)

        Left_Array_Index = Right_Array_Index = Array_Index = 0


        while Left_Array_Index < len(Left_array) and Right_Array_Index < len(Right_array):
            if Left_array[Left_Array_Index] < Right_array[Right_Array_Index]:
                array[Array_Index] = Left_array[Left_Array_Index]
                Left_Array_Index += 1
            else:
                array[Array_Index] = Right_array[Right_Array_Index]
                Right_Array_Index += 1
            Array_Index += 1

        while Left_Array_Index < len(Left_array):
            array[Array_Index] = Left_array[Left_Array_Index]
            Left_Array_Index += 1
            Array_Index += 1

        while Right_Array_Index < len(Right_array):
            array[Array_Index] = Right_array[Right_Array_Index]
            Right_Array_Index += 1
            Array_Index += 1



unsortedArray = rand50Numbers
print("Before Merge Sort: ")
printArray(unsortedArray)
start1 = time.time()
MergeSort(unsortedArray)
print("\n After Merge Sort: ")
printArray(unsortedArray)
end1 = time.time()
print('\nTime Taken: ',end1 - start1, ' seconds')
print("\n____________________________")



