"""
This file contains a script that runs a game that allows the user to specify two Twitter users,
load their tweets, then displays tweets randomly and asks the user to identify which user
tweeted each tweet. The game ends when the user runs out of their initial 3 lives.
@author Jacob Stallings
Last updated 9/25/20

Developed for Vanderbilt Change++ as part of the interview process
"""

import tweepy
import random
"""
get_tweets(screen_name)

Makes requests to the Twitter API to load the last 3200 tweets from the user specified by 
screen_name. Makes multiple requests because tweepy limits tweet counts to 200 per request.
Filters out tweets containing tags to other user or links to media.

Used Github user yanofsky's script as a starting point. 
Link: https://gist.github.com/yanofsky/5436496

@param screen_name  The twitter @username (NOT the display name) of the user whose tweets are
                    to be loaded.

@return a list holding all the user's tweets, filtered to exclude those containing tags
        or media links.
"""
def get_tweets(screen_name):
    alltweets = [] # all the tweets received from the api
    clean_tweets = [] # alltweets but those tagging users or containing media links
    try:
        new_tweets = api.user_timeline(screen_name=screen_name, 
                                        include_retweets=False, 
                                        tweet_mode='extended', 
                                        count=200)
    except tweepy.error.TweepError:
        print("Invalid username. Please restart.")
        exit(2)
        

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name, 
                                        include_retweets=False, 
                                        tweet_mode='extended', 
                                        count=200,
                                        max_id=oldest)

        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
                
    for tweet in alltweets:
        if ('@' not in tweet.full_text) and ('http' not in tweet.full_text):
            tweet.full_text = tweet.full_text.replace('&amp;', '&') # looks cleaner
            clean_tweets.append(tweet.full_text)

    # Return a list of text strings that represent tweets
    return clean_tweets

"""
display_random_tweet(user1, user2, user1_tweets, user2_tweets)

Displays a tweet randomly chosen from the filtered tweets from the two users.
Prompts the user for a response and handles accordingly.

@param user1        The username of the first user whose tweets are being used
@param user2        The username of the first user whose tweets are being used
@param user1_tweets The list of valid tweets to display from user1
@param user2_tweets The list of valid tweets to display from user2

@return True if the user guessed the correct user, False otherwise
"""
def display_random_tweet(user1, user2, user1_tweets, user2_tweets):
        user = random.randint(1,2)
        if user == 1:
            tweet_index = random.randint(0, len(user1_tweets) - 1)
            chosen_tweet = user1_tweets[tweet_index]
        else:
            tweet_index = random.randint(0, len(user2_tweets) - 1)
            chosen_tweet = user2_tweets[tweet_index]

        print('\nThe Tweet:\n')
        print(chosen_tweet)
        print()
        print('Who Tweeted this?')
        answer = input(f'Enter 1 for @{user1} or 2 for @{user2} (q to quit):  ')
        if user == 1 and answer == '1':
            print(f'\nYou got it! It was @{user1}.')
            return True
        elif user == 2 and answer == '2':
            print(f'\nYou got it! It was @{user2}.')
            return True
        elif user == 1 and answer == '2':
            print(f'\nOops! It was actually @{user1}!')
            return False
        elif user == 2 and answer == '1':
            print(f'\nTough cookie! It was @{user2}.')
            return False
        elif answer == 'q':
            exit(1)
        else:
            control = input('\nYou must input either 1 or 2! Press q to quit or any key to continue: ')
            if control == 'q':
                exit(1)
            else:
                display_random_tweet(user1,user2,user1_tweets,user2_tweets)
            print()

credentials = {'consumer_key': 'RQXfenrukpSK3KyyoBTuHOlkM',
                'consumer_secret': 'vvhr9BA3KI0XDXQCnniIWMoOJITi6LYukdRD1l8VbGDRHtptun',
                'access_token': '2255833898-skSRtlg0HhmrQDVkjoAyKqTiVPRe9rW28iJQZRJ',
                'access_token_secret': 'dQ0tsLkMwN8o9A5ZQundj6bilWfJnOmk6RVVBKTCC4G86'}

auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])

api = tweepy.API(auth)

# DRIVER
def main():
    lives = 3
    score = 0
    tweet_count = 0

    print('\n\nWelcome to Who Tweeted? Your job is to identify which of two users tweeted each tweet!\n\n')
    user1 = input('Enter the Twitter handle of the first user: @')
    user2 = input('Enter the Twitter handle of the second user: @')

    print(f'Loading @{user1}\'s tweets...')
    user1_tweets = get_tweets(user1)

    print(f'Loading @{user2}\'s tweets...')
    user2_tweets = get_tweets(user2)

    while len(user1_tweets) > 0 and len(user2_tweets) > 0 and lives > 0:
        if display_random_tweet(user1,user2, user1_tweets, user2_tweets):
            score += 1
        else:
            lives -= 1
            print('You have ' + str(lives) + ' lives remaining.')
        tweet_count += 1

    # If run out of lives or tweets
    print(f'\nGame over. You got {score} correct answers out of {tweet_count}!\n')
    exit(0)

if __name__ == "__main__":
    main()




        







