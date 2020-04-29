import datetime, subprocess
import settings

#tweetdata.datからツイートIDを取得
with open(settings.datapath) as f:
  l = f.readlines()
  readed_tweet_id = int(l[1])

#tweetdata.datの1行目をOpeningに変更
with open(settings.datapath, mode = 'w') as f:
  f.write('Opening\n' + str(readed_tweet_id))

latest_tweet_id = readed_tweet_id

#ツイート監視
try:
  #タイムラインチェック(自分にメンションされているもの)
  for mention in settings.api.mentions_timeline(since_id = readed_tweet_id):
    #送り主が管理者かつ、ツイートに"Activate"(settings.activate_sign)が含まれていたら起動
    tweet_id = mention.id
    target = mention.user.screen_name
    if target != settings.AdminID:
      continue
    tweet = mention.text
    if not(settings.activate_sign in tweet):
      continue

    latest_tweet_id = tweet_id
    for cmd in settings.start_cmds:
      subprocess.call(cmd.split())
    text =  '@' + settings.AdminID + ' 起動しますっての！(ㆁᴗㆁ✿) ' + str(datetime.datetime.now())
    settings.api.update_status(status = text, in_reply_to_status_id = tweet_id)
#エラーを吐いたらとりあえず管理者にツイート
except Exception as e:
  text =  '@' + settings.AdminID + 'at standby.py\n' + str(e) + ' at ' + str(datetime.datetime.now())
  settings.api.update_status(status = text)
#最後にtweetdata.datをClosingに
finally:
  with open(settings.datapath, mode = 'w') as f:
    f.write('Closing\n' + str(latest_tweet_id))