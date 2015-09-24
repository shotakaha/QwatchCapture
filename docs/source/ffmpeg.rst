==================================================
FFmpegのインストール
==================================================

MacOS Xの場合
--------------------------------------------------

- MacPortsを使って :command:`ffmpeg` をインストールする（ :command:`variants` はお好みで）

.. code-block:: bash

   $ sudo port install ffmpeg


Ubuntuの場合
--------------------------------------------------

- ``14.04 LTS`` ではそのままでは :command:`apt-get` できないみたいなので、PPAリポジトリを追加する
- 詳しくは https://launchpad.net/~mc3man/+archive/ubuntu/trusty-media を読むこと
- ``14.10`` 以上にアップグレードしないほうがいいらしい。その場合はクリーンインストールがオススメだそう。

.. code-block:: bash

   $ sudo add-apt-repository ppa:mc3man/trusty-media
   $ sudo apt-get update
   $ sudo apt-get dist-upgrade
   $ sudo apt-get install ffmpeg
