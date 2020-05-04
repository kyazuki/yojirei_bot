# -*- coding: utf-8 -*-
import subprocess

from twitter_auth import api
import settings

#Twitterプロフィールを稼働中に更新
api.update_profile(name = settings.profile_name, description = settings.profile_description)

#cronを編集し、通常モードに設定
with open(settings.cronpath, mode = 'w') as f:
  f.write('* * * * * for i in `seq 0 10 59`;do (sleep ${i}; /home/twitter/www/yojirei_bot/run.sh) & done;\n#* * * * * /home/twitter/www/yojirei_bot/standby.sh &\n')
for cmd in settings.cron_cmds:
  subprocess.call(cmd.split())