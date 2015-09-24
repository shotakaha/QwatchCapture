==================================================
ちょっと詳しいこと
==================================================


画像のキャプチャ
--------------------------------------------------

- ウェブカメラ内に保存されている画像を :command:`wget` を使って取得
- 画像のURLは http://www.ispyconnect.com/man.aspx?n=IO+Data で調べた
- 右上の検索ボックスに型番とか入れるとたぶん見つかる
- 取得した画像は、その時の時刻でリネーム

.. code-block:: bash

   $ wget --http-user=USER --http-password=PASS http://QwatchIPADDRESS/snapshot.jpg
   $ mv snapshot.jpg snapshots/YYYY-MMDD-hhmm-ss.jpg


タイムラプス動画の生成
--------------------------------------------------

- 画像がある程度たまったら :command:`ffmpeg` を使って連結

.. code-block:: bash

   $ ffmpeg -y -f image2 -r 15 -pattern_type glob -i 'snapshots/*.jpg' -r 15 -an -vcodec libx264 -pix_fmt yuv420p video.mp4
   $ mv video.mp4 snapshots/


自動実行
--------------------------------------------------

- これらの動作を :command:`cron` に食べさせて、定期的に実行している


もうちょいやってること
--------------------------------------------------

- ユーザ情報（ ``USER`` , ``PASS`` ）をファイル中に書くのは嫌

  - PythonのConfigParserモジュールを使って外部ファイルから読むことにする

- 以下の :command:`wget` のオプションを使えるようにしている

  - アクセスできなかった場合にタイムアウトする秒数（デフォルト 10秒に設定）
  - タイムアウトした際にリトライする回数（デフォルト 1回に設定）
  - ログをファイルを残すときのファイル名（デフォルト :file:`qwatch.log` に設定）
