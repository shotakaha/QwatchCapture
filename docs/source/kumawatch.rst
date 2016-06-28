==================================================
:mod:`kumawatch`
==================================================


オブジェクトの作成
==================================================

.. code:: python

   ## Init KumaWatch
   kw = KumaWatch(name=name,
                  user=user,
                  passwd=passwd,
                  uri=uri,
                  base=base,
                  log=log)


初期設定の読み込み
==================================================

設定は :mod:`ConfigParser` を使って読み込んでいる

.. code:: python

    ## Read config files
    config = ConfigParser.SafeConfigParser()
    config.read(args.conffile)

    ## Set KumaWatch
    sections = config.sections()
    for section in sections:
        name = section
        uri = config.get(section, 'uri')
        user = config.get(section, 'user')
        passwd = config.get(section, 'pass')
        base = config.get(section, 'base')
        log = config.get(section, 'log')

.. py:class:: KumaWatch(object)


.. py:function:: def __init__(self, name, user, passwd, uri, base, log):

   '''
   Configure KumaWatch.
   '''

   :param str name: オブジェクトの名前
   :param str user: ウェブカメラにログインするユーザ名
   :param str passwd: パスワード
   :param str uri: URI
   :param str base: base
   :param str log: ログファイル名
   :param str jpgfmt: 定点撮影したファイル名のフォーマット ( :file:`snapshots/%Y/%m/%d/%Y-%m%d-%H%M-%S.jpg` )
   :param str mp4fmt: タイムラプス動画のファイル名フォーマット ( :file:`timelapse/%Y-%m-%d.mp4` )
   :param str jpgfile: JPEGファイル名 ( :file:`os.path.join(self.base, jpgfmt)` )
   :param str mp4file: MP4ファイル名 ( :file:`os.path.join(self.base, mp4fmt)` )

.. py:method:: self.set_logger()
