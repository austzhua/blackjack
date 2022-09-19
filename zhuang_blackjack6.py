#!/usr/bin/env python3
'''
The task is to model the game of blackjack. The goal of the game is to beat the dealer by getting a count as close to 21 as possible, without going over 21. 

The dealer gives two cards face up to a player and one card face up and one card face down to themselves.

If a player's first two cards are an ace and a "ten-card" (a picture card or 10), giving a count of 21 in two cards, this is a natural or "blackjack." 

If the dealer's face-up card is a ten-card or an ace, they look at their face-down card to see if the two cards make a natural. 
If the face-up card is not a ten-card or an ace, they do not look at the face-down card until it is the dealer's turn to play.

Player’s turn
A player may either “stand” (not ask for another card) or “hit” (ask for another card) until they decide to stand on the total (if the total is less than 21) 
or they go “bust” (if the total is greater than 21). The dealer wins if the player goes bust.
Dealer’s turn
After the player’s turn is over, the dealer flips their face-down card. 
If their total is 17 or more, they must stand. If their total is 16 or less, they must take cards until their total is 17 or more, at which point the dealer must stand.
If a player's first two cards are of the same denomination, such as two jacks or two sixes, they may choose to treat them as two separate hands when their turn comes around. 
The player first plays the player_hand to their left by standing or hitting one or more times; only then is the player_hand to the right played. 
With a pair of aces, the player is given one card for each ace and may not draw again.

If the player gets a blackjack, they get 1.5 times the bet they wagered

If the player splits, they must wager amounts equal to the original bet on both hands.

The game will interact with the player using the command output and input() function.

Name: Austin Zhuang
Date: 12/17/20

Version 6
Adding the feedback given + improving splitting
'''

#imported modules
import random
import time
import math
#global variables
symbols = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
suits = [' of Hearts', ' of Diamonds', ' of Spades', ' of Clubs']
deck = {}
#populates deck
for suit in suits:
	for symbol in symbols:
		if type(symbol) == type(4):
			deck[str(symbol)+suit] = symbol
		elif symbol == 'Ace':
			deck[symbol+suit] = [1, 11]
		else:
			deck[symbol+suit] = 10
hit_responses = ['hit', 'Hit', 'h']
stand_responses = ['stand', 'Stand', 's']
yes_responses = ['yes', 'Yes', 'y', 'Y', 'YES']
no_responses = ['no', 'No', 'n', 'N', 'NO']

#functions

'''shuffle takes in a dictionary and rerounds a randomized version of the dictionary'''
def shuffle(deck):
	keys = list(deck.keys())
	random.shuffle(keys)
	shuffled_deck = {}
	for key in keys:
		shuffled_deck[key] = deck[key]
	return (shuffled_deck)

'''create_hand takes in a list with the cards and their values and rerounds a string with the names
of the cards printed out'''
def create_hand(hand):
	cards = ''
	if len(hand) == 1 and type(hand) == type([]):
		return hand[0][0]
	else:
		for i in range(len(hand)):
			if i == 0 and hand[i][0] != 'A':
				cards = cards + hand[i][0]
			elif i != 0 and hand[i][0] != 'A':
				cards = cards + '   ' + hand[i][0]
			else: 'nothing'
		return cards
new_deck = shuffle(deck)
player_hand = [new_deck.popitem(), new_deck.popitem()]
dealer_hand = [new_deck.popitem(), new_deck.popitem()]
player_total = 0
dealer_total = 0
player_display = create_hand(player_hand)
dealer_display = create_hand(dealer_hand)
money = 500
bet = 0
split_turn = False
high_score = money
rounds = 0

