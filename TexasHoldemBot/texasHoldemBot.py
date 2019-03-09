import os
import time
import re
from slackclient import SlackClient
from deck import Deck
from hand import Hand

class TexasHoldemBot:
    
    def __init__(self) : 
        self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
        self.starterbot_id = None
        self.RTM_READ_DELAY = 1
        
        ## Game related values
        self.players = []
        self.hands   = []
        self.bets    = []
        
        ## Deck Related values
        self.deck = Deck()
        self.community_cards = []

        ## Poker Related Values
        self.current_bet = 0
        
        ## State Machine Related values
        self.game_state = 0
        self.current_player = 0

        # State Definitions
        self.STATE_WAITING_ON_PLAYERS = 0 
        self.STATE_BETTING = 1

        ## Commands
        self.COMMAND_RAISE = "Raise "
        self.COMMAND_START_GAME = "Start"
        self.COMMAND_END_GAME = "End Game"
        self.COMMAND_JOIN_GAME = "Join"
        
        ## Regular expression for a mention
        self.MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
        print("Instanced")

    def test_bot(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print("Starter Bot connected and running!")
            # Read bot's user ID by calling Web API method `auth.test`
            self.starterbot_id = self.slack_client.api_call("auth.test")["user_id"]
            print(self.starterbot_id)
            while True:
                command, channel, user = self.parse_bot_commands(self.slack_client.rtm_read())
                if command:
                    print(command)
                    self.handle_command(command, user, channel)
                time.sleep(self.RTM_READ_DELAY)
        else:
            print("Connection failed. Exception traceback printed above.")
        
    def parse_bot_commands(self,slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot commands.
            If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.
        """
        user = None
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                print("User: " + event["user"])
                user_id, message = self.parse_direct_mention(event["text"])
                print(message)
                if user_id == self.starterbot_id:
                    print('That was toward me!!!')
                    return message, event["channel"], event["user"]
        return None, None, None

    def parse_direct_mention(self,message_text):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(self.MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def handle_command(self, command, user, channel):
        """
            Executes bot command if the command is known
        """
        # Default response is help text for the user
        default_response = "Not sure what you mean"

        # Finds and executes the given command, filling in response
        response = None
        
        # Increment bet
        if command.startswith(self.COMMAND_RAISE):
            amnt_to_raise = int(command[5:])
            self.current_bet += amnt_to_raise
            response = "USER raises by " + str(amnt_to_raise) + ". Current Bet: " + str(self.current_bet)
        
        # Join game
        if command.startswith(self.COMMAND_JOIN_GAME):
            response = self.join_game(user)

        # Start Round
        if command.startswith(self.COMMAND_START_GAME):
            response = self.start_game(channel)
            
        # Sends the response back to the channel
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )

    def add_common_card(self,channel):
        # Draw Card
        num, suit = self.deck.draw()

    def start_game(self,channel):
        # Shuffle the deck
        self.deck.shuffleCards()
        response = "Betting has commenced!"
        # Deal two cards per each player
        for i in range(len(self.players)) :
            # First Card
            num, suit = self.deck.draw()
            self.hands[i].add_card(num,suit)
            # Second Card
            num, suit = self.deck.draw()
            self.hands[i].add_card(num,suit)
            # Notify User what their hand is
            ephemeral_responce = self.hands[i].print_hand()
            self.slack_client.api_call(
                "chat.postEphemeral",
                channel=channel,
                text=ephemeral_responce,
                user=self.players[i]
            )
        return response

    def join_game(self,user):
        '''
            Checks if game hasn't started and adds 'user' to list of players if he's not already playing
        '''
        if self.game_state == self.STATE_WAITING_ON_PLAYERS :
            user_not_playing = True
            for player in self.players :
                if player == user :
                    user_not_playing = False
                    break
            if user_not_playing == True :
                # Add User to list of players and create a corresponding value for bet and hand
                self.players.append(user)
                self.hands.append(Hand())
                self.bets.append(0)
                response = "USER has joined the game!"
            else :
                response = "User is already in the game..."
        else :
            response = "Sorry, the game has already started..."
        return response