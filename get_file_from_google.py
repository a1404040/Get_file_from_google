from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
import os
import urllib.request
import json
import ssl
import socket
from loguru import logger
from selenium.webdriver.common.by import By

socket.setdefaulttimeout(10.0)

ssl._create_default_https_context = ssl._create_unverified_context


def get_image_urls(sw, keyword, path, directory):
    kw = 'filetype:' + keyword + f' {sw}'
    ch_op = Options()
    ch_op.add_argument('--headless')
    ch_op.add_argument('--no-sandbox')
    ch_op.add_argument('--disable-gpu')
    ch_op.add_argument('--disable-dev-shm-usage')
    url = "https://www.google.com.hk/"
    browser = webdriver.Chrome(options=ch_op)
    logger.info(sw + ":打开浏览器" + keyword)
    browser.get(url)
    time.sleep(2)
    input = browser.find_elements(By.XPATH, "//textarea[@class='gLFyf']")[0]
    input.send_keys(kw)
    input.send_keys(Keys.ENTER)
    time.sleep(2)
    while True:
        for i in range(1, 10):
            try:
                a = browser.find_element(By.XPATH,
                                         f"//*[@id='rso']/div[{i}]/div/div/div[1]/div/div/span/a")
                name = browser.find_element(By.XPATH,
                                            f"//*[@id='rso']/div[{i}]/div/div/div[1]/div/div/span/a/h3").text
                print(name)
                logger.success('success')
            except Exception as e:
                continue
            href = str(a.get_attribute('href'))
            logger.info(href)
            try:
                download_file(href, name, path, keyword)
                time.sleep(1)
            except Exception as e:
                print(e)
                continue
        time.sleep(2)
        try:
            b = browser.find_element(By.XPATH, '//*[@id="pnnext"]/span[2]')
            logger.info("点击下一页")
        except Exception as e:
            time.sleep(2)
            break
        b.click()
    time.sleep(2)
    logger.info("关闭浏览器")
    browser.close()


def download_file(url, name, path, keyword):
    try:
        logger.info(f"路径:{path} |下载类型:{keyword}  | 下载文件:{name}")
        headers = ("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE")
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        res = opener.open(url).read()
    except Exception as e:
        logger.error(f"下载失败:{name} | {e}")
        return
    if len(res) > 0:
        with open(directory + path + name + '.' + keyword, 'wb') as file:
            # file.write(res.content)
            file.write(res)
            file.close()


def str2json(strs):
    strjson = json.loads(strs)
    image_url = strjson.get('ou')
    return image_url


def get_search_word(word_list):
    search_list = []
    for word in word_list:
        directory = word.split(".")[0]
        with open(word, 'r', encoding='utf-8-sig') as f:
            for line in f.readlines():
                date = ''.join(line).strip('\n')
                search_list.append(date)
        return search_list, directory


if __name__ == '__main__':
    search_list = ["操作员编号", "查询结果编号", "查询目的", "登记业务编号", "交易金额", "交易类型", "交易子类",
                   "接入类型", "保单状态", "保费", "基金名称", "CVN", "银行卡类型", "SSN", "保证种类", "币种",
                   "厂牌车型", "车牌种类", "催收方式", "存款种类", "贷款类型", "贷款用途", "担保方式", "房产信息",
                   "个人信用报告", "还款方式", "假币收缴来源", "开户行",
                   "授信用途", "授信种类", "违约种类", "视频类型", "视频名称", "投保单号", "信贷记录", "银行ukey",
                   "游戏类兑换码", "动态口令", "公钥", "汽车行业名词_新能源汽车", "汽车行业名词_燃油汽车",
                   "汽车行业名词_接车单", "汽车行业名词_冷却系", "不动产登记证明号", "产权人名称",
                   "产品名称", "出口贸易编号", "订单ID", "国家代码", "国家名称", "行业名称", "金融许可证号", "经济类型",
                   "客户代码", "客户类型", "客户名称", "渠道ID", "渠道名称", "抵押权人名称", "付款人名称", "汇率",
                   "收款人类型", "业务串号", "银行代码",
                   "公司财务数据", "公司运营数据", "签名方法", "渠道类型", "商户代码", "二级商户代码", "二级商户简称",
                   "发卡机构代码", "业务种类", "预付卡通道", "持卡人IP", "订单接收超时时间", "控制规则", "默认支付方式",
                   "支付超时时间", "终端号", "原交易查询流水号",
                   "收单机构代码", "证书类型", "商户简称", "商户类别", "清算日期", "文件类型", "化工行业名词_化学药剂1",
                   "经营指标名词", "经营指标名词", "电信行业名词_锁相术语", "电信行业名词_电源术语", "业务代码",
                   "业务类型", "业务流水号", "银行账户", "银行账户ID", "证件号码", "投资者类型"]

    keywords = ['xlsx', 'xls', 'doc', 'docx', 'csv', 'pdf']
    for sw in search_list:
        path = f'{sw}/'
        directory = ''
        for keyword in keywords:
            try:
                if not os.path.exists(directory + path):
                    os.makedirs(directory + path)
                get_image_urls(sw, keyword, path, directory)
            except Exception as e:
                logger.error(str(e))
                logger.error(keyword + " " + path + "——下载出错")
                continue
    logger.error("运行结束")
