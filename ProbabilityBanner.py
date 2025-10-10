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
        r=NextCharacter('C',miss,0,broken)
        for i in range(ticketNumber-1):
            r=NextCharacter(*r)
        if r[2]>goal-1:
            result +=1
    print("Character {}pick up {}success Probability is :".format(ticketNumber,goal),100*result/accuracy,"%")

def Weapon(ticketNumber,goal,accuracy=20000,miss=0,broken=0,pick2=0):
    result=0
    for _ in range(accuracy):
        r=NextWeapon('F',miss,0,pick2,broken)
        for i in range(ticketNumber-1):
            r=NextWeapon(*r)
        if r[2]>goal-1:
            result +=1
    print("Weapon {}pick up {}success Probability is :".format(ticketNumber,goal),100*result/accuracy,"%")

# Character function need parameters which are, first, (1)the number of ticket you have, second, (2)how many do you want.
# Additionally, you may have already gambled some pick up banners, or you would like to adjust the accuracy of result.
# Then, you can put more parameters in Character function.
# Such as number of (3)accuracy(20000 is default), (4)missed stack(number of consecutive 3or4 stars times), (5)whether you lost in 50/50(If you lost, enter 1).
# In weapon funtion, all the parameters are same but you can also put (6)the number of destiny-God's orbit(another weapon which is in banner but you don'y want)
# The result is expressed in percent(%) and the result has small error range, because the method is numerical.
# 캐릭터 함수랑 무기 함수에 인수를 집어 넣으면 확률값이 퍼센트(%)로 도출됩니다. 계산은 Numerical한 방법으로 진행되기에 정확도에 따라 오차가 있을 수 있습니다.
# 필수적으로 입력할 인수는 1.돌릴 뽑기(기원)수, 2.뽑고 싶은 목표 개수 입니다.
# 추가적으로 입력할 수 있는것은 3.정확도 숫자(높을 수록 오래걸리지만 정확해집니다. 기본은 20000번), 4.스택 개수(5성 안나온 횟수), 5.픽뚫여부(확천이면 1, 반천이면 0)
# 무기 함수에는 마지막으로 6.운명-신이 정한 궤도 횟수 넣을 수 있습니다.

# Example
Character(320,3)
Weapon(100,1)
