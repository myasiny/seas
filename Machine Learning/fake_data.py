import time
import random

import collections

""""""
    #Exam: Time Spent by student
    #Question: Number of Compiling
    #Question: Time Spent by Student
    #Timestamp: Keystroke
    #Timestamp: Network Logs
    #Timestamp: Memory Logs

    ### {exam_id :
    #            {student_id :
    #                         [time_spent,
    #                         {question : number_of_compiling},
    #                         {question : time_spent},
    #                         {time : keystroke},
    #                         {time : network},
    #                         {time : memory}
    #                         ]
    #            }
    ### }
""""""

########################################################################################################################
def total_exam_time_per_std(total_timee):
    return random.randint(total_timee/2,total_timee)
########################################################################################################################
def question_over_num_of_comp(question_number):
    qonoc_dict = {}
    for i in range(1,question_number + 1):
        qonoc_dict["r_q_%s"%i] = random.randint(0,7)
    return qonoc_dict
########################################################################################################################
def irregular_rand(n, total):

    dividers = sorted(random.sample(xrange(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]
def regular_rand(n, _sum):
    mean = _sum / n
    variance = int(0.25 * mean)

    min_v = mean - variance
    max_v = mean + variance
    array = [min_v] * n

    diff = _sum - min_v * n
    while diff > 0:
        a = random.randint(0, n - 1)
        if array[a] >= max_v:
            continue
        array[a] += 1
        diff -= 1
    return array
def question_over_timespent(question_number,timespent,regular=True):
    qot_dict = {}
    if regular == True:
        timespents = regular_rand(question_number,timespent)
    else:
        timespents = irregular_rand(question_number,timespent)
    for i in range(1, question_number + 1):
        qot_dict["t_q_%s"%i] = timespents[i - 1]
    return qot_dict
########################################################################################################################
def memory_regular(reference):
    return reference + random.uniform(0,0.5)
def memory_irregular(reference):
    return reference + random.uniform(0,1.5)
def rand_memory(timee,reference,timespent,regular=True):
    mem_dict = {}
    for i in range(0,timespent*60+1,10):
        if regular == True:
            mem_dict[float(i) + timee] = memory_regular(reference)
        else:
            mem_dict[float(i) + timee] = memory_irregular(reference)
    return mem_dict
########################################################################################################################
def network_regular(reference):
    return reference + random.uniform(0,250000)
def network_irregular(reference):
    return reference + random.uniform(0,75000000)
def rand_network(timee,reference,timespent,regular=True):
    network_dict = {}
    for i in range(0,timespent*60+1,10):
        if regular == True:
            network_dict[float(i) + timee] = network_regular(reference)
        else:
            network_dict[float(i) + timee] = network_irregular(reference)
    return network_dict
########################################################################################################################
def keystroke_regular(reference):
    return reference + random.randint(0,30)
def keystroke_irregular(reference):
    return reference + random.randint(0,75)
def rand_keystroke(timee,reference,timespent,regular=True):
    keystroke_dict = {}
    for i in range(0,timespent*60+1,10):
        if regular == True:
            keystroke_dict[float(i) + timee] = keystroke_regular(reference)
        else:
            keystroke_dict[float(i) + timee] = keystroke_irregular(reference)
    return keystroke_dict
########################################################################################################################




def randomize(total_timee,question_count,starting_time,keystroke_reference,network_reference,memory_reference,regularity):
    ls = {}
    total_time = total_exam_time_per_std(total_timee)
    ls["total_time"] = (total_time)
    ls["num_of_comp"]=(question_over_num_of_comp(question_count))
    ls["time_spent"] =(question_over_timespent(question_count,total_time,regular=regularity))
    ls["keystroke"] =(rand_keystroke(starting_time,keystroke_reference,total_time,regular=regularity))
    ls["net_use"] =(rand_network(starting_time, network_reference, total_time,regular=regularity))
    ls["mem_use"] =(rand_memory(starting_time, memory_reference, total_time,regular=regularity))
    return ls

    ### {exam_id :
    #            {student_id :
    #                         [time_spent,
    #                         {question : number_of_compiling},
    #                         {question : time_spent},
    #                         {time : keystroke},
    #                         {time : network},
    #                         {time : memory}
    #                         ]
    #            }
    ### }


dict2 = {}



def generate(exam_id,student_count,total_exam_time,question_count,starting_time,keystroke_reference,network_reference,memory_reference):
    student_ids = list(range(0, student_count))
    dict1 = {}
    for i in student_ids:
        if i < len(student_ids)-len(student_ids)*0.05:
            dict1[i]= randomize(total_exam_time,question_count,starting_time,keystroke_reference,
                                         network_reference,memory_reference,regularity = True)

        else:
            dict1[i] = randomize(total_exam_time, question_count, starting_time, keystroke_reference,
                                            network_reference, memory_reference, regularity=False)
    dict2["exam_%s"%exam_id] = dict1


starting_time = 0

exam_ids = list(range(1, 101))
for exam_id in exam_ids:
    print "%"+str(exam_id)+" bitti."
    generate(exam_id,student_count = 100, total_exam_time = 120, question_count =10, starting_time= starting_time,
             keystroke_reference = 0, network_reference = 0, memory_reference = 5.0)


import json
with open("fakedata2.json","w") as f:
    json.dump(dict2,f)
print "Done"