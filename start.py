import subprocess

from twitter_auth import api
import settings

#Twitterプロフィールを稼働中に更新
api.update_profile(name = settings.profile_name, description = settings.profile_description)

#cronを編集し、通常モードに設定
with open(settings.cronpath, mode = 'w') as f:
  f.write('* * * * * for i in `seq 0 10 59`;do (sleep ${i}; cd /home/twitter/www/yojirei_bot/repository; /usr/local/bin/python3.8 run.py) & done;\n#* * * * * (cd /home/twitter/www/yojirei_bot/repository; /usr/local/bin/python3.8 standby.py) &\n')
for cmd in settings.cron_cmds:
  subprocess.call(cmd.split())