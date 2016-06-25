==================================================
事前準備
==================================================

* Python
* wget
* FFmpeg


wgetのインストール
==================================================

Homebrewを使ってインストールしたものを使っている。

.. code:: bash

   $ brew install wget
   $ wget --version
   GNU Wget 1.18 built on darwin15.5.0.

   -cares +digest -gpgme +https +ipv6 -iri
   +large-file -metalink -nls +ntlm +opie
   -psl +ssl/openssl


FFmpegのインストール
==================================================

Homebrewを使ってインストールしたものを使っている。
別の用途で必要だったので ``--with-libx265`` しているが、KumaWatchでは必須ではない

.. code:: bash

   $ brew install ffmpeg --with-libx265
   $ ffmpeg -version
   ffmpeg version 3.0.2 Copyright (c) 2000-2016 the FFmpeg developers
   built with Apple LLVM version 7.3.0 (clang-703.0.31)

   configuration: --prefix=/usr/local/Cellar/ffmpeg/3.0.2
   --enable-shared --enable-pthreads --enable-gpl --enable-version3
   --enable-hardcoded-tables --enable-avresample --cc=clang
   --host-cflags= --host-ldflags= --enable-opencl --enable-libx264
   --enable-libmp3lame --enable-libxvid --enable-libx265 --enable-vda
