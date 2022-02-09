def bubble_sort(data: list):
    """冒泡排序"""
    flag = True
    while flag:
        flag = False
        for index in range(len(data) - 1):
            if data[index] <= data[index + 1]:
                continue
            else:
                data[index], data[index + 1] = data[index + 1], data[index]
                flag = True
    return data


def insert_sort(data: list):
    """插入排序"""
    if not data:
        return list()

    for i in range(len(data)):
        pre_index = i - 1
        current = data[i]
        while pre_index >= 0 and data[pre_index] > current:
            data[pre_index+1] = data[pre_index]
            pre_index -= 1
        data[pre_index+1] = current
    return data


def merge_sort(data: list):
    """归并排序"""
    mid = len(data) // 2

    part_1 = data[:mid]
    part_2 = data[mid:]

    if len(part_1) > 1:
        part_1 = merge_sort(part_1)
    if len(part_2) > 1:
        part_2 = merge_sort(part_2)

    if not part_1 or not part_2:
        return part_1 + part_2

    i = j = 0
    part = list()
    part_1_len = len(part_1)
    part_2_len = len(part_2)
    while i < part_1_len and j < part_2_len:
        if part_1[i] < part_2[j]:
            part.append(part_1[i])
            i += 1
        else:
            part.append(part_2[j])
            j += 1
    part += part_1[i:] + part_2[j:]
    return part


def get_pivot(data: list):
    """三平均分区法"""
    data_length = len(data)
    assert data_length, '空数组'
    if data_length > 3:
        mid = data[data_length // 2]
        if data[0] > data[-1] and data[0] > data[mid] and data[-1] > data[mid]:
            return data[-1]
        elif data[-1] > data[mid] and data[-1] > data[0] and data[0] > data[mid]:
            return 0, data[0]
        else:
            return mid, data[mid]
    else:
        return 0, data[0]


def two_partition(data: list, start: int = 0, end: int = 0):
    """二分区操作"""

    if start >= end:
        return
    left, right = start, end

    pivot_index, pivot = get_pivot(data[start:end])
    pivot_index = start + pivot_index

    flag = False
    while left < right:
        while right > pivot_index and data[right] >= pivot:
            right -= 1
        if right > pivot_index:
            data[pivot_index] = data[right]
            pivot_index = right
            flag = True
        while left < pivot_index and data[left] <= pivot:
            left += 1

        if left < pivot_index:
            data[pivot_index] = data[left]
            pivot_index = left
            flag = True

    if flag is True:
        data[right] = pivot

    two_partition(data=data, start=start, end=left-1)
    two_partition(data=data, start=right+1, end=end)


def three_partition(data: list, start: int = 0, end: int = 0):
    """三分区操作"""

    pass


def quick_sort(data: list):
    """快速排序"""
    if not data:
        return data

    two_partition(data=data, start=0, end=len(data) - 1)
    return data


def shell_sort(data: list):
    """希尔排序"""
    n = len(data)
    gap = int(n/2)

    while gap > 0:
        for i in range(gap, n):
            index = i
            value = data[i]
            while index >= gap and data[index-gap] > value:
                data[index] = data[index-gap]
                index -= gap
            data[index] = value

        gap = int(gap/2)
    return data


def select_sort(data: list):
    """选择排序"""
    length = len(data)
    i = 0
    while i < length:
        min_index = i
        for j in range(i, length):
            if data[j] < data[min_index]:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]
        i += 1
    return data


def main():
    example = [1, 3, 2, 0, 9, 5, 4, 7, 8, 6, 4]
    print('example', example)
    # 冒泡排序
    # print(bubble_sort(example))
    # 插入排序
    print(insert_sort(example))
    # 归并排序
    # print(merge_sort(example))
    # 快速排序
    # print(quick_sort(example))
    # 希尔排序
    # print(shell_sort(example))
    # 选择排序
    # print(select_sort(example))


if __name__ == '__main__':
    main()