'''player_turn takes in the player and dealer's total, player's cards as a string and list and dealer's cards as a list, and a shuffled deck
and runs through one player turn'''
def player_turn():
	global new_deck 
	global player_hand 
	global dealer_hand 
	global player_total 
	global player_display 
	global money

	action = 0
	time.sleep(0.5)
	#catches the case if the player starts with a pair of aces
	if player_total > 21:
		player_hand.append(new_deck.popitem())
		if 'A' in player_hand[-1][0]:
			player_total = player_total + 11
			player_hand.insert(-1, 'A')
		else: player_total = player_total + deck[player_hand[-1][0]]
		player_hand.append(new_deck.popitem())
		if 'A' in player_hand[-1][0]:
			player_total = player_total + 11
			player_hand.insert(-1, 'A')
		else: player_total = player_total + deck[player_hand[-1][0]]
		player_display = create_hand(player_hand)
		while True:
			if 'A' in player_hand and player_total > 21:
				print("Player: {} ({})".format(player_display, player_total))
				time.sleep(0.5)
				print("Your ace becomes a 1 now.")
				time.sleep(0.5)
				player_hand.remove('A')
				player_total = player_total - 10
				continue
			elif player_total == 21:
				print("Player: {} ({})".format(player_display, player_total))
				time.sleep(0.5)
				print("You have 21!")
				time.sleep(0.5)
				return False
			else:
				return False

	while player_total < 21 and action not in stand_responses:
		print("Player: {} ({})".format(player_display, player_total))
		time.sleep(0.5)
		if 'A' in dealer_hand[0][0] and not split_turn: print("Dealer: {} ({})".format(dealer_hand[0][0], 11))
		elif 'A' not in dealer_hand[0][0] and not split_turn: print("Dealer: {} ({})".format(dealer_hand[0][0], dealer_hand[0][1]))
		else: print("Dealer: {} ({})".format(dealer_display, dealer_total))
		action = input("Do you want to hit or stand?\n--> ")
		if action in hit_responses:
			player_hand.append(new_deck.popitem())
			player_display = create_hand(player_hand)
			if 'A' in player_hand[-1][0]:
				player_total = player_total + 11
				player_hand.append('A')
			else: player_total = player_total + deck[player_hand[-1][0]]
			if player_total > 21 and 'A' not in player_hand:
				print("Player: {} ({})".format(player_display, player_total))
				time.sleep(0.5)
				print("Bust! You lose ${}.".format(bet))
				money = money - bet
				return True
			elif 'A' in player_hand and player_total > 21:
				print("Player: {} ({})".format(player_display, player_total))
				time.sleep(0.5)
				print("Your ace becomes a 1 now.")
				time.sleep(0.5)
				player_hand.remove('A')
				player_total = player_total - 10
				continue
			elif player_total == 21:
				print("Player: {} ({})".format(player_display, player_total))
				time.sleep(0.5)
				print("You have 21!")
				time.sleep(0.5)
				return False
			else: 
				continue
		elif action in stand_responses:
			return False
		else:
			print("Please respond hit or stand (h/s)")
			time.sleep(0.5)
	return 'nothing'

