import time
import random
import datetime
import threading
import itertools
import numpy as np


'''
There are 98 letters, 2 players taking 7 letters each, and different number of rounds, depending on your time 
management. For every move each player can allocate up to x seconds of the total chosen time. The seconds 
allocated will be, whether used fully or not, subtracted from the the total time. Before allocating your 
time you will see your letters and the number of each n-letter words (2 <= n <= 7) that can be arranged.
'''


POINTS_VOWELS = {'A': 1, 'E': 1, 'I': 1, 'O': 1, 'U': 1}

POINTS_CONSONANTS = {'B': 3, 'C': 3, 'D': 2, 'F': 4, 'G': 2, 'H': 4, 'J': 8,
                     'K': 5, 'L': 1, 'M': 3, 'N': 1, 'P': 3, 'Q': 10, 'R': 1,
                     'S': 1, 'T': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}

POINTS_OF_LETTERS = POINTS_VOWELS | POINTS_CONSONANTS

all_letters = list('A' * 9 + 'B' * 2 + 'C' * 2 + 'D' * 4 + 'E' * 12 + 'F' * 2
                   + 'G' * 3 + 'H' * 2 + 'I' * 9 + 'J' * 1 + 'K' * 1 + 'L' * 4
                   + 'M' * 2 + 'N' * 6 + 'O' * 8 + 'P' * 2 + 'Q' * 1 + 'R' * 6
                   + 'S' * 4 + 'T' * 6 + 'U' * 4 + 'V' * 2 + 'W' * 2 + 'X' * 1
                   + 'Y' * 2 + 'Z' * 1)


seconds_for_player_1 = int(input('Type the number of seconds for Player 1: '))
seconds_for_player_2 = int(input('Type the number of seconds for Player 2: '))

while not seconds_for_player_1 == seconds_for_player_2:
    print('They both should have the same number of seconds.')
    seconds_for_player_1 = int(input('Type the number of seconds for Player 1: '))
    seconds_for_player_2 = int(input('Type the number of seconds for Player 2: '))


total_points_of_player_1 = 0
total_points_of_player_2 = 0


class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_string = False  # Because default blank node.


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        cur = self.root
        for c in word:
            if c not in cur.children:  # If not in hashmap's keys of the root node.
                cur.children[c] = TrieNode()
            cur = cur.children[c]
        cur.end_of_string = True

    def search(self, word):
        cur = self.root
        for c in word:
            if c not in cur.children:
                return False
            cur = cur.children[c]
        return cur.end_of_string


the_main_trie = Trie()

with open('scrabble_dictionary.txt') as f:
    mylist = f.read().splitlines()
    for word in mylist:
        the_main_trie.insert(word)


class Hand:
    size = 7

    def __init__(self):
        self.lists = [two_letter := [], three_letter := [], four_letter := [],
                      five_letter := [], six_letter := [], seven_letter := []]
        self.sample = random.sample(all_letters, Hand.size)
        for i in self.sample:
            all_letters.remove(i)

    def display_opportunities(self):
        permutations_from_sample = []
        poss_from_sample = set()
        for i in range(2, 8):
            permutations_from_sample.extend(list(itertools.permutations(self.sample, i)))
        for i in permutations_from_sample:
            s = ''.join(i)
            if the_main_trie.search(s):
                poss_from_sample.add(s)

        poss_from_sample = sorted(poss_from_sample, key=len)

        for i in poss_from_sample:
            if len(i) == 2:
                self.lists[0].append(i)
            elif len(i) == 3:
                self.lists[1].append(i)
            elif len(i) == 4:
                self.lists[2].append(i)
            elif len(i) == 5:
                self.lists[3].append(i)
            elif len(i) == 6:
                self.lists[4].append(i)
            elif len(i) == 7:
                self.lists[5].append(i)

        for i, j in enumerate(self.lists, 2):
            print(f'{len(j)}', end="\t ")
            print(f'~~~  {i}-letter words.')

        print(f'\t\t\t\t\t\t Your letters: {self.sample}.')

    def return_possibilities(self):
        flattened_possibilities = list(np.concatenate(self.lists))
        return flattened_possibilities


