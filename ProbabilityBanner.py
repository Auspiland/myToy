import random

def NextCharacter(state,miss,pick,broken):
    if broken == 1:
        b_probability=0
        if miss <= 73:
            a_probability=0.006
        elif miss >= 90:
            a_probability=1
        else:
            a_probability=0.006+0.06*(miss-73)
    elif broken == 0:
        if miss <= 73:
            a_probability=0.003
            b_probability=0.003
        elif miss >= 90:
            a_probability=0.5
            b_probability=0.5
        else:
            a_probability=0.003+0.03*(miss-73)
            b_probability=0.003+0.03*(miss-73)
    else:
        raise ValueError("number of broken has an Error.")
    
    ticket = random.random()
    if ticket < a_probability:
        state = 'A'
        miss = 0
        pick += 1
        broken = 0
    elif ticket < a_probability+b_probability:
        state = 'B'
        miss = 0
        broken = 1
    else:
        state = 'C'
        miss +=1
    
    return state,miss,pick,broken

def NextWeapon(state,miss,pick,pick2,broken):
    if broken == 1:
        c_probability=0
        if pick2 >= 2:
            b_probability=0
            if miss <= 62:
                a_probability=0.007
            elif miss >= 77:
                a_probability=1
            else:
                a_probability=0.007+0.07*(miss-62)
        else:
            if miss <= 62:
                a_probability=0.0035
                b_probability=0.0035
            elif miss >= 77:
                a_probability=0.5
                b_probability=0.5
            else:
                a_probability=0.0035+0.035*(miss-62)
                b_probability=0.0035+0.035*(miss-62)
    elif broken == 0:
        if pick2 >= 2:
            b_probability=0
            if miss <= 62:
                a_probability=0.0035
                c_probability=0.0035
            elif miss >= 77:
                a_probability=0.5
                c_probability=0.5
            else:
                a_probability=0.0035+0.035*(miss-62)
                c_probability=0.0035+0.035*(miss-62)
        else:
            if miss <= 62:
                a_probability=0.00175
                b_probability=0.00175
                c_probability=0.0035
            elif miss >= 77:
                a_probability=0.25
                b_probability=0.25
                c_probability=0.5
            else:
                a_probability=0.00175+0.0175*(miss-62)
                b_probability=0.00175+0.0175*(miss-62)
                c_probability=0.0035+0.035*(miss-62)
        
    else:
        raise ValueError("number of broken has an Error.")
    
    ticket = random.random()
    if ticket < a_probability:
        state = 'A'
        miss = 0
        pick += 1
        pick2 = 0
        broken = 0
    elif ticket < a_probability+b_probability:
        state = 'B'
        miss = 0
        pick2 += 1
        broken = 0
    elif ticket < a_probability+b_probability+c_probability:
        state = 'C'
        miss = 0
        broken = 1
    else:
        state = 'F'
        miss += 1
    
    return state,miss,pick,pick2,broken

def Character(ticketNumber,goal,accuracy=20000,miss=0,broken=0):
    result=0
    for _ in range(accuracy):
        r=NextCharacter('C',miss,broken)
        for i in range(ticketNumber-1):
            r=NextCharacter(*r)
        if r[2]>goal-1:
            result +=1
    return 100*result/accuracy

def Weapon(ticketNumber,goal,accuracy=20000,miss=0,broken=0,pick2=0):
    result=0
    for _ in range(accuracy):
        r=NextWeapon('F',miss,0,pick2,broken)
        for i in range(ticketNumber-1):
            r=NextWeapon(*r)
        if r[2]>goal-1:
            result +=1
    return 100*result/accuracy

# Character function need parameters which are, first, (1)the number of ticket you have, second, (2)how many do you want.
# Additionally, you may have already gambled some pick up banners, or you would like to adjust the accuracy of result.
# Then, you can put more parameters in Character function.
# Such as number of (3)accuracy(20000 is default), (4)missed stack(number of consecutive 3or4 stars times), (5)whether you lost in 50/50.
# In weapon funtion, all the parameters are same but you can also put (6)the number of destiny-God's orbit(another weapon which is in banner but you don'y want)
# The result is expressed in percent(%).
print("Character pick up Probability is :",Character(100,1),"%")
print("Weapon pick up Probability is :",Weapon(300,1),"%")