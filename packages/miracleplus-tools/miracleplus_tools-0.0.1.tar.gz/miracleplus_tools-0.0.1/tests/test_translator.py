import os
os.environ["BAIDU_APP_ID"] = '20231023001856425'
os.environ["BAIDU_APP_KEY"] = 'XJyBRvO_Ugy2lsTvXO0y'

from miracleplus_tools import Translator

def test_base_function():
  translate_text = Translator().call(['test', '不翻译', None, ''])

  assert translate_text == ['测验', '不翻译', None, ''], 'Test translator'