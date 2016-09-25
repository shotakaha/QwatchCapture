==================================================
クイックスタート
==================================================


リポジトリのチェックアウト
==================================================

.. code-block:: bash

   $ git clone https://github.com/shotakaha/kumawatch.git
   $ ls kumawatch/
   LICENSE
   README.md
   docs/
   kumawatch.py
   kwcapture.py
   kwconf.example
   kwcron.example
   kwtimelapse.py


設定ファイルの用意
==================================================

.. code-block:: bash

   $ cp kwconf.example myconf.conf
   $ emacs myconf.conf


画像のキャプチャ
==================================================

.. code-block:: bash

   $ ./kwcapture.py -h
   $ ./kwcapture.py myconf.conf

タイムラプスの動画の生成
==================================================

.. code-block:: bash

   $ ./kwtimelapse.py -h
   $ ./kwtimelapse.py <date> myconf.conf
   $ ./kwtimelapse.py today myconf.conf
   $ ./kwtimelapse.py yesterday myconf.conf


自動実行したい場合
==================================================

自動実行はcronにお願いする

.. code-block:: bash

   $ cp qwcron.example mycron.txt
   $ emacs mycron.txt
   $ crontab mycron.txt


Python2.x 系を使う場合
==================================================

- タグ ``v1.5`` をチェックアウトする
- このタグの実行スクリプト内では ``#!/usr/bin/env python2`` を直書きしている
- myconf.conf の編集方法は変わらない

.. code-block:: bash

   $ git clone https://github.com/shotakaha/QwatchCapture.git
   $ cd QwatchCapture/
   $ git checkout -b v1.5 v1.5
   $ cp qwconf.example myconf.conf    ## --> myconf.confを編集する
   $ ./qwcapture.py myconf.conf

.. note::

   :command:`python3` でも :command:`python2` でも、どちらでも動くようにしたかったが、モジュール名が変わってたりしてめんどくさそうだったから諦めた