'''dealer_turn takes in the player and dealer's total, dealer's cards as a string and list, player's cards as a string, and a shuffled deck
and runs through one dealer turn'''
def dealer_turn():
	global new_deck 
	global dealer_hand 
	global player_total 
	global dealer_total 
	global player_display 
	global dealer_display
	global money

	print("Dealer's turn")
	time.sleep(0.5)
	while dealer_total <= player_total:
		print("Player: {} ({})".format(player_display, player_total))
		time.sleep(0.5)
		print("Dealer: {} ({})".format(dealer_display, dealer_total))
		time.sleep(0.5)
		if dealer_total >= 17 and dealer_total > player_total and dealer_total <= 21:
			print("Dealer has more! You lose ${}.".format(bet))
			money = money - bet
			return 'nothing'
		elif dealer_total >= 17 and dealer_total < player_total:
			if player_total == 21:
				print("You got blackjack! You win ${}.".format(math.floor(bet*1.5)))
				money = money + math.floor(bet*1.5)
			else: 
				print("You have more! You win ${}.".format(bet))
				money = money + bet
			return 'nothing'
		elif dealer_total < 17:
			dealer_hand.append(new_deck.popitem())
			if 'A' in dealer_hand[-1][0]:
				dealer_total = dealer_total + 11
				dealer_hand.insert(-1, 'A')
			else: dealer_total = dealer_total + deck[dealer_hand[-1][0]]
			dealer_display = create_hand(dealer_hand)
			print("The dealer is drawing a card...")
			time.sleep(1)
			print("Dealer: {} ({})".format(dealer_display, dealer_total))
			time.sleep(0.5)
			if dealer_total > 21:
				if 'A' not in dealer_hand:
					if player_total == 21:
						print("Dealer went bust and you have blackjack! You win ${}.".format(round(math.floor(bet*1.5))))
						money = money + round(math.floor(bet*1.5))
						return 'nothing'
					else:
						print("Dealer went bust! You win ${}.".format(bet))
						money = money + bet
						return 'nothing'
				else:
					print("Dealer's ace becomes a 1 now.")
					time.sleep(0.5)
					dealer_hand.remove('A')
					dealer_total = dealer_total - 10
					print("Dealer: {} ({})".format(dealer_display, dealer_total))
					time.sleep(0.5)
					continue
			elif dealer_total > player_total:
				print("Dealer has more! You lose ${}.".format(bet))
				money = money - bet
				return 'nothing'
			elif dealer_total == player_total and dealer_total >= 17:
				print("Push! You don't lose any money.")
				return 'nothing'
			else: continue
		elif dealer_total == player_total: 
			print("Push! You don't lose any money.")
			return 'nothing'
	#catches the case when the total of dealer_hand is already > than the total of player_hand
	else:
		if dealer_total > player_total and dealer_total <= 21:
			print("Player: {} ({})".format(player_display, player_total))
			time.sleep(0.5)
			print("Dealer: {} ({})".format(dealer_display, dealer_total))
			time.sleep(0.5)
			print("Dealer has more! You lose ${}.".format(bet))
			money = money - bet
		elif player_total == dealer_total and dealer_total <= 21:
			print("Player: {} ({})".format(player_display, player_total))
			time.sleep(0.5)
			print("Dealer: {} ({})".format(dealer_display, dealer_total))
			time.sleep(0.5)
			print("Push! You don't lose any money")
			return 'nothing'
		#catches the case if the dealer has two aces but never enters the loop because dealer_total > player_total
		else:
			print("Player: {} ({})".format(player_display, player_total))
			time.sleep(0.5)
			print("Dealer: {} ({})".format(dealer_display, 12))
			time.sleep(0.5)
			print('Dealer has more! You lose ${}.'.format(bet))
			return 'nothing'

