#!/usr/bin/env python3
import os
import random
import time

# PWMCT 5000
# inspired by: https://www.nytimes.com/2020/07/22/us/politics/trump-cognitive-test-results.html

words = ['person', 'woman', 'man', 'camera', 'tv']
nexts = ['And then...', 'Go on...', 'What else...', 'What’s next...', 'Continue...', 'Carry on...', 'Followed by...']
errors = ['Hmmm...', 'Uh...', 'What the...', 'Strange...', 'That’s odd...', 'Sure...', 'Weird...']
rewards = [
    'It’s actually tricky, but for you, kinda sorta easy!',
    'Alright, nobody gets it in order...',
    'That’s great, you’re like pretty smart. \nYou must have, like, a shuffled memory.'
    ]
perfects = [
    'It’s actually not that easy, but for you, it’s easy!',
    'Impressive, they said nobody gets it in order!',
    'That’s amazing. How did you do that? \nYou’re cognitively there!'
    ]
repeats = [
    'Give us that again. Can you do that again?',
    'Could you repeat that?',
    'How about one more time?',
    'Go back to that question and repeat ’em, can you do it?'
]
mistakes = [
    'Ouch, I mean — going to probably happen to all of us, right?',
    'Whoops, and, I say this with respect.',
    'Uh oh, something’s going on.',
    'Too bad, those last questions are much more difficult.'
]
fears = [
    'We know, nobody can do it.',
    'Don’t worry, others refuse to test.',
    'Yeah, smart brains don’t need to prove there smart!',
    'You should take that test, because something’s going on.'
]

rewardsStep = 0
total = 0.0
rows, columns = os.popen('stty size', 'r').read().split()
skipGame = False

# reset everything
def reset_game():
    global rewardsStep, fears, repeats, total, rows, columns, skipGame
    rows, columns = os.popen('stty size', 'r').read().split()
    random.shuffle(fears)
    random.shuffle(repeats)
    rewardsStep = 0
    total = 0.0
    skipGame = False
    clear()

# test your brain
def test_round():
    global total
    tempWords = words.copy()
    random.shuffle(nexts)
    tempNexts = nexts.copy()
    random.shuffle(errors)
    tempErrors = errors.copy()
    score = []

    for i in range(len(words)):
        tscore = 0.0
        # guess = input(str(i + 1) + ' - ').lower()
        guess = input().lower()
        if guess == '':
            break
        elif guess in tempWords:
            tempWords.remove(guess)
            tscore += 1
            if guess == words[i]:
                tscore += 1
            wait(.2)
            if i < len(words)-1:
                print()
                rc = random.choice(tempNexts)
                typewriter(rc)
                tempNexts.remove(rc)
        else:
            wait(.2)
            rc = random.choice(tempErrors)
            typewriter(rc)
            tempErrors.remove(rc)
        total += tscore
        score.append(tscore)

    return score

# check done playing
def winner():
    return rewardsStep == 3

# check perfect score
def checkPerfect():
    return total == 30

# nifty typing out effect
def typewriter(txt, lf = 1, t = .01):
    chars = list(txt)
    pc = ''
    for c in chars:
        print(c, end='', flush=True)
        if c == ' ' and pc in ['.', '!', '?']:
            wait(.5)
        wait(t)
        pc = c
    for i in range(lf):
        print()

# (w)ait
def wait(t = .2):
    time.sleep(t)

# breakline
def br(chr = '-'):
    print('\n'+ chr*int(columns))

# clear screen
def clear():
    for i in range(int(rows)):
        print()
        wait(.01)
    os.system('cls||clear')

# continue playing?
def ask():
    return input(' (y/n) ').lower() != 'n'

# kick off everything
while True:
    reset_game()
    tempRepeats = repeats.copy()

    br()
    typewriter('PWMCT 5000 – Some kind of a test... an acuity test?', 0)
    br()

    while True:
        typewriter('Begin cognitive test?', 0)
        if not ask():
            typewriter('\n' + random.choice(fears))
            skipGame = True
            break

        print()
        typewriter('I’ll give you five names and you have to repeat ’em.', 2)
        wait(.5)

        for w in words:
            print('\t• '+w)
            wait(0.5)
        print()

        typewriter('\t+ 2 : If you get it in order you get extra points!', 2)
        typewriter('\t+ 1 : If you repeat ’em out of order, it’s OK, \n\t      but, you know, it’s not as good.', 2)



        typewriter('Repeat ’em, can you do it?')

        # game time!
        while True:
            random.shuffle(mistakes)

            # check score to word count
            tscore = test_round()
            tsum = sum(tscore)

            if len(tscore) == len(words):
                clear()
                if tsum < 5:
                    typewriter(random.choice(mistakes))
                    break
                elif tsum == 10:
                    typewriter(perfects[rewardsStep])
                else:
                    typewriter(rewards[rewardsStep])

                if rewardsStep < 2:
                    rc = random.choice(tempRepeats)
                    print()
                    typewriter(rc)
                    tempRepeats.remove(rc)
            else:
                typewriter(random.choice(mistakes))
                break

            rewardsStep += 1
            wait(.5)

            if winner():
                break
        break

    cogReport = 'Loser'
    cogAdvice = 'Magically disappear.'
    cogScore = str(round(total)) + ' / 30'

    if checkPerfect():
        cogReport = 'Very Stable Genius'
        cogAdvice = 'Get on Twitter and brag about it!'
    elif winner():
        cogReport = 'Like Really Smart'
        cogAdvice = 'Nobody gets it in order...'
    else:
        cogReport = 'Dummy'
        cogAdvice = 'Take that test again, because something’s going on.'

    if not skipGame:
        print()
        br()
        typewriter('SCORE: ' + cogScore)
        typewriter('REPORT: ' + cogReport)
        typewriter('ADVICE: ' + cogAdvice)
        br()

        if checkPerfect():
            typewriter('The first few questions are easy, \nbut I’ll bet you couldn’t even answer the last five questions.')
        else:
            typewriter('I’ll bet you couldn’t even answer the last five questions. \nI’ll bet you couldn’t. \nThey get very hard, the last five questions.')

        print()
        typewriter('Test again?', 0)
    else:
        print()
        typewriter('Last call, take the test?', 0)

    if ask():
        continue
    else:
        break
br()
clear()