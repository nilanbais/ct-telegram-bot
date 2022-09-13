import context
from framework.api.communication import APICommunicator
from framework.twitter_api import TwitterAPI

api = APICommunicator(TwitterAPI())

#   'id': '22341856',
#   'name': 'IamNomad',
url = 'https://api.twitter.com/2/users/22341856/tweets'
header = {"User-Agent": "v2UserTweetsPython"}
qp =  {'tweet.fields': 'created_at'}

result = api.connect_to_endpoint(endpoint='user_tweets', header_kwargs=header, query_parameters_kwargs=qp, user_id=22341856)

print(result)