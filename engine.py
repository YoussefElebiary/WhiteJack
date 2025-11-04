from config import *
from cards import Cards

class Engine:
    def __init__(self, cards: Cards):
        self.cards = cards
        self.balance = 1000
        self.bet = 0
        self.deck = cards.build_deck()
        self.hands = []
        self.player_cards = []    # (RANK, SUIT)
        self.dealer_cards = []    # (RANK, SUIT)
        self.current_hand = 0
        self.in_round = False
        self.result = ""

    def start_round(self, bet: int):
        self.bet = bet
        # Get Bet
        if self.balance <= 0:
            self.result = "You lost all your money!"
            self.end_game(999)
            return
        if bet > self.balance:
            bet = self.balance
        self.balance -= bet

        # Initialize Variables
        self.is_player: bool = True
        self.player_cards = []
        self.dealer_cards = []
        if len(self.deck) < 15:
            self.deck = self.cards.build_deck()


        # Draw Starting Cards
        self.player_cards.append(self.deck.pop())
        self.player_cards.append(self.deck.pop())
        self.dealer_cards.append(self.deck.pop())
        self.dealer_cards.append(self.deck.pop())

        # Flip Dealer Card
        self.cards.flip_card(*self.dealer_cards[1])

        # Track Player Hands
        self.hands = [self.player_cards]
        self.current_hand = 0
        self.in_round = True
        self.result = ""

        # Track Scores
        player_score = Engine.hand_value(self.player_cards)
        dealer_score = Engine.hand_value(self.dealer_cards)

        # Check BlackJack
        if player_score == 21:
            self.cards.flip_card(*self.dealer_cards[1])
            if dealer_score == 21:
                self.result = "Push with BlackJacks!"
                self.end_game(0)
            else:
                self.result = "You win with a BlackJack!"
                self.end_game(1)

    def player_hit(self):
        if not self.in_round:
            return

        hand = self.hands[self.current_hand]
        hand.append(self.deck.pop())
        val = Engine.hand_value(hand)

        if val > 21:
            self.result = "Bust!"
            self.end_game(4)
        elif val == 21:
            self.player_stand()

    def player_stand(self):
        if not self.in_round:
            return
        
        if self.current_hand + 1 < len(self.hands):
            self.current_hand += 1
            return
        
        self.dealer_play()

    def player_double(self):
        if not self.in_round:
            return
        
        double_amount = min(self.bet, self.balance)
        self.bet += double_amount
        self.balance -= double_amount

        self.player_hit()
        self.player_stand()

    def player_split(self):
        hand = self.hands[self.current_hand]

        if len(hand) != 2 or hand[0][0] != hand[1][0]:
            return False
        if self.balance < self.bet:
            return False
        
        self.balance -= self.bet
        self.hands[self.current_hand] = [hand[0]]
        self.hands.insert(self.current_hand + 1, [hand[1]])
        
        self.hands[self.current_hand].append(self.deck.pop())
        self.hands[self.current_hand + 1].append(self.deck.pop())

    def dealer_play(self):
        self.cards.flip_card(*self.dealer_cards[1])

        val = Engine.hand_value(self.dealer_cards)

        while val < 17:
            self.dealer_cards.append(self.deck.pop())
            val = Engine.hand_value(self.dealer_cards)
        
        player_val = Engine.hand_value(self.hands[self.current_hand])

        if val > 21:
            self.result = "You Win! Dealer Bust!"
            self.end_game(3)
        elif val > player_val:
            self.result = "Dealer Wins!"
            self.end_game(5)
        elif val < player_val:
            self.result = "You Win!"
            self.end_game(3)
        else:
            self.result = "Push!"
            self.end_game(0)

    def end_game(self, end_code: int):
        """
        0: Push
        1: Natural
        2: 21
        3: win
        4: Bust
        5: Dealer Win
        999: Insufficient Funds
        """
        self.in_round = False

        if end_code == 1:
            self.balance += int(self.bet * 2.5)
        if end_code == 2 or end_code == 3:
            self.balance += self.bet * 2
        elif end_code == 0:
            self.balance += self.bet
        self.bet = 0

    @staticmethod
    def hand_value(hand):
        value = 0
        aces = 0
        for rank, _ in hand:
            if rank == 'ace':
                value += 11
                aces += 1
            else:
                value += SCORE[rank]
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value