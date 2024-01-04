import os
os.environ["BAIDU_APP_ID"] = '20231023001856425'
os.environ["BAIDU_APP_KEY"] = 'XJyBRvO_Ugy2lsTvXO0y'

from miracleplus_tools import HtmlLoader

def test_base_function():
  url = 'https://californiapolicycenter.org/san-franciscos-financial-crisis/'
  documents = HtmlLoader([url], html=True, partial=True).call()
  
  assert len(documents) > 0, 'Test selenium loader'

  