'''blackjack_round models one round of blackjack'''
def blackjack_round():
	#shuffles deck and creates player_hand and dealer_hand
	global new_deck 
	global player_hand 
	global dealer_hand 
	global player_total 
	global dealer_total 
	global player_display 
	global dealer_display 
	global money
	global split_turn
	global high_score
	global rounds

	#finds the total of player_hand
	if 'A' in player_hand[0][0] and 'A' not in player_hand[1][0]:
		player_total = 11 + player_hand[1][1]
		player_hand.insert(-1, 'A')
	elif 'A' in player_hand[1][0] and 'A' not in player_hand[0][0]:
		player_total = player_hand[0][1] + 11
		player_hand.insert(-1, 'A')
	elif 'A' in player_hand[0][0] and 'A' in player_hand[1][0]:
		player_total = 22
		player_hand.insert(-1, 'A')
		player_hand.insert(-1, 'A')
	else: player_total = player_hand[0][1] + player_hand[1][1]
	
	#finds the total of dealer_hand
	if 'A' in dealer_hand[0][0] and 'A' not in dealer_hand[1][0]:
		dealer_total = 11 + dealer_hand[1][1]
		dealer_hand.insert(-1, 'A')
	elif 'A' in dealer_hand[1][0] and 'A' not in dealer_hand[0][0]:
		dealer_total = dealer_hand[0][1] + 11
		dealer_hand.insert(-1, 'A')
	elif 'A' in dealer_hand[0][0] and 'A' in dealer_hand[1][0]:
		dealer_total = 22
		dealer_hand.insert(-1, 'A')
		dealer_hand.insert(-1, 'A')
	else: dealer_total = dealer_hand[0][1] + dealer_hand[1][1]

	#checks if the dealer or the player has a natural (a count of 21)
	if 'A' in dealer_hand[0][0] or 'J' in dealer_hand[0][0] or 'Q' in dealer_hand[0][0] or 'K' in dealer_hand[0][0] or '10' in dealer_hand[0][0]:
		print("Player: {} ({})".format(player_display, player_total))
		if 'A' in dealer_hand[0][0]: print("Dealer: {} ({})".format(dealer_hand[0][0], 11))
		else: print("Dealer: {} ({})".format(dealer_hand[0][0], 10))
		time.sleep(0.5)
		print("Checking dealer's hand for blackjack...")
		time.sleep(1)
		if dealer_total < 21 and player_total < 21:
			print("The dealer does not have blackjack.")
			time.sleep(0.5)
		elif dealer_total == 21 and player_total < 21:
			print("Dealer: {} ({})".format(dealer_display, dealer_total))
			time.sleep(0.5)
			print("Dealer has blackjack! You lose ${}.".format(bet))
			money = money - bet
			rounds = rounds + 1
			return 'nothing'
		elif dealer_total == 21 and player_total == 21:
			print("Dealer: {} ({})".format(dealer_display, dealer_total)) 
			time.sleep(0.5)
			print("Both you and the dealer have blackjack. You don't lose any money")
			rounds = rounds + 1
			return 'nothing'
		elif dealer_total < 21 and player_total == 21:
			print("You have blackjack and the dealer does not. You win ${}.".format(math.floor(bet*1.5)))
			money = money + math.floor(bet*1.5)
			rounds = rounds + 1
			return 'nothing'
		elif dealer_total > 21:
			print("The dealer does not have blackjack")
			time.sleep(0.5)
		else: 'nothing'
	elif player_total == 21: 
		print("Player: {} ({})".format(player_display, player_total))
		time.sleep(0.5)
		print("Dealer: {} ({})".format(dealer_display, dealer_total))
		time.sleep(0.5)
		print("You have blackjack and the dealer does not. You win ${}.".format(round(math.floor(bet*1.5))))
		money = money + math.floor(bet*1.5)
		rounds = rounds + 1
		return 'nothing'
	else: 'nothing'

	#split case
	if player_hand[0][0][0] == player_hand[-1][0][0]:
		is_split = 0
		while is_split not in yes_responses:
			print("Player: {} ({})".format(player_display, player_total))
			if 'A' in dealer_hand[0][0]: print("Dealer: {} ({})".format(dealer_hand[0][0], 11))
			else: print("Dealer: {} ({})".format(dealer_hand[0][0], dealer_hand[0][1]))
			time.sleep(0.5)
			is_split = input("You have two cards of the same denomination. Do you want to split?\n--> ")
			if is_split in yes_responses and bet*2 <= money:
				if 'A' not in player_hand[0][0]:
					print("Okay, playing the first hand")
					time.sleep(0.5)
					player_hand1 = player_hand
					dealer_total1 = dealer_total
					dealer_display1 = dealer_display
					player_hand = [player_hand[0]]
					player_display = create_hand(player_hand)
					player_total = player_hand[0][1]
					if player_turn():
						split_turn = True
						print("Second hand")
						time.sleep(0.5)
						player_hand = [player_hand1[1]]
						player_display = create_hand(player_hand)
						player_total = player_hand1[0][1]
						if player_turn(): 
							rounds = rounds + 1
							return 'nothing'
						else: dealer_turn()
						if dealer_total > 21:
							if player_total == 21:
								print("You have blackjack! You win ${}.".format(math.floor(bet*1.5)))
								money = money + math.floor(bet*1.5)
							else:
								print("You win ${}.".format(bet))
								money = money + bet
						elif player_total < dealer_total:
							print("Player: {} ({})".format(player_display, player_total))
							time.sleep(0.5)
							print("Dealer: {} ({})".format(dealer_display, dealer_total))
							time.sleep(0.5)
							print("Dealer has more! You lose ${}.".format(bet))
							money = money - bet
						elif player_total > dealer_total:
							if player_total == 21:
								print("Player: {} ({})".format(player_display, player_total))
								time.sleep(0.5)
								print("Dealer: {} ({})".format(dealer_display, dealer_total))
								time.sleep(0.5)
								print("You have blackjack! You win ${}.".format(math.floor(bet*1.5)))
								money = money + math.floor(bet*1.5)
							else:
								print("Player: {} ({})".format(player_display, player_total))
								time.sleep(0.5)
								print("Dealer: {} ({})".format(dealer_display, dealer_total))
								time.sleep(0.5)
								print("You have more! You win ${}.".format(bet))
								money = money + bet
						else:
							print("Player: {} ({})".format(player_display, player_total))
							time.sleep(0.5)
							print("Dealer: {} ({})".format(dealer_display, dealer_total))
							time.sleep(0.5)
							print("Push. You don't lose any money")
						rounds = rounds + 1
						return 'nothing'
					else:
						dealer_total = dealer_total1
						dealer_display1 = dealer_display1
						dealer_turn()
						split_turn = True
						print("Second hand")
						time.sleep(0.5)
						player_hand = [player_hand1[1]]
						player_display = create_hand(player_hand)
						player_total = player_hand1[0][1]
						if player_turn(): 'nothing'
						elif dealer_total > 21:
							if player_total == 21:
								print("You have blackjack! You win ${}.".format(math.floor(bet*1.5)))
								money = money + math.floor(bet*1.5)
							else:
								print("You win math.floor(bet*1.5).".format(bet))
								money = money + bet
						elif player_total < dealer_total:
							print("Player: {} ({})".format(player_display, player_total))
							time.sleep(0.5)
							print("Dealer: {} ({})".format(dealer_display, dealer_total))
							time.sleep(0.5)
							print("Dealer has more! You lose .".format(bet))
							money = money - bet
						elif player_total > dealer_total:
							if player_total == 21:
								print("Player: {} ({})".format(player_display, player_total))
								time.sleep(0.5)
								print("Dealer: {} ({})".format(dealer_display, dealer_total))
								time.sleep(0.5)
								print("You have blackjack! You win ${}.".format(math.floor(bet*1.5)))
								money = money + math.floor(bet*1.5)
							else:
								print("Player: {} ({})".format(player_display, player_total))
								time.sleep(0.5)
								print("Dealer: {} ({})".format(dealer_display, dealer_total))
								time.sleep(0.5)
								print("You have more! You win ${}.".format(bet))
								money = money + bet
						else:
							print("Player: {} ({})".format(player_display, player_total))
							time.sleep(0.5)
							print("Dealer: {} ({})".format(dealer_display, dealer_total))
							time.sleep(0.5)
							print("Push. You don't lose any money")
						rounds = rounds + 1
						return 'nothing'
				else: continue
			elif is_split in no_responses:
				break
			elif bet*2 > money:
				print("You don't have enough money to split.")
				break
			else: print("Please respond yes or no (y/n)")
		#the ace case of splits
		else:
			print("You have two aces, so you will only recieve one card for each hand.")
			hand1 = [player_hand[0], new_deck.popitem()]
			hand2 = [player_hand[-1], new_deck.popitem()]
			time.sleep(0.5)
			dealer_total1 = dealer_total
			if 'A' in hand1[1][0]:
				player_total = 12
				player_display = create_hand(hand1)
				print("First hand")
				time.sleep(0.5)
				dealer_turn()
			else: 
				player_total = 11 + hand1[1][1]
				player_display = create_hand(hand1)
				print("First hand")
				time.sleep(0.5)
				dealer_turn()
			dealer_total = dealer_total1
			if 'A' in hand2[1][0]:
				player_total = 12
				player_display = create_hand(hand2)
				print("Second hand")
				time.sleep(0.5)
				dealer_turn()
			else: 
				player_total = 11 + hand2[1][1]
				player_display = create_hand(hand2)
				print("Second hand")
				time.sleep(0.5)
				dealer_turn()
			rounds = rounds + 1
			return 'nothing'

	#player's turn
	flag = player_turn()
	if flag: 'nothing'

	#dealer's turn
	else: dealer_turn()

	#updates highscore
	if money > high_score:high_score = money
	else: 'nothing'
	rounds = rounds + 1
	return 'nothing'
