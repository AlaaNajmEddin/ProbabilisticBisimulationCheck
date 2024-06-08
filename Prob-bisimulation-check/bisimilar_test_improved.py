from typing import Tuple
from decimal import Decimal
import traceback
import pandas as pd

from datetime import datetime


def bisimilarity_test(df1: pd.DataFrame, df2: pd.DataFrame) -> Tuple[str, str]:
    print("bisimilar test improved called")
    print(df1)
    print(df2)
    start_time = datetime.now().timestamp()
    cross_product = calculate_cross_product(df1, df2)
    filtered_tuples = filter_tuples(cross_product, df1, df2)
    merged_tuples = distict_merge_tupels(filtered_tuples)
    # print(merged_tuples)
    # equivalence_classes_result = equivalence_classes(merged_tuples, df1, df2)

    # previous = set(merged_tuples)
    # next = equivalence_classes(previous, df1, df2)
    #
    # while not previous == next:
    #     tmp = next
    #     previous = tmp
    #     next = equivalence_classes(previous, df1, df2)

    equivalence_classes_result = determine_all_equivalence_classes(merged_tuples, df1, df2)
    print(equivalence_classes_result)

    end_time = datetime.now().timestamp()
    laufzeit = end_time - start_time

    print(f'Laufzeit = {laufzeit} Sekunden')

    return to_string(equivalence_classes_result), str(laufzeit)


def to_string(merged_tuples: list[Tuple[str, str]]) -> str:
    res = '{ '
    for tuple in merged_tuples:
        res += convertTuple(tuple)
    res += ' }'
    return res


def convertTuple(tup):
    st = '('
    st += ', '.join(map(str, tup))
    st += '), '
    return st


# Jeder Zustand mit sich selbst und mit anderen Zuständen

def calculate_cross_product(df1: pd.DataFrame, df2: pd.DataFrame) -> list[Tuple[str, str]]:
    all_nodes_df1 = set(df1['Node'].tolist() + df1['target'].tolist())
    all_nodes_df2 = set(df2['Node'].tolist() + df2['target'].tolist())
    union = list(all_nodes_df1 | all_nodes_df2)
    i = 0
    j = 0
    res = []
    while i < len(union):
        while j < len(union):
            pair = union[i], union[j]
            res.append(pair)
            j += 1
        i += 1
        j = i

    return res


# tupeln, die die selben Labels zu Liste similar_labels hinzufügen und die restlichen entfernen.
# first und second (gleiche Labels)
def filter_tuples(cross_product, df1: pd.DataFrame, df2: pd.DataFrame) -> list[Tuple[str, str]]:
    similar_labels = []
    both_dataframes = pd.concat([df1, df2])
    for first, second in cross_product:
        first_labels = both_dataframes.loc[both_dataframes['Node'] == first]['output_labels']
        first_labels = set([x for x in first_labels])

        second_labels = both_dataframes.loc[both_dataframes['Node'] == second]['output_labels']
        second_labels = set([x for x in second_labels])

        if first_labels == second_labels:
            similar_labels.append((first, second))

    return similar_labels


def distict_merge_tupels(tuples: list[Tuple[str, str]]):
    if len(tuples) == 0:
        return []

    merged_tuples = []
    # tuples is the cross product = [('X1', 'X1'), ('X1', 'Y1'), ('Y1', 'Y1'), ('X3', 'X3'), ('Y2', 'Y2'), ('Y2', 'Y3'), ('Y3', 'Y3'), ('X2', 'X2')]
    # merge the tuples
    # merged_tuples result = [('Y3', 'Y3', 'Y2'), ('Y1', 'Y1', 'X1'), ('X3', 'X3'), ('X2', 'X2')]
    # remove duplicates
    for first, second in tuples:
        flattend_list = list(sum(merged_tuples, ()))
        if first not in flattend_list and second not in flattend_list:
            merged_tuples.append((first, second))
        else:
            if first in flattend_list and second not in flattend_list:
                tuple_that_contains_item = find_tuple_that_contains_item(first, merged_tuples)
                merged_tuples.remove(tuple_that_contains_item)
                new_tuple = list(tuple_that_contains_item)
                new_tuple.append(second)
                merged_tuples.append(tuple(new_tuple))
            elif second in flattend_list and first not in flattend_list:
                tuple_that_contains_item = find_tuple_that_contains_item(second, merged_tuples)
                merged_tuples.remove(tuple_that_contains_item)
                new_tuple = list(tuple_that_contains_item)
                new_tuple.append(first)
                merged_tuples.append(tuple(new_tuple))

    distinct_tuples = []
    for not_distinct_tuple in merged_tuples:
        distinct = []
        for inner_tuple_item in not_distinct_tuple:
            if not inner_tuple_item in distinct:
                distinct.append(inner_tuple_item)
        distinct_tuples.append(tuple(distinct))

    # distinct_tuples result = [('X1', 'Y1'), ('Y2', 'Y3'), ('X2',), ('X3',)]
    return distinct_tuples


