import context
from framework.api.communication import APICommunicator
from framework.twitter_api import TwitterAPI

api = APICommunicator(TwitterAPI())

print(api.name)