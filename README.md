# KumaWatch

ウェブカメラを使って定点観測＆タイムラプス動画の自動生成ができるPythonスクリプト

# クイックスタート

   - とりあえず画像キャプチャ

``` shellsession
$ git clone https://github.com/shotakaha/QwatchCapture.git
$ cd QwatchCapture/
$ cp qwconf.example myconf.conf    ## --> edit myconf.conf
$ ./qwcapture.py myconf.conf
```

   - 自動実行したい場合

``` shellsession
$ cp qwcron.example mycron.txt    ## --> edit mycron.txt
$ crontab mycron.txt
```

# より詳しく

  [[http://qwatchcapture.readthedocs.org/ja/latest/][QwatchCapture - Read the Docs]] に書いておきました


## 備考

2016-06-20 : QwatchCapture -> KumaWatch に改名
