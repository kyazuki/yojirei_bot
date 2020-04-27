import sys, os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

def main():
  #"共有フォルダ/09.その他/用事例Botソースコードバックアップ"のフォルダID(URLの末端文字列)
  folder_id = '15UKHzghktHw2gigRtq5zOh54LlBECOOd'
  sub_folder_id = '1QFMD6SDeqQYnIpumCPUj8-KUMjVsOrWN'
  #ListFileメソッドでファイル種別を指定するための工夫。"folder_id"で指定したフォルダ内かつ、削除されていないファイルのみを抽出する
  query = "'{}' in parents and trashed=false".format(folder_id)

  file_list = drive.ListFile({'q': query}).GetList()

  args = sys.argv
  if len(args) <= 1:
    print('ファイル名が必要です', file=sys.stderr)
  elif len(args) > 2:
    print('不正な引数です。使用法: refresh.py [ファイル名]', file=sys.stderr)
  else:
    if args[1] == 'all':
      dl_files('./', folder_id)
    else:
      query = "'{0}' in parents and title contains '{1}' and trashed=false".format(folder_id, args[1])
      file_list = drive.ListFile({'q': query}).GetList()
      isSubfolder = False
      if len(file_list) == 0:
        query = "'{0}' in parents and title contains '{1}' and trashed=false".format(sub_folder_id, args[1])
        file_list = drive.ListFile({'q': query}).GetList()
        isSubfolder = True
      
      if len(file_list) != 1:
        print('そのファイルは存在しません')
      else:
        filename = file_list[0]['title']
        file_list[0].GetContentFile(filename if not isSubfolder else 'sidecode/' + filename)
        print("Downloaded: " + filename)
    

def dl_files(save_folder, drive_folder_id):
  query = "'{}' in parents and trashed=false".format(drive_folder_id)

  file_list = drive.ListFile({'q': query}).GetList()
  for f in file_list:
    # mimeTypeでフォルダか判別
    if f['mimeType'] == 'application/vnd.google-apps.folder':
      dl_files(os.path.join(save_folder, f['title']), f['id'])
    elif ".py" in f['title']:
      f.GetContentFile(os.path.join(save_folder, f['title']))
      print("Downloaded: " + f['title'])

main()