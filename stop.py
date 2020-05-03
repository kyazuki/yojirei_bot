import subprocess

from twitter_auth import api
import settings

#Twitterプロフィールを停止中に更新
api.update_profile(name = settings.profile_name_stop, description = settings.profile_description_stop)

#cronを編集し、待機モードに設定
with open(settings.cronpath, mode = 'w') as f:
  f.write('#* * * * * for i in `seq 0 10 59`;do (sleep ${i}; cd /home/twitter/www/yojirei_bot/repository; /usr/local/bin/python3.8 run.py) & done;\n* * * * * (cd /home/twitter/www/yojirei_bot/repository; /usr/local/bin/python3.8 standby.py) &\n')
for cmd in settings.cron_cmds:
  subprocess.call(cmd.split())