def find_tuple_that_contains_item(searched_item, merged_tuples) -> Tuple:
    for tuple in merged_tuples:
        for item in tuple:
            if item == searched_item:
                return tuple


def determine_all_equivalence_classes(merged_tuples, df1, df2) -> list[Tuple]:
    previous = set(merged_tuples)
    next = equivalence_classes(previous, df1, df2)

    while not previous == next:
        tmp = next
        previous = tmp
        next = equivalence_classes(previous, df1, df2)

    return next


# calculates probability table based on merged tuples then calls
# determine_equivalence_classes which does the splitting when necessary

def equivalence_classes(merged_tuples, df1, df2) -> list[Tuple]:
    #  {'item':'X2', 'tuple':(x2,y2), 'label':(a, 1)}
    #  {'item':'X2', 'tuple':(x2,y2), 'label':(b, 0.5)}
    probability_table_dict = {
        'item': [],
        'tuple': [],
        'label': [],
        'label_wk_sum': []
    }

    for tuple in merged_tuples:
        for item in tuple:
            for inner_loop_tuple in merged_tuples:
                if tuple == inner_loop_tuple:
                    continue
                determine_label_sums(item, tuple, df1, df2, probability_table_dict)
                determine_label_sums(item, inner_loop_tuple, df1, df2, probability_table_dict)

    # see screenshot
    probability_table = pd.DataFrame.from_dict(probability_table_dict).drop_duplicates()
    return determine_equivalence_classes(probability_table, merged_tuples, df1, df2)


def determine_label_sums(item: str, tuple, df1, df2, data_dict):
    # item could be present in df1 or df2
    df1_labels = df1.loc[df1['Node'] == item]['output_labels']
    df1_labels = set([x for x in df1_labels])

    df2_labels = df2.loc[df2['Node'] == item]['output_labels']
    df2_labels = set([x for x in df2_labels])

    all_labels = df1_labels.union(df2_labels)
    item = item
    for label in all_labels:
        label_sum = Decimal('0.0')
        for inner_tuple_item in tuple:
            label_wk = fetch_probability(item, inner_tuple_item, label, df1, df2)
            try:
                label_sum += label_wk
            except TypeError:
                continue
        data_dict['item'].append(item)
        data_dict['tuple'].append(tuple)
        data_dict['label'].append(label)
        data_dict['label_wk_sum'].append(label_sum)


def find_all_lables(df: pd.DataFrame):
    return set(df['output_labels'])


# struktur der tabel

def fetch_probability(item, inner_tuple_item, label, df1, df2):
    df1_prob = df1.loc[
        (df1['Node'] == item) &
        (df1['target'] == inner_tuple_item) &
        (df1['output_labels'] == label)]['output_prob']

    df2_prob = df2.loc[
        (df2['Node'] == item) &
        (df2['target'] == inner_tuple_item) &
        (df2['output_labels'] == label)
        ]['output_prob']

    if df1_prob.values.size > 0:
        return Decimal(df1_prob.values[0])
    elif df2_prob.values.size > 0:
        return Decimal(df2_prob.values[0])
    else:
        return 0


