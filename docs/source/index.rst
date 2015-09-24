.. QwatchCapture documentation master file, created by
   sphinx-quickstart on Thu Sep 24 15:54:21 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================================
Welcome to QwatchCapture's documentation!
==================================================


できること
==================================================

ウェブカメラを使って定点観測＆タイムラプス動画の自動生成ができるPythonスクリプト


クイックスタート
--------------------------------------------------

- とりあえず画像キャプチャ

.. code-block:: bash

   $ git clone https://github.com/shotakaha/QwatchCapture.git
   $ cd QwatchCapture/
   $ cp qwconf.example myconf.conf    ## --> edit myconf.conf
   $ ./qwcapture.py myconf.conf

- 自動実行したい場合

.. code-block:: bash

   $ cp qwcron.example mycron.txt    ## --> edit mycron.txt
   $ crontab mycron.txt


動作環境
==================================================

ウェブカメラ
--------------------------------------------------

  - [[http://www.iodata.jp/product/lancam/lancam/ts-wlcam/][IO-DATA Qwatch TS-WLCAMシリーズ]]
    - USBケーブルしか付属してないので注意
    - TS-WLCAM用ADアダプター（[[http://www.ioplaza.jp/shop/g/g60-TVCXGA2-001/][TVC-XGA2]]）があるとよい

パソコン
--------------------------------------------------

  - MacOS X(10.10 Yosemite) + Python(2.7.9) + wget(1.16.2) + ffmpeg(2.6)
  - Ubuntu (14.04LTS) + Python(2.7.6) + wget(1.15) + ffmpeg(2.6)


やってること
==================================================


画像のキャプチャ
--------------------------------------------------

   - ウェブカメラ内に保存されている画像を wget を使って取得
     - 画像のURLは http://www.ispyconnect.com/man.aspx?n=IO+Data で調べた
     - 右上の検索ボックスに型番とか入れるとたぶん見つかる
   - 取得した画像は、その時の時刻でリネーム

.. code-block:: bash

   $ wget --http-user=USER --http-password=PASS http://QwatchIPADDRESS/snapshot.jpg
   $ mv snapshot.jpg snapshots/YYYY-MMDD-hhmm-ss.jpg


タイムラプス動画の生成
--------------------------------------------------

   - 画像がある程度たまったら ffmpeg を使って連結

.. code-block:: bash

   $ ffmpeg -y -f image2 -r 15 -pattern_type glob -i 'snapshots/*.jpg' -r 15 -an -vcodec libx264 -pix_fmt yuv420p video.mp4
   $ mv video.mp4 snapshots/



自動実行
--------------------------------------------------

   - これらの動作をcronに食べさせて、定期的に実行している


もうちょいやってること
--------------------------------------------------

   - ユーザ情報（USER、PASS）をファイル中に書くのは嫌
     - PythonのConfigParserモジュールを使って外部ファイルから読むことにする
   - 以下のwgetのオプションを使えるようにしている
     - アクセスできなかった場合にタイムアウトする秒数（デフォルト 10秒に設定）
     - タイムアウトした際にリトライする回数（デフォルト 1回に設定）
     - ログをファイルを残すときのファイル名（デフォルト qwatch.logに設定）

使い方
==================================================

設定ファイルを用意する
--------------------------------------------------

   - qwconf.exampleをコピーしてmyconf.confを新規に作成する
   - myconf.confの中身を自分のQwatchの設定に書き換える

設定ファイルの書式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: config

   [WEBCAM]
   name = CAMNAME
   uri = http://QWatchADDRESS/snapshot.jpg
   user = USER
   pass = PASS
   base = EXPERIMENTS/%(name)s


- WEBCAM :: ConfigParserで「セクション」と呼ぶ。カメラごとに異なった名前にする。
- name :: 名前。カメラ毎に保存先を分けるために使う。（全部同じにしても動くが、後で編集することを考えると非推奨）
- uri :: JPEGファイルの場所。TS-WLCAMシリーズの場合は「QwatchADDRESS」の部分を該当のIPアドレスに書き換えればOK
- user :: ユーザー名
- pass :: パスワード
- base :: 画像／動画を保存するディレクトリ。%(name)sの部分は、上にある「name」で置換される。EXPERIMENTSには各実験グループ名（とか用途）をいれるつもり。


画像／動画の保存先
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- スクリプト内部で日付ごとに管理している
- ファイルパスの例
  - 画像 :: EXPERIMENTS/CAMNAME/snapshots/2015/03/11/2015-0311-2230-15.jpg
  - 動画 :: EXPERIMENTS/CAMNAME/timelapse/2015-03-11.jpg

- ブラウザで確認したい場合は、experiments を公開ディレクトリへのシンボリックにするとよい

.. code-block:: bash

   $ ln -s ~/public_html/qwatch/snap experiments


複数台カメラを設定する場合（みかくにん）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- １台ごとにconfファイルを用意して、引数にしてもOK
- １つのconfファイルに複数台の設定を書いてもOK

.. code-block:: bash

   [WEBCAM1]
   name = CAMNAME1
   uri = http://QWatchADDRESS-1/snapshot.jpg
   user = USER
   pass = PASS
   base = WEBHOME/%(name)s

   [WEBCAM2]
   name = CAMNAME2
   uri = http://QWatchADDRESS-2/snapshot.jpg
   user = USER
   pass = PASS
   base = WEBHOME/%(name)s



画像をキャプチャする : qwcapture
--------------------------------------------------

- confファイルを引数にして実行する

.. code-block:: bash

   $ ./qwcapture.py QWCONF.conf


- 複数のconfファイルを指定することもできる

.. code-block:: bash

   $ ./qwcapture.py QWCONF.conf QWCONF2.conf


オプションについて
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- いちおうwgetのオプションが使えるようになっている
- ヘルプを確認して下さい

.. code-block:: bash

   $ ./qwatch.py -h


タイムラプス動画の作成 : qwtimelapse
--------------------------------------------------

- 日付とconfファイルを引数にして実行する
- 日付には、「today」「yesterday」「YYYY/mm/dd の書式」が使える
- 日付は *１個* しか指定できない（confファイルは複数指定できる）
  - 基本的に毎日更新するため、複数日をまとめてやる必要が（とりあえず）ないと思うから


.. code-block:: bash

   $ ./qwtimelapse.py DATE QWCONF.conf


cronに登録する
--------------------------------------------------

- qwcron.example をコピーして、mycron.txtを作成する（拡張子はなんでもよい）

.. code-block:: bash

   $ cp qwcron.example mycron.txt    ## Copy example and modify
   $ crontab mycron.txt              ## Eat mycron.txt
   $ crontab -l                      ## Check crontab


- crontabは上書きされてしまうので、すでに設定がある場合はバックアップを取っておく

.. code-block:: bash

   $ crontab -l > mycront.bk    ## Backup crontab


cronの書式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   分 時 日 月 曜日 実行コマンド


10分ごとに画像をキャプチャする場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- QwatchCaptureのあるディレクトリまでのパスを指定する
- confファイルも指定する

.. code-block:: text

   QWDIR=      ## qwatch.py があるディレクトリを指定する
   QWCONFIGS=  ## confファイルを指定（複数指定できる、半角スペースで区切る（みかくにん））

   */10 * * * * `cd $QWDIR && ./qwcapture.py $QWCONFIG`


1時間ごとにタイムラプス動画を作る場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 毎時5分に作成（キャプチャの実行と時間をずらしてある）
- 毎日00時08分に、前日の動画をまとめる（これも時間をずらしてある）

.. code-block:: text

   5 * * * * `cd $QWDIR && ./qwtimelapse.py today QWCONFIGS`
   8 0 * * * `cd $QWDIR && ./qwtimelapse.py yesterday QWCONFIGS`


ログの確認
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- cronのログは以下のディレクトリ／ファイルで確認できる

.. code-block:: text

   $ tail /var/log/syslog
   $ sudo ls -ltrh /var/spool/nullmailer/queue/ | tail   ## ログファイル名、タイムスタンプ、サイズを確認する
   $ sudo less /var/spool/nullmailer/queue/LOGFILE       ## 上で調べたLOGFILE名の中には、cron実行時のログが吐き出されている


その他
==================================================

FFmpegのインストール
--------------------------------------------------

MacOS Xの場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    - MacPortsを使って ffmpeg をインストールする
      - variants はお好みで

#+begin_src
$ sudo port install ffmpeg
#+end_src

Ubuntuの場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - 14.04 LTS ではそのままではapt-getできないみたいなので、PPAリポジトリを追加する
   - 詳しくは https://launchpad.net/~mc3man/+archive/ubuntu/trusty-media を読むこと
     - 14.10 以上にアップグレードしないほうがいいらしい。その場合はクリーンインストールがオススメだそう。

#+begin_src bash
$ sudo add-apt-repository ppa:mc3man/trusty-media
$ sudo apt-get update
$ sudo apt-get dist-upgrade
$ sudo apt-get install ffmpeg
#+end_src


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