#main
#introduction
name = input("What is your name?\n--> ")
start = 0
start = input("Hi, {}, are you ready to play blackjack?\n--> ".format(name))
while True:
	if start in yes_responses:
		print("Okay, you have $500 to play with.")
		time.sleep(0.5)
		bet = input("How much money do you want to bet (must be at least $25 and at most $500)?\n--> ")
		if not bet.isdigit() or int(bet) < 25 or int(bet) > money:
			print("Please input a positive integer greater than or equal to 25 (e.g. 25, 26, 27, etc.) and less than or equal to 500.")
			time.sleep(0.5)
			continue
		else:
			print("Okay, dealing cards now...")
			bet = int(bet)
			time.sleep(1)
			blackjack_round()
			break
	elif start in no_responses: 
		print("Okay, I can wait 3 seconds...")
		time.sleep(3)
		print("Time's up!")
		start = input("Are you ready to play blackjack?\n--> ")
		continue
	else: 
		print("Please respond yes or no (y/n)")
		time.sleep(0.5)
		start = input("Are you ready to play blackjack?\n--> ")

#asks the player if they want to play again
play_again = 0
time.sleep(0.5)
while money > 0:
	if rounds == 1: print("You have ${} after 1 round.".format(money))
	else: print("You have ${} after {} rounds.".format(money, rounds))
	play_again = input("Do you want to play again?\n--> ")
	if play_again in yes_responses: 
		play_again = 0
		new_deck = shuffle(deck)
		player_hand = [new_deck.popitem(), new_deck.popitem()]
		dealer_hand = [new_deck.popitem(), new_deck.popitem()]
		player_total = 0
		dealer_total = 0
		player_display = create_hand(player_hand)
		dealer_display = create_hand(dealer_hand)
		split_turn = False
		if money <= 25:
			bet = money
			print("Okay, you are going all in (you have at most $25).")
			time.sleep(0.5)
			print("Dealing cards now...")
			time.sleep(1)
			blackjack_round()
			continue
		bet = input("Okay, how much do you want to bet (the bet must be at least $25 and at most ${})?\n--> ".format(money))
		if not bet.isdigit() or int(bet) < 25 or int(bet) > money:
			print("Please input a positive integer greater than 25 (e.g. 25, 26, 27, etc.) and less than {}".format(money))
			time.sleep(0.5)
			continue
		else:
			print("Okay, dealing cards now...")
			bet = int(bet)
			time.sleep(1)
			blackjack_round()
			continue
	elif play_again in no_responses: 
		print("Thanks for playing, {}!".format(name))
		time.sleep(0.5)
		if rounds == 1: print("The highest amount of money you accumulated was ${}, and you played 1 round.".format(high_score))
		else: print("The highest amount of money you accumulated was ${}, and you played {} rounds.".format(high_score, rounds))
		break
	else: 
		print("Please respond yes or no (y/n)")
		time.sleep(0.5)
		continue
else:
	print("You're all out of money, {}! Game over!".format(name))
	time.sleep(0.5)
	if rounds == 1: print("The highest amount of money you accumulated was ${}, and you played 1 round.".format(high_score))
	else: print("The highest amount of money you accumulated was ${}, and you played {} rounds.".format(high_score, rounds))