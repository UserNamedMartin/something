def merge_sorted_lists(list_1:list[int], list_2:list[int]) :
    output = list()
    ind_1, ind_2 = 0, 0
    len_1, len_2 = len(list_1), len(list_2)
    while len_1 > ind_1 and len_2 > ind_2 :
        el_1 = list_1[ind_1]
        el_2 = list_2[ind_2]
        if el_1 < el_2 :
            output.append(el_1)
            ind_1 += 1
        else :
            output.append(el_2)
            ind_2 += 1
    output.extend(list_1[ind_1:])
    output.extend(list_2[ind_2:])
    return output

def sort_list(unsorted_list:list[int]) -> list[int] :
    if len(unsorted_list) == 1 :
        return unsorted_list
    middle = len(unsorted_list)//2
    sorted_left = sort_list(unsorted_list[:middle])
    sorted_right = sort_list(unsorted_list[middle:])
    return merge_sorted_lists(sorted_left, sorted_right)
    
z = [9,8,6,4,6,8,9,6,4,5,3,2,7,8,9,7,1,2,9,8,3,4,7,6,4,5,6,5,4]
x = sort_list(z)
print(x)