def determine_equivalence_classes(probability_table: pd.DataFrame, distinct_merged_tuples, df1, df2) -> set[Tuple]:
    if not distinct_merged_tuples or probability_table.empty:
        return []

    # keep splitting until no more split is possible
    # previous = set(distinct_merged_tuples)
    # next = split_merged_tuples(probability_table, distinct_merged_tuples, df1, df2)

    # while not previous == next:
    #     tmp = next
    #     previous = tmp
    #     next = split_merged_tuples(probability_table, previous, df1, df2)

    return split_merged_tuples(probability_table, distinct_merged_tuples, df1, df2)


def split_merged_tuples(probability_table: pd.DataFrame, distinct_merged_tuples, df1, df2):
    final_result = set()
    for label in find_all_lables(df1).union(find_all_lables(df2)):

        for tuple in distinct_merged_tuples:
            if len(tuple) == 1:
                append_if_not_present(tuple, final_result)
                continue

            tuple_prob = pd.DataFrame(columns=['item', 'tuple', 'label', 'label_wk_sum'])
            for inner_tuple_item in tuple:
                probability = probability_table.loc[
                    (probability_table['item'] == inner_tuple_item) &
                    (probability_table['label'] == label)
                    ]
                tuple_prob = pd.concat([tuple_prob, probability], ignore_index=True)

            if tuple_prob.empty:
                append_if_not_present(tuple, final_result)
                continue

            # this try-except statement is only to catch the type error in case it happens
            try:
                check_pairwise_equal(tuple_prob, tuple, final_result)
            except TypeError:
                traceback.print_exc()
                return split_merged_tuples(probability_table, distinct_merged_tuples, df1, df2)

    return final_result


def append_if_not_present(item, set):
    if item not in set:
        flattened_list = [i for tuple in set for i in tuple]
        # check if an item of the tuple to add is already present in the final_result
        for inner_tuple_item in item:
            if inner_tuple_item in flattened_list:
                # don't append
                return
        set.add(item)


def check_pairwise_equal(tuple_prob: pd.DataFrame, tuple_in_check: Tuple, final_result: list[Tuple]):
    distinct_tuples = set(tuple_prob['tuple'].tolist())
    for t in distinct_tuples:
        rows_to_compare: pd.DataFrame = tuple_prob.loc[(tuple_prob['tuple'] == t)]

        dict = {}
        for _, row in rows_to_compare.iterrows():
            if row.loc['label_wk_sum'] not in dict.keys():
                dict[row['label_wk_sum']] = [row['item']]
            else:
                dict[row['label_wk_sum']].append(row['item'])
        if len(dict.keys()) > 1:
            # we need to split the tuple because we have more than one probability
            if tuple_in_check in final_result:
                final_result.remove(tuple_in_check)

            for value in dict.values():
                # beispiel: dict = {0.0: ['Y4', 'X7', 'Y16'], 1.0: ['X10', 'Y6', 'Y1', 'X8']}
                append_if_not_present(tuple(value), final_result)
            return

    append_if_not_present(tuple_in_check, final_result)


