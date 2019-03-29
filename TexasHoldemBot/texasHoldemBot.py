import os
import time
import re
from slackclient import SlackClient
from deck import Deck
from hand import Hand
from TexasHoldemGame import TexasHoldemGame

# CONSTANTS
GAME_STATE_INIT = 0
GAME_STATE_SET_BLINDS = 1
GAME_STATE_BETTING = 2
GAME_STATE_DRAWING = 3
GAME_STATE_END_OF_GAME = 4

class TexasHoldemBot:

    def __init__(self) : 
        self.slack_client = SlackClient(os.getenv('THBOT_SLACK_API'))
        self.starterbot_id = None
        self.RTM_READ_DELAY = 1
        
        ## Game related values
        self.game_state = GAME_STATE_INIT
        self.game = TexasHoldemGame()
        self.cur_player = 0

        ## Regular expression for a mention
        self.MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
        print("Instanced")

    def get_users_displayname(self,user_id):
        api_out = self.slack_client.api_call('users.list')
        if api_out["ok"] :
            for item in api_out['members'] :
                if item["id"] == user_id : 
                    print(item["real_name"])
                    return item["real_name"]
        return None

    def notify_user_to_play(self,channel):
        player_name = self.get_users_displayname(self.game.players[self.cur_player])
        strings = []
        # Print Current Bet
        strings.append("The current bet is at " + str(max(self.game.bets)))
        # Print status of the current player
        strings.append(player_name + ", it's your turn. Your current bet is at " + \
            str(self.game.bets[self.cur_player]) + " and you have " + \
            str(self.game.chips[self.cur_player] - self.game.bets[self.cur_player]) + \
            " chips at your disposal")
        for string_out in strings:
            self.slack_client.api_call(
                "chat.postMessage",
                channel=channel,
                text=string_out
            )
        # Print the users hand
        strings = []
        strings.append('Your current hand: ')
        strings.append(self.game.hands[self.cur_player].print_hand(2))
        if len(self.game.community_cards.card_nums) > 0 :
            strings.append('The community hand: ')
            strings.append(self.game.print_community_cards())
        for string_out in strings:
            self.slack_client.api_call(
                "chat.postEphemeral",
                channel=channel,
                text=string_out,
                user=self.game.players[self.cur_player]
            )
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
                    ## Non-command related functions
                    # Check if betting is done
                    if self.game_state == GAME_STATE_BETTING :
                        if self.game.check_betting_complete() :
                            self.game_state = GAME_STATE_DRAWING
                            # If everyone else folded, end the game
                            if self.game.players_active.count(True) == 1 :
                                self.game_state = GAME_STATE_END_OF_GAME
                        else : 
                            self.notify_user_to_play(channel)
                    # Set Blinds and initial player
                    if self.game_state == GAME_STATE_SET_BLINDS :
                        self.cur_player = 0
                        self.game_state = GAME_STATE_BETTING
                        self.notify_user_to_play(channel)
                    # Draw new card
                    if self.game_state == GAME_STATE_DRAWING : 
                        if len(self.game.community_cards.card_nums) < 5 :
                            self.game.add_community_card()
                            while len(self.game.community_cards.card_nums) < 3 :
                                self.game.add_community_card()
                            comm_string = self.game.print_community_cards()
                            print("Community" + comm_string)
                            # Notify players
                            self.slack_client.api_call(
                                "chat.postMessage",
                                channel=channel,
                                text=comm_string 
                            )                      
                            self.game_state = GAME_STATE_BETTING
                            self.notify_user_to_play(channel)
                        else :
                            self.game_state = GAME_STATE_END_OF_GAME
                    # Determine Winner
                    if self.game_state == GAME_STATE_END_OF_GAME :
                        # Show them hands
                        string_out = []
                        for i in range(len(self.game.players)):
                            if self.game.players_active[i] : 
                                player_name = self.get_users_displayname(self.game.players[i])
                                string_out.append(player_name + "'s hand: ")
                                string_out.append(self.game.hands[i].print_hand(2))
                        for string in string_out :
                            self.slack_client.api_call(
                                    "chat.postMessage",
                                    channel=channel,
                                    text=string
                                )                                            
                        winning_player_id, win_str = self.game.determine_winner()
                        player_name = self.get_users_displayname(winning_player_id)
                        win_str = player_name + win_str
                        # Check if chips are working
                        self.slack_client.api_call(
                            "chat.postMessage",
                            channel=channel,
                            text=win_str
                        )         
                        for player in self.game.players : 
                            n_chips = self.game.fetch_chips(player)
                            player_name = self.get_users_displayname(player)
                            chip_msf = player_name + " has " + str(n_chips) + " chips"            
                            self.slack_client.api_call(
                                "chat.postMessage",
                                channel=channel,
                                text=chip_msf 
                            )  
                        self.game_state = GAME_STATE_INIT
                        self.slack_client.api_call(
                            "channels.setTopic",
                            channel=channel,
                            topic="Waiting on players... :hourglass:"
                        )              

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
        
        # STATE INIT
        if self.game_state == GAME_STATE_INIT :

            # Join game
            if command.startswith("join"):
                res = self.game.add_player(user)
                user_name = self.get_users_displayname(user)
                if res == 1 :
                    response = "Welcome Aboard " + str(user_name) + "! :partyparrot:"
                    response_type = "public"
                else : 
                    response = "You are already playing..."
                    response_type = "public"

            # Leave Game
            if command.startswith("leave"):
                self.game.leave_game(user)
                response = "User has left the game"

            # Start Round
            if command.startswith("start"):
                if len(self.game.players) > 1 :
                    self.game.start_game()
                    response = "Let's begin"
                    response_type = "public"
                    self.game_state = GAME_STATE_SET_BLINDS
                    # Notify each player of their hand
                    for i in range(len(self.game.players)): 
                        private_response = "Your hand: "
                        private_response += self.game.hands[i].print_hand()
                        player = self.game.players[i]
                        self.slack_client.api_call(
                            "chat.postEphemeral",
                            channel=channel,
                            text=private_response,
                            user=player 
                        )
                    self.slack_client.api_call(
                        "channels.setTopic",
                        channel=channel,
                        topic="A game is in progress! :congaparrot::congaparrot::congaparrot::congaparrot:"
                    )      
                else : 
                    response = "Not enough players have joined yet."
        
        # State Betting
        if self.game_state == GAME_STATE_BETTING :
            responce_type = "public"
            # Check if user can actually play...
            if self.game.players_active[self.cur_player] == True and \
                self.game.all_in[self.cur_player] == False and \
                self.game.players[self.cur_player] == user:
                # Raising
                valid_command = False
                if command.startswith("raise ") :
                    raise_str = command[6:].strip()
                    if raise_str.isdigit() : 
                        res = self.game.raise_bet(self.game.players[self.cur_player],int(raise_str))
                        if res == 2 :
                            response = "Player is all in!"
                            valid_command = True
                        elif res == 1 :
                            response = "Current bet is set to " + str(max(self.game.bets))
                            valid_command = True
                    else : 
                        response = "... You can't raise '" + raise_str +"'"
                        
                # Calling
                if command.startswith("call"):
                    res = self.game.call(self.game.players[self.cur_player])
                    response = "Player calls."
                    valid_command = True
                # All In
                if command.startswith("all"):
                    self.game.go_all_in(self.game.players[self.cur_player])
                    response = "Player is all in!"
                    valid_command = True
                # Fold
                if command.startswith("fold"):
                    self.game.fold(self.game.players[self.cur_player])
                    response = "Player folds"
                    valid_command = True
                # Check
                if command.startswith("check"):
                    res = self.game.check(user)
                    response = "Player Checks"
                    if res == 1 : 
                        valid_command = True

                # Move onto next player after the current player makes a move
                if valid_command :
                    self.cur_player = ((self.cur_player+1)%len(self.game.players))
                    while self.game.players_active[self.cur_player] == False :
                        print(self.cur_player)

                    
    
        # Sends the response back to the channel
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )

    



