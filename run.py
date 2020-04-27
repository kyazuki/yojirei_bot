import sys, tweepy, datetime, subprocess, traceback
import settings
from sidecode import text_analysis

#多重起動しないように、tweetdata.datの文字列をチェック(1行目がOpeningなら既に実行中、Closingなら停止中)
#Openingなら終了、Closingなら2行目からツイートIDを取得
with open(settings.datapath) as f:
  l = f.readlines()
  if l[0] == 'Opening\n':
    sys.exit()
  else:
    readed_tweet_id = int(l[1])

#tweetdata.datの1行目をOpeningに変更
with open(settings.datapath, mode = 'w') as f:
  f.write('Opening\n' + str(readed_tweet_id))

latest_tweet_id = readed_tweet_id

#ツイート監視
try:
  loop = 0
  text = 'NoText'

  #タイムラインチェック(自分にメンションされているもの)
  for mention in settings.api.mentions_timeline(since_id = readed_tweet_id):
    tweet_id = mention.id
    tweet = mention.text
    target = mention.user.screen_name
    if target == settings.MyID:
      continue
    elif target == settings.AdminID and settings.activate_sign in tweet:
      continue
    
    #ツイート分析
    text = '@' + target + ' '
    try:
      mode = text_analysis.mode_analysis(tweet)
      text += text_analysis.execute(mode, tweet)
    except text_analysis.callMultiCommandsError:
      #重複の場合
      text += '複数の処理は一度に実行不可ですっての…(ㆁxㆁ✿)\n分けてお願いしますっての！'
    except text_analysis.commandSyntaxError:
      if mode == 1: text += '形式が不正ですっての…(ㆁxㆁ✿)\n例:1:\"見出し(ひらがな)\",2:\"用字例表記\",3:\"解説\"を追加'
      elif mode == 2: text += '形式が不正ですっての…(ㆁxㆁ✿)\n例:\"削除対象(ひらがな)\"を削除'
      else: text += '形式が不正ですっての…(ㆁxㆁ✿)\n例:1:\"見出し(ひらがな)\",2:\"用字例表記\",3:\"解説\"に更新'
    
    #リプライ
    settings.api.update_status(status = text, in_reply_to_status_id = tweet_id)
    
    text = 'NoText'
    if loop == 0:
      latest_tweet_id = tweet_id
      loop = 1
#エラーを吐いたらとりあえず管理者にツイート
except tweepy.error.TweepError as e:
  text =  '@' + settings.AdminID + ' ' + traceback.format_exc() + ' at ' + str(datetime.datetime.now()) + '\nto:' + text[1:]
  settings.api.update_status(status = text)
except Exception as e:
  print(e)
  text =  '@' + settings.AdminID + ' ' + traceback.format_exc() + ' at ' + str(datetime.datetime.now())
  settings.api.update_status(status = text)
  settings.api.update_profile(name = settings.profile_name_error, description = settings.profile_description_error)
  with open(settings.errorpath, mode = 'w') as f:
    f.write(readed_tweet_id + '\n' + tweet_id)
  with open(settings.cronpath, mode = 'w') as f:
    f.write('#error * * * * * for i in `seq 0 10 59`;do (sleep ${i}; cd /home/twitter/www/yojirei_bot/repository; python3.6 run.py) & done;\n* * * * * (cd /home/twitter/www/yojirei_bot/repository; python3.6 standby.py) &\n')
  for cmd in settings.cron_cmds:
    subprocess.call(cmd.split())
#最後にtweetdata.datをClosingに
finally:
  with open(settings.datapath, mode = 'w') as f:
    f.write('Closing\n' + str(latest_tweet_id))