def first_task(x):
    x = datetime.timedelta(seconds=x)
    fut = datetime.datetime.now() + x
    while fut > datetime.datetime.now():
        time.sleep(1)
    exit_event.set()
    print("The time is over. Press Enter.")


def second_task(hand_possibilities, points_player1, points_player2):
    global total_points_of_player_1
    global total_points_of_player_2

    copy_hand_possibilities = hand_possibilities.copy()

    while True:
        if exit_event.is_set():
            break
        else:
            inp = input().upper()
            if not exit_event.is_set() and inp in hand_possibilities:
                print('Correct. (Flag is not set.)')

                if copy_hand_possibilities == h1.return_possibilities():
                    for i in inp:
                        print(POINTS_OF_LETTERS[i])
                        points_player1 += POINTS_OF_LETTERS[i]
                    print('POINTS of Player 1:', points_player1)

                if copy_hand_possibilities == h2.return_possibilities():
                    for i in inp:
                        print(POINTS_OF_LETTERS[i])
                        points_player2 += POINTS_OF_LETTERS[i]
                    print('POINTS of Player 2:', points_player2)

                hand_possibilities.remove(inp)
                # print(hand_possibilities)
            elif not exit_event.is_set() and inp not in hand_possibilities:
                print('Not correct. (Flag is not set.)')
            else:
                print()

    if copy_hand_possibilities == h1.return_possibilities():
        total_points_of_player_1 += points_player1

    elif copy_hand_possibilities == h2.return_possibilities():
        total_points_of_player_2 += points_player2


# The game starts below:


for_temp_points_1 = 0
for_temp_points_2 = 0


while len(all_letters) > 0 and (seconds_for_player_1 > 0 or seconds_for_player_2 > 0):
    print('Each player takes 7 letters.')
    print('First player move. You can make:')
    h1 = Hand()
    h2 = Hand()

    h1.display_opportunities()
    exit_event = threading.Event()
    print(f'\t\t\t\t\t\t ({seconds_for_player_1} seconds left.) Type how many '
          f'seconds you want to allocate for your move. Then press Enter.')
    your_seconds1 = int(input('Here: '))

    while your_seconds1 not in range(seconds_for_player_1 + 1):
        your_seconds1 = int(input('Please enter the correct number: '))

    seconds_for_player_1 -= your_seconds1
    thread1 = threading.Thread(target=first_task, args=(your_seconds1,))
    thread1.start()
    thread2 = threading.Thread(target=second_task, args=(h1.return_possibilities(), for_temp_points_1, for_temp_points_2))
    thread2.start()
    print(f'There is {len(all_letters)} left in the bag.')
    print(f'Type your words, then press Enter. You have {your_seconds1} seconds.')

    thread1.join()
    thread2.join()
    print(total_points_of_player_1, total_points_of_player_2)

    # Second player turn.

    print('Second player move. You can make:')

    h2.display_opportunities()
    exit_event = threading.Event()
    print(f'\t\t\t\t\t\t ({seconds_for_player_2} seconds left.) Type how many '
          f'seconds you want to allocate for your move. Then press Enter.')
    your_seconds2 = int(input('Here: '))

    while your_seconds2 not in range(seconds_for_player_2 + 1):
        your_seconds2 = int(input('Please enter the correct number: '))

    seconds_for_player_2 -= your_seconds2
    thread1 = threading.Thread(target=first_task, args=(your_seconds2,))
    thread1.start()
    thread2 = threading.Thread(target=second_task, args=(h2.return_possibilities(), for_temp_points_1, for_temp_points_2))
    thread2.start()
    print(f'There is {len(all_letters)} left in the bag.')
    print(f'Type your words, then press Enter. You have {your_seconds2} seconds.')

    thread1.join()
    thread2.join()
    print(total_points_of_player_1, total_points_of_player_2)

if total_points_of_player_1 > total_points_of_player_2:
    print(f'Player 1 wins {total_points_of_player_1} to {total_points_of_player_2} points.')
elif total_points_of_player_2 > total_points_of_player_1:
    print(f'Player 2 wins {total_points_of_player_2} to {total_points_of_player_1} points.')
else:
    print(f'DRAW. Both got {total_points_of_player_1} points.')

print('\n~~ THE END ~~')
