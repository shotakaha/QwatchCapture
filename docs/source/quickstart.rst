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
