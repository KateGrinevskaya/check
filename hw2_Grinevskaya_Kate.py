from itertools import permutations
from graphviz import Digraph

dot = Digraph()

# пузырьком
def bubble(my_list):
    if len(my_list) <= 1:
       return my_list
    for i in range(len(my_list)-1):
        for j in range(len(my_list)-i-1):
            if my_list[j+1] < my_list[j]:
                my_list[j], my_list[j+1] = my_list[j+1], my_list[j]
    return my_list

# быстрая сортировка
def quicksort(my_list):
   if len(my_list) <= 1:
       return my_list
   else:
       q = my_list[len(my_list) // 2]
   l_nums = [n for n in my_list if n < q]
 
   e_nums = [q] * my_list.count(q)
   b_nums = [n for n in my_list if q < n]
   return quicksort(l_nums) + e_nums + quicksort(b_nums)

# класс, запоминающий сравнения
class Preparing:
    def __init__(self, x, id, history):
        self.x = x
        self.id = id
        self.history = history
    def __lt__(self, other):
        self.history.append([self.id, other.id, self.x < other.x])
        return self.x < other.x
    
# сортировка одной последовательности
def one_seq_sort(sort_method, seq):
    sorted_l = []
    prepared_l = []
    history = []
    for el in seq:
        el = Preparing(el, seq.index(el), history)
        prepared_l.append(el)
    if sort_method == 'bubble':
        sorted_l = [el.x for el in bubble(prepared_l)]
    elif sort_method == 'quicksort':
        sorted_l = [el.x for el in quicksort(prepared_l)]
    else:
        sorted_l = [el.x for el in sorted(prepared_l)]
    return history

# получаю все возможные перестановки длинны, заданной пользователем
def get_all_seq(l):
    return permutations(list(range(0, l)), l)

# получаю все сравнения и их результаты для всех возможных
# последовательностей
def get_history(sort_method, l):
    hist = []
    all_seq = get_all_seq(l)
    for seq in all_seq:
        hist.append(one_seq_sort(sort_method, seq))
    return hist

# функция,которая строит график
def get_graph(all_histories):
    for h in all_histories:
        i = 0
        while i < len(h)-1:
            if i>0:
                dot.node('%s %s < %s' % (i+1, h[i+1][0], h[i+1][1]),\
                        '%s < %s' % (h[i+1][0], h[i+1][1]))
                dot.edge('%s %s < %s' % (i, h[i][0], h[i][1]),\
                        '%s %s < %s' % (i+1, h[i+1][0], h[i+1][1]),\
                        label = str(h[i][2]))
            elif i==0:
                dot.node('%s < %s' % (h[i][0], h[i][1]),\
                        '%s < %s' % (h[i][0], h[i][1]))
                dot.node('%s %s < %s' % (i+1, h[i+1][0], h[i+1][1]),\
                        '%s < %s' % (h[i+1][0], h[i+1][1]))
                dot.edge('%s < %s' % (h[i][0], h[i][1]),\
                        '%s %s < %s' % (i+1, h[i+1][0], h[i+1][1]),\
                        label = str(h[i][2]))

            i += 1
            if i == len(h)-1:
                dot.node('done', 'done')
                dot.edge('%s %s < %s' % (i, h[i][0], h[i][1]), 'done')
    with open('dot_code.dot', 'w') as fh:
        fh.write(dot.source)
    dot.render('check.png')
    return fh

#функция, которая сделает всё
def i_will_do_all():
    sort_method = str(input('Введите название сортировки(bubble/sorted/quicksort): '))
    l = int(input('Введите длинну последовательности: '))
    if l<=1:
        print('Аккуратно! Для такой длины не получится сделать дерево!')
    else:
        all_histories = get_history(sort_method, l)
        fh = get_graph(all_histories)

if __name__ == "__main__":
    final_file = i_will_do_all()
