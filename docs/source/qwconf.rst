==================================================
設定ファイルの準備
==================================================

- :file:`qwconf.example` をコピーして :file:`myconf.conf` を新規に作成する
- :file:`myconf.conf` の中身を自分のQwatchの設定に書き換える

設定ファイルの書式
==================================================

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
==================================================

- スクリプト内部で日付ごとに管理している
- ファイルパスの例

  :画像: :file:`EXPERIMENTS/CAMNAME/snapshots/2015/03/11/2015-0311-2230-15.jpg`
  :動画: :file:`EXPERIMENTS/CAMNAME/timelapse/2015-03-11.jpg`

- ブラウザで確認したい場合は ``EXPERIMENTS`` を公開ディレクトリへのシンボリックにするとよい

.. code-block:: bash

   $ ln -s ~/public_html/qwatch/snap EXPERIMENTS


複数台カメラを設定する場合（みかくにん）
==================================================

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
