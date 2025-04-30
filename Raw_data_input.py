
def createRawList(text):
    lines = text.strip().split('\n')
    numbers_str = [line.strip() for line in lines]
    python_list_str = "[" + ", ".join(numbers_str) + "]"

    numbers_int_list = [int(num_str) for num_str in numbers_str]
    return numbers_int_list

def createList(lis):
    newList = []
    for i in range(len(lis)):
        newList.append(4000-lis[i])
    return newList