if __name__ == "__main__":
    # two transition systems with 5 nodes
    # data_dict_1 = {
    #     'Node': ['X1', 'X1', 'X2', 'X3'],
    #     'output_labels': ['a', 'a', 'b', 'b'],
    #     'output_prob': ['0.5', '0.5', '1.0', '1.0'],
    #     'target': ['X2', 'X3', 'X2', 'X3'],
    # }
    #
    # data_dict_2 = {
    #     'Node': ['Y1', 'Y2'],
    #     'output_labels': ['a', 'b'],
    #     'output_prob': ['1.0', '1.0'],
    #     'target': ['Y2', 'Y2'],
    # }

    # two transition systems with 4 nodes
    # data_dict_1 = {
    #     'Node': ['X', 'X'],
    #     'output_labels': ['a', 'a'],
    #     'output_prob': ['1.0', '1.0'],
    #     'target': ['Y', 'Y'],
    # }
    #
    # data_dict_2 = {
    #     'Node': ['U'],
    #     'output_labels': ['a'],
    #     'output_prob': ['1.0'],
    #     'target': ['Z'],
    # }

    # two transition systems with 6 nodes
    # data_dict_1 = {
    #     'Node':          ['X1', 'X1', 'X2', 'X3', 'X3'],
    #     'output_labels': ['a', 'b',    'a', 'a', 'c'],
    #     'output_prob':   ['1', '1', '1.0', '1.0', '1.0'],
    #     'target':        ['X2', 'X3', 'X2', 'X3', 'X3'],
    # }
    #
    # data_dict_2 = {
    #     'Node':          ['Y1', 'Y1', 'Y2', 'Y2', 'Y3'],
    #     'output_labels': ['b', 'a',    'a', 'c', 'a'],
    #     'output_prob':   ['1', '1', '1.0', '1.0', '1.0'],
    #     'target':        ['Y2', 'Y3', 'Y2', 'Y2', 'Y3'],
    # }

    # two transition systems with 6 nodes

    # data_dict_1 = {
    #     'Node': ['X1' , 'X2' , 'X1'],
    #     'output_labels': ['a' , 'c' ,  'a'],
    #     'output_prob': ['0.5' , '1' ,  '0.5'],
    #     'target': ['X2' , 'X2' , 'X3'],
    # }
    #
    # data_dict_2 = {
    #     'Node': ['Y1' ,  'Y2' , 'Y3'] ,
    #     'output_labels': ['a', 'b', 'b'],
    #     'output_prob': ['1' , '1' ,  '1' ],
    #     'target': ['Y2','Y3', 'Y3'],
    # }

    # two transition systems with 33 nodes
    # data_dict_1 = {
    #     'Node': ['X' , 'X' , 'X' ,  'X' ,  'X' ,  'X' ,  'X' ,  'X' , 'X10'  ,'X8' ,'X5' , 'X5' , 'X7' , 'X3' , 'X3'],
    #     'output_labels': ['a' , 'a' ,  'a' ,  'b' , 'b' ,  'c' ,  'c',   'c' ,  'c' ,  'c' , 'a' ,  'c' ,   'c' ,  'b' ,  'b'],
    #     'output_prob': ['0.3' , '0.5' ,  '0.2' ,  '0.4' ,  '0.6' ,  '0.1' ,  '0.2' ,  '0.7' ,  '1' ,   '1' ,    '1' ,    '1' ,     '1' ,   '0.3' ,  '0.7' ],
    #     'target': ['X1' , 'X2', 'X3', 'X5' , 'X8' , 'X10', 'X12', 'X13', 'X11','X9' , 'X6' , 'X7' , 'X7' , 'X4' , 'X14'],
    # }
    #
    # data_dict_2 = {
    #     'Node': ['Y' ,  'Y' , 'Y' , 'Y' ,  'Y' ,  'Y' , 'Y',  'Y1', 'Y6' ,'Y6' , 'Y3' ,'Y3' ,'Y4' , 'Y15' , 'Y15' ,  'Y16' , 'Y11' ],
    #     'output_labels': ['a' ,  'a' , 'b' , 'b' ,  'b' ,  'c' , 'c',  'c' , 'c' , 'c' ,  'a' , 'c' , 'c' ,   'a' ,  'c' ,     'c' ,   'b'],
    #     'output_prob': ['0.2' ,  '0.8' , '0.2' ,  '0.2' ,  '0.6' , '0.1' , '0.9' ,  '1' ,   '0.8' , '0.2' ,  '1' ,   '1' ,   '1' ,     '1' , ' 1' ,'1' ,     '1' ],
    #     'target': ['Y11','Y10', 'Y3' ,'Y15', 'Y1' ,'Y6' , 'Y8', 'Y2', 'Y14' ,'Y13','Y5' ,'Y4' ,'Y4' ,  'Y17' ,'Y16' ,   'Y16' , 'Y12'],
    # }
    #

    # transition with 10 nodes
    # data_dict_1 = {
    #     'Node': ['x1', 'x1', 'x1', 'x4', 'x5'],
    #     'output_labels': ['a', 'a', 'b', 'c', 'c'],
    #     'output_prob': ['1', '1', '1', '1', '1'],
    #     'target': ['x6', 'x6', 'x8', 'x6', 'x6'],
    # }
    #
    # data_dict_2 = {
    #     'Node': ['x10', 'x10', 'x10', 'x40', 'x50'],
    #     'output_labels': ['a', 'a', 'b', 'c', 'c'],
    #     'output_prob': ['1', '1', '1', '1', '1'],
    #     'target': ['x60', 'x60', 'x60', 'x90', 'x60'],
    # }

    # 2 transition systems with 20 nodes
    # data_dict_1 = {
    #     'Node': ['x1','x2','x3', 'x4' , 'x5'],
    #     'output_labels':['a','a','b','c','c'],
    #     'output_prob': ['1','1','1','1','1'],
    #     'target':['x6','x7','x8','x9','x10'],
    # }
    #
    # data_dict_2 = {
    #     'Node': ['x11', 'x20', 'x30', 'x40', 'x50'],
    #     'output_labels': ['a', 'a', 'b', 'c', 'c'],
    #     'output_prob': ['1', '1', '1', '1', '1'],
    #     'target': ['x60', 'x70', 'x80', 'x90', 'x100'],
    # }

    # two transition systems with 10 nodes

    # data_dict_1 = {
    #     'Node': ['X' , 'X' , 'X' ,  'X1' ,  'X3'],
    #     'output_labels': ['a' , 'a' ,  'a' ,  'b' , 'b'],
    #     'output_prob': [0.3 , 0.3 ,  0.4 ,  1 ,  1],
    #     'target': ['X1' , 'X3' , 'X5' ,  'X2' ,  'X4'],
    # }
    #
    # data_dict_2 = {
    #     'Node': ['Y' ,  'Y' , 'Y1'] ,
    #     'output_prob': [0.6 , 0.4 ,  1 ],
    #     'output_labels': ['a' , 'a' ,  'b' ],
    #     'target': ['Y1','Y3', 'Y2'],
    # }

    # two transition systems with 50 nodes

    # data_dict_1 = {
    #       'Node': ["x1", "x1", "x2", "x2", "x3", "x3", "x4", "x5", "x5", "x6","x26",
    #       "x7", "x8", "x9", "x10", "x27", "x25", "x22", "x26", "x26"] ,
    # 'output_labels': ['a','a','c','b','o','o','p','b','m','b','k','p','q','e','e','a','x','f','o','k'],
    #  'output_prob': [0.6 , 0.4 , 1, 1, 0.3, 0.7, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 0.5],
    #     'target': ["x11", "x12", "x13", "x14", "x15", "x16", "x17", "x18", "x19",
    #      "x20", "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28", "x29", "x30"],
    # }
    #
    # data_dict_2 = {
    #     'Node': ["x31", "x47", "x48", "x48", "x32", "x40", "x41", "x32", "x33",
    #       "x32", "x33", "x34", "x35", "x50", "x45"] ,
    #     'output_labels': ['a','z','a','a','p','o','w','p','t','p','g','d','s','a','b'],
    #     'output_prob': [1,1,0.2,0.8,0.1,1,1,0.4,0.3,0.5,0.5,1,1,1,1],
    #     'target': ["x36", "x37", "x38", "x39", "x40", "x41", "x42", "x43", "x44",
    #       "x45", "x46", "x47", "x48", "x49", "x50"],
    # }

    # two transition systems with 100 nodes

    # data_dict_1 = {
    #       'Node': ["x1", "x1", "x2", "x2", "x3", "x3", "x4", "x5", "x5", "x6","x26",
    #       "x7","x8","x9","x10","x27","x25","x22","x26","x26","x51","x52","x53","x54",
    #       "x55","x56","x57","x58","x59", "x60", "x61", "x62", "x63", "x64", "x65"],
    #       'output_labels': ['a','a','c','b','o','o','p','b','m','b','k','p','q','e',
    #       'e','a','x','f','o','k','w','k','t','g','f','k','k','f','s','q','w','r','i','i', 'o'],
    # 'output_prob': [0.6,0.4,1,1,0.3,0.7,1,1,1,1,0.5,1,1,1,1,1,1,1,1,0.5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    #     'target': ["x11", "x12", "x13", "x14", "x15", "x16", "x17", "x18", "x19",
    #      "x20", "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28", "x29", "x30","x65",
    # "x66", "x67", "x68", "x69", "x70", "x71", "x72", "x73", "x74", "x75", "x76", "x77", "x78", "x79"],
    # }
    #
    # data_dict_2 = {
    #     'Node': ["x31","x47","x48","x48","x32","x40","x41", "x32", "x33",
    #      "x32","x33","x34","x35","x50","x45","x80","x81","x82","x83","x84","x85","x86","x87","x88","x89","x90","x91","x92","x93","x94","x109","x109"] ,
    #     'output_labels': ['a','z','a','a','p','o','w','p','t','p','g','d','s','a','b','b','w','s','b','i','b','q','o','i','a','c','a','b','e','c','c','c'],
    #     'output_prob': [1,1,0.2,0.8,0.1,1,1,0.4,0.3,0.5,0.5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.2,0.8],
    #     'target': ["x36", "x37", "x38", "x39", "x40", "x41", "x42", "x43", "x44",
    #       "x45","x46","x47","x48","x49","x50","x95","x96","x97","x98","x99","x100","x101","x102","x103","x104","x105","x106","x107","x108","x109","x107","x101"],
    # }

    # two transition systems with 150 nodes

    # data_dict_1 = {
    #       'Node': ["x1", "x1", "x2", "x2", "x3", "x3", "x4", "x5", "x5", "x6","x26",
    #       "x7","x8","x9","x10","x27","x25","x22","x26","x26","x51","x52","x53","x54",
    #       "x55","x56","x57","x58","x59", "x60", "x61", "x62", "x63", "x64", "x65","x300","x301","x302",
    #       "x303","x304","x305","x306","x307","x308","x309","x310","x311","x312","x313","x314"],
    #       'output_labels': ['a','a','c','b','o','o','p','b','m','b','k','p','q','e',
    #       'e','a','x','f','o','k','w','k','t','g','f','k','k','f','s','q','w','r','i','i','o','a','a','c','b','o','o','p','b','m','b','k','p','q','e',
    #       'e'],
    # 'output_prob': [0.6,0.4,1,1,0.3,0.7,1,1,1,1,0.5,1,1,1,1,1,1,1,1,0.5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    #     'target': ["x11", "x12", "x13", "x14", "x15", "x16", "x17", "x18", "x19",
    #      "x20", "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28", "x29", "x30","x65",
    #       "x66","x67","x68","x69","x70","x71","x72","x73","x74","x75","x76","x77","x78","x79","x315", "x316", "x317", "x318", "x319",
    #       "x320","x321","x322","x323","x324","x325","x326","x327","x328","x329"],
    # }
    #
    # data_dict_2 = {
    #     'Node': ["x31","x47","x48","x48","x32","x40","x41", "x32", "x33",
    #      "x32","x33","x34","x35","x50","x45","x80","x81","x82","x83","x84","x85","x86","x87",
    #      "x88","x89","x90","x91","x92","x93","x94","x109","x109","x315","x316","x317",
    #      "x318","x319","x320","x321","x322","x323","x324"] ,
    #     'output_labels': ['a','z','a','a','p','o','w','p','t','p','g','d','s','a','b','b','w',
    #      's','b','i','b','q','o','i','a','c','a','b','e','c','c','c','a','z','a','a','p','o','w','p','t','p'],
    #     'output_prob': [1,1,0.2,0.8,0.1,1,1,0.4,0.3,0.5,0.5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.2,0.8,1,1,1,1,1,1,1,1,1,1],
    #     'target': ["x36", "x37", "x38", "x39", "x40", "x41", "x42", "x43", "x44",
    #     "x45","x46","x47","x48","x49","x50","x95","x96","x97","x98","x99","x100","x101","x102","x103","x104","x105","x106",
    #     "x107","x108","x109","x107","x101","x325","x326","x327","x328","x329","x330","x331","x332","x333", "x334"],
    # }

    # two transition systems with 200 nodes

    # data_dict_1 = {
    #     'Node': ["x1", "x1", "x2", "x2", "x3", "x3", "x4", "x5", "x5", "x6", "x26",
    #              "x7", "x8", "x9", "x10", "x27", "x25", "x22", "x26", "x26", "x51", "x52", "x53", "x54",
    #              "x55", "x56", "x57", "x58", "x59", "x60", "x61", "x62", "x63", "x64", "x65", "x300", "x301", "x302",
    #              "x303", "x304", "x305", "x306", "x307", "x308", "x309", "x310", "x311", "x312", "x313", "x314", "x400",
    #              "x401", "x402", "x403", "x404", "x405", "x406", "x407", "x408", "x409", "x410", "x411", "x412", "x413", "x414", "x414"],
    #     'output_labels': ['a', 'a', 'c', 'b', 'o', 'o', 'p', 'b', 'm', 'b', 'k', 'p', 'q', 'e',
    #                       'e', 'a', 'x', 'f', 'o', 'k', 'w', 'k', 't', 'g', 'f', 'k', 'k', 'f', 's', 'q', 'w', 'r', 'i',
    #                       'i', 'o', 'a', 'a', 'c', 'b', 'o', 'o', 'p', 'b', 'm', 'b', 'k', 'p', 'q', 'e',
    #                       'e', 'x', 'f', 'o', 'k', 'w', 'k', 't', 'g', 'f', 'k', 'k', 'f', 's', 'q', 'w', 'w'],
    #     'output_prob': [0.6, 0.4, 1, 1, 0.3, 0.7, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 1, 1, 1, 1,
    #                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.3, 0.7],
    #     'target': ["x11", "x12", "x13", "x14", "x15", "x16", "x17", "x18", "x19",
    #                "x20", "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28", "x29", "x30", "x65",
    #                "x66", "x67", "x68", "x69", "x70", "x71", "x72", "x73", "x74", "x75", "x76", "x77", "x78", "x79",
    #                "x315","x316","x317", "x318","x319", "x320", "x321", "x322", "x323", "x324", "x325", "x326", "x327", "x328", "x329", "x415", "x416", "x417",
    #                "x418", "x419", "x420", "x421", "x422", "x423", "x424", "x425", "x426", "x427", "x428", "x429", "x327"],
    # }
    #
    #
    # data_dict_2 = {
    #     'Node': ["x31", "x47", "x48", "x48", "x32", "x40", "x41", "x32", "x33",
    #              "x32", "x33", "x34", "x35", "x50", "x45", "x80", "x81", "x82", "x83", "x84", "x85", "x86", "x87",
    #              "x88", "x89", "x90", "x91", "x92", "x93", "x94", "x109", "x109", "x315", "x316", "x317",
    #              "x318", "x319", "x320", "x321", "x322", "x323", "x324",  "x430", "x431", "x432", "x433", "x434", "x435", "x436", "x437", "x438", "x439","x439"],
    #     'output_labels': ['a', 'z', 'a', 'a', 'p', 'o', 'w', 'p', 't', 'p', 'g', 'd', 's', 'a', 'b', 'b', 'w',
    #                       's', 'b', 'i', 'b', 'q', 'o', 'i', 'a', 'c', 'a', 'b', 'e', 'c', 'c', 'c', 'a', 'z', 'a', 'a',
    #                       'p', 'o', 'w', 'p', 't', 'p','a', 'z', 'a', 'a','p', 'o', 'w', 'p', 't', 'p', 'p'],
    #     'output_prob': [1, 1, 0.2, 0.8, 0.1, 1, 1, 0.4, 0.3, 0.5, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    #                     1, 1, 1, 0.2, 0.8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 0.6, 0.4],
    #     'target': ["x36", "x37", "x38", "x39", "x40", "x41", "x42", "x43", "x44",
    #                "x45", "x46", "x47", "x48", "x49", "x50", "x95", "x96", "x97", "x98", "x99", "x100", "x101", "x102",
    #                "x103", "x104", "x105", "x106",
    #                "x107", "x108", "x109", "x107", "x101", "x325", "x326", "x327", "x328", "x329", "x330", "x331",
    #                "x332", "x333", "x334","x440", "x441", "x442", "x443", "x444", "x445", "x446", "x447", "x448", "x449", "x325"],
    # }

    # data_dict_1 ={
    #     'Node': ['x11', 'x12', 'x21', 'x23', 'x24', 'x25', 'x81', 'x91', 'x62', 'x43', 'x04', 'x35', 'x18', 'x17', 'x26', 'x35', 'x94', 'x25', 'x01', 'x21', 'x76', 'x98', 'x89', 'x87', 'x09', 'x100', 'x200', 'x300', 'x49', 'x59', 'x198', 'x981', 'x982', 'x093', 'x094', 'x095', 'x82', 'x81', 'x127', 'x876', 'x098', 'x589', 'x165', 'x09', 'x897', 'x42', 'x212', 'x675', 'x461', 'x121', 'x456', 'x0983', 'x7654', 'x5346'],
    #     'output_labels': ['a', 'a', 'b', 'b', 'c', 'c', 'a', 'a', 'b', 'b', 'c', 'c', 'a', 'a', 'b', 'b', 'c', 'c', 'a', 'a', 'b', 'b', 'c', 'c', 'a', 'a', 'b', 'b', 'c', 'c', 'a', 'a', 'b', 'b', 'c', 'c', 'a', 'a', 'b', 'b', 'c', 'c', 'a', 'a', 'b', 'b', 'c', 'c', 'a', 'a', 'b', 'b', 'c', 'c'],
    #     'output_prob': ['0.5', '0.5', '1', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '1'],
    #     'target': ['xn2', 'xx63', 'xp4', 'xm4', 'xk5', 'xml5', 'xpm2', 'xli3', 'xov4', 'xv4m', 'xkl5', 'xbn5', 'xmn2', 'xpo3', 'xkl4', 'xfd4', 'xxa5', 'xer5', 'xqw2', 'xyx3', 'xtz4', 'x4iu']
    # }

    # data_dict_2 = {
    #     'Node': ['yu1m', 'ybk2', 'yoc3', 'ypl3', 'yü4b', 'y1m', 'ylk2', 'ymo3', 'yp3', 'y4b', 'ym1m', 'yk2', 'yo3', 'ypm3', 'y4bj', 'yzx1m', 'xyk2', 'ypo3', 'ypuy3', 'ys4b', 'yu1m', 'ykz2', 'yo3', 'yp3', 'y4b', 'y1pm', 'yrk2', 'yow3', 'ypq3', 'y4eb', 'yx1m', 'yzk2', 'yon3', 'yüop3', 'y4b', 'y1m', 'yk2', 'yo3', 'yp3', 'y4b'],
    #     'output_labels': ['a', 'b', 'c', 'c', 'c', 'a', 'b', 'c', 'c', 'c', 'a', 'b', 'c', 'c', 'c', 'a', 'b', 'c', 'c', 'c', 'a', 'b', 'c', 'c', 'c', 'a', 'b', 'c', 'c', 'c', 'c', 'a', 'b', 'c', 'c', 'c'],
    #     'output_prob': ['1', '1', '0.5', '0.5', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '0.5', '0.5', '1', '1', '1', '1', '0.5', '0.5', '1'],
    #     'target': ['yi2', 'yn3', 'yj4', 'y5', 'yn4', 'yi2', 'yn3', 'yj4', 'y5', 'yn4', 'yi2', 'yn3', 'yj4', 'yo5', 'yn4', 'yi2', 'ybn3', 'yj4', 'y5', 'yn4', 'yi2', 'yn3', 'yj4', 'y5', 'yn4', 'yi2', 'ynp3', 'yj4', 'y5', 'yn4', 'yi2', 'yn3', 'ynj4', 'y5', 'yn4', 'yi2', 'yi2', 'yn3', 'yj4', 'y5', 'yn4', 'yi2']
    # }

    df1 = pd.DataFrame.from_dict(data_dict_1)

    df2 = pd.DataFrame.from_dict(data_dict_2)

    bisimilarity_test(df1, df2)
    # print(equivalence_classes_result)
    print('laufzeit')
