==================================================
クイックスタート
==================================================

- とりあえず画像キャプチャ

.. code-block:: bash

   $ git clone https://github.com/shotakaha/QwatchCapture.git
   $ cd QwatchCapture/
   $ cp qwconf.example myconf.conf    ## --> myconf.confを編集する
   $ ./qwcapture.py myconf.conf

- 自動実行したい場合

.. code-block:: bash

   $ cp qwcron.example mycron.txt    ## --> mycron.txtを編集する
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
