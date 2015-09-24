==================================================
使い方
==================================================

設定ファイルを用意する
--------------------------------------------------

- :file:`qwconf.example` をコピーして :file:`myconf.conf` を新規に作成する
- :file:`myconf.conf` の中身を自分のQwatchの設定に書き換える

設定ファイルの書式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   [WEBCAM]
   name = CAMNAME
   uri = http://QWatchADDRESS/snapshot.jpg
   user = USER
   pass = PASS
   base = EXPERIMENTS/%(name)s


.. list-table::
   :header-rows: 1
   :stub-columns: 1
   :widths: 1,3

   * - 変数名
     - 説明
   * - ``WEBCAM``
     - | ConfigParserで「セクション」と呼ぶ。
       | カメラごとに異なった名前にする。
   * - ``name``
     - | 名前。
       | カメラ毎に保存先を分けるために使う。
       | （全部同じにしても動くが、後で編集することを考えると非推奨）
   * - ``uri``
     - | JPEGファイルの場所。
       | TS-WLCAMシリーズの場合は「QwatchADDRESS」の部分を該当のIPアドレスに書き換えればOK
   * - ``user``
     - ユーザー名
   * - ``pass``
     - パスワード
   * - ``base``
     - | 画像／動画を保存するディレクトリ。
       | %(name)sの部分は、上にある「name」で置換される。
       | EXPERIMENTSには各実験グループ名（とか用途）をいれるつもり。



画像／動画の保存先
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- スクリプト内部で日付ごとに管理している
- ファイルパスの例

  :画像: :file:`EXPERIMENTS/CAMNAME/snapshots/2015/03/11/2015-0311-2230-15.jpg`
  :動画: :file:`EXPERIMENTS/CAMNAME/timelapse/2015-03-11.jpg`

- ブラウザで確認したい場合は ``EXPERIMENTS`` を公開ディレクトリへのシンボリックにするとよい

.. code-block:: bash

   $ ln -s ~/public_html/qwatch/snap EXPERIMENTS


複数台カメラを設定する場合（みかくにん）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- １台ごとにconfファイルを用意して、引数にしてもOK
- １つのconfファイルに複数台の設定を書いてもOK

.. code-block:: python

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



画像をキャプチャする : ``qwcapture``
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


タイムラプス動画の作成 : ``qwtimelapse``
--------------------------------------------------

- 日付とconfファイルを引数にして実行する
- 日付には、「 ``today`` 」「 ``yesterday`` 」「 ``YYYY/mm/dd`` の書式」が使える
- 日付は **１個** しか指定できない（confファイルは複数指定できる）

  - 基本的に毎日更新するため、複数日をまとめてやる必要が（とりあえず）ないと思うから

.. code-block:: bash

   $ ./qwtimelapse.py DATE QWCONF.conf


cronに登録する
--------------------------------------------------

- :file:`qwcron.example` をコピーして :file:`mycron.txt` を作成する（拡張子はなんでもよい）

.. code-block:: bash

   $ cp qwcron.example mycron.txt    ## Copy example and modify
   $ crontab mycron.txt              ## Eat mycron.txt
   $ crontab -l                      ## Check crontab


- :command:`crontab` は上書きされてしまうので、すでに設定がある場合はバックアップを取っておく

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

.. code-block:: bash

   $ tail /var/log/syslog
   $ sudo ls -ltrh /var/spool/nullmailer/queue/ | tail   ## ログファイル名、タイムスタンプ、サイズを確認する
   $ sudo less /var/spool/nullmailer/queue/LOGFILE       ## 上で調べたLOGFILE名の中には、cron実行時のログが吐き出されている
