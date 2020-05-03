#直近でチェックしたツイートのIDを保存するファイルパス
datapath = 'tweetdata.dat'

errorpath = 'error.dat'
cronpath = 'cron.txt'
cron_cmds = ['crontab ' + cronpath, 'sudo systemctl restart crond.service']
start_cmds = ['cd /home/twitter/www/yojirei_bot/repository', 'python start.py']

#自分自身(この用字例Bot)のTwitterID
MyID = 'yojirei_bot_kai'
#手動版(手動版の用字例Bot)のTwitterID
ManualBotID = 'yojirei_bot'
#管理者のTwitterID(エラー送信用)
AdminID = 'kyazuki_maru'

#起動コード
activate_sign = 'Activate'

#稼働中のプロフィール名と説明文
profile_name = '用字例bot(自動) 稼働中！'
profile_description = '用字例を自動で応答しますっての！(ㆁᴗㆁ✿) 使い方は固定ツイートのスレッドをみてね 手動版@' + ManualBotID + ' 管理者@' + AdminID

#メンテ中のプロフィール名と説明文
profile_name_error = '用字例bot(自動) メンテ中...'
profile_description_error = '※ただいまメンテナンス中です※ 用字例を自動で応答しますっての！(ㆁᴗㆁ✿) 使い方は固定ツイートのスレッドをみてね 手動版@' + ManualBotID + ' 管理者@' + AdminID

#停止中のプロフィール名と説明文
profile_name_stop = '用字例bot(自動) 停止中...'
profile_description_stop = '※ただいま停止中です※ 用字例を自動で応答しますっての！(ㆁᴗㆁ✿) 使い方は固定ツイートのスレッドをみてね 手動版@' + ManualBotID + ' 管理者@' + AdminID
