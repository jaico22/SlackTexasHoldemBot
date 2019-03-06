import os
import time
import re
from slackclient import SlackClient

class TexasHoldemBot:
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    starterbot_id = None
    RTM_READ_DELAY = 1
    EXAMPLE_COMMAND = "do"
    MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
    print("Instanced")

    def test_bot(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print("Starter Bot connected and running!")
            # Read bot's user ID by calling Web API method `auth.test`
            self.starterbot_id = self.slack_client.api_call("auth.test")["user_id"]
            print(self.starterbot_id)
            while True:
                command, channel = self.parse_bot_commands(self.slack_client.rtm_read())
                if command:
                    print(command)
                    self.handle_command(command, channel)
                time.sleep(self.RTM_READ_DELAY)
        else:
            print("Connection failed. Exception traceback printed above.")
        
    def parse_bot_commands(self,slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot commands.
            If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                user_id, message = self.parse_direct_mention(event["text"])
                print(user_id)
                print(self.starterbot_id)
                print(message)
                if user_id == self.starterbot_id:
                    print('That was toward me!!!')
                    return message, event["channel"]
        return None, None

    def parse_direct_mention(self,message_text):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(self.MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def handle_command(self,command, channel):
        """
            Executes bot command if the command is known
        """
        # Default response is help text for the user
        default_response = "Not sure what you mean. Try *{}*.".format(self.EXAMPLE_COMMAND)

        # Finds and executes the given command, filling in response
        response = None
        # This is where you start to implement more commands!
        if command.startswith(self.EXAMPLE_COMMAND):
            response = "Sure...write some more code then I can do that!"

        # Sends the response back to the channel
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )