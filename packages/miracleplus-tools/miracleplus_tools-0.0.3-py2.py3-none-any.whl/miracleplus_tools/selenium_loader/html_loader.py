from typing import List, Optional
import time, logging, json

from .lib.document import Document
from .lib.selenium_driver import SeleniumDriver

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

NEED_REDIRECT_URLS = [
    "toutiao.com",
    "youtube.com",
    "twitter.com",
    "mathstodon.xyz",
    "hn.algolia.com",
]

SHOW_YOUTUBE_TRANSCRIPT_JS = """
(function() {
    'use strict';
    setTimeout(() => {
        const transcripts = document.querySelectorAll('[target-id="engagement-panel-searchable-transcript"]');
        if(transcripts.length == 1) {
            const transcript = transcripts[0];
            transcript.setAttribute("visibility", "ENGAGEMENT_PANEL_VISIBILITY_EXPANDED");
            console.log('transcript should show up now...');
        }
    }, "3000"); // wait for 3 seconds (hopefully sufficient for all the necessary elements to load) - adjust this based on your internet speed
})();
"""

MARK_HIDDEN_JS = """
function isHiddenInSelenium(el) {
    return getComputedStyle(el).display == "none";
}
function traverse(elm) {
    if (elm.classList && isHiddenInSelenium(elm)) {
        elm.classList.add("selenium-hidden");
    }
    for (var i=0; i < elm.childNodes.length; i++) {
        // recursively call to traverse
        traverse(elm.childNodes[i]);
    }
}
traverse(document.querySelector("body"));
"""

MARK_IMAGE_SIZE_JS = """
function mark_image_size() {
    for (var img of document.querySelectorAll("img")) {
        var style = getComputedStyle(img);
        img.dataset.computedHeight = style.height;
        img.dataset.computedWidth = style.width;
    }
}
mark_image_size();
"""

FORMAT = '%(asctime)s %(name)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('html_loader')
logger.setLevel(logging.INFO)

# 使用
class HtmlLoader:
    def __init__(
        self, urls: List[str], binary_location: Optional[str] = None, html: bool = False, partial: bool = False, driver = None
    ):
        self.urls = urls
        self.binary_location = binary_location
        self.html = html
        self.partial = partial
        self._start_time = time.time()
        self.driver = driver

    def call(self):
        docs: List[Document] = list()
        time_start = time.time()
        for url in self.urls:
            driver = self.driver or SeleniumDriver.init_driver()
            wait = WebDriverWait(driver, 10)
            try:
                if not url.startswith("http"):
                    url = "https://" + url

                # 有时候会有newtab的情况发生，即页面还没有开始加载内容
                # 这种情况即重新加载页面，这里有3次的重试
                max_attempts = 3
                attempt = 0
                while attempt < max_attempts:
                    try: 
                        # 最多加载30秒，超时则抛出异常
                        # 有的页面会有很多的异步加载请求，但是实际上页面已经加载完成了
                        # 所以只需要加载30秒，超时则抛出异常，然后直接读取页面数据即可
                        driver.set_page_load_timeout(30)
                        driver.get(url)
                        if driver.execute_script('return document.title') == 'New Tab':
                            attempt += 1
                        else:
                            break
                    except TimeoutException as e:
                        pass

                # 这种域名带有中间页面跳转，需要等待一段时间
                if any([redirect_url in url for redirect_url in NEED_REDIRECT_URLS]):
                    time.sleep(3)

                element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                # 错误页面检查，如果为chrome的错误页面，则重新请求
                # error_elements = driver.find_elements(By.CSS_SELECTOR, "div[jscontent='errorCode'].error-code")
                # if len(error_elements) > 0:
                #     raise Exception("error page")

                embed_content = driver.execute_script("return document.querySelectorAll('body > embed').length") > 0
                extra_content = None
                if not self.partial and driver.current_url.startswith("https://www.youtube.com"):
                    driver.execute_script(SHOW_YOUTUBE_TRANSCRIPT_JS)
                    try:
                        element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "ytd-transcript-segment-renderer")))
                    except:
                        pass
                    content = "<html>%s</html>" % driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
                    soup = BeautifulSoup(content, "lxml")
                    extra_content = "\n".join([str(tag.text) for tag in soup.select("ytd-transcript-segment-renderer yt-formatted-string")])
                elif embed_content:
                    type = driver.execute_script("return document.querySelector('body > embed').type")
                    url = driver.execute_script("return document.querySelector('body > embed').src")
                    if url == 'about:blank':
                        url = driver.current_url
                    doc = Document(page_content="", metadata={"url": url, "type": type})
                    docs.append(doc)
                    continue
                elif self.html:
                    # mark hidden elements
                    driver.execute_script(MARK_HIDDEN_JS)
                    # mark image size
                    # if icon is not specified, we will use largest image as icon
                    driver.execute_script(MARK_IMAGE_SIZE_JS)
                    content = "<html>%s</html>" % driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
                    soup = BeautifulSoup(content, "lxml")
                    for css in [
                        "body .selenium-hidden",
                        "head style",
                        "head script",
                        "head noscript",
                        "img",
                        ".errorContainer"
                    ]:
                        for item in soup.select(css):
                            item.extract()
                    # optimized for sharing page.
                    # https://developers.facebook.com/docs/sharing/webmasters?locale=zh_CN
                    title = soup.select_one("head title")
                    og_title = soup.select_one('head meta[property="og:title"]')
                    if (not title or len(title.text.strip()) == 0) and og_title and len(
                        og_title["content"]
                    ) > 0:
                        for item in soup.select("head title"):
                            item.extract()
                        new_title = soup.new_tag("title")
                        new_title.string = og_title["content"]
                        soup.select_one("head").append(new_title)

                    content = str(soup)
                else:
                    content = element.get_attribute("innerHTML")
                # for redirect scenario, we need to find real url
                docs.append(Document(page_content=content, metadata={"url": url, "type": "text/html", "extra": extra_content}))
            except Exception as e:
                print(url, e)
                continue
            finally:
                driver.quit()

        logger.info(f"--- selenium time in {time.time() - time_start} ---")
        return docs