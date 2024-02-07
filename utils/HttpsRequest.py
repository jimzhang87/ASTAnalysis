import requests
import DrissionPage as dp


class HttpRequesst:
    def __init__(self, url, headers=None, params=None, data=None, json=None, verify=False):
        self.url = url
        self.headers = headers
        self.params = params
        self.data = data
        self.json = json
        self.verify = verify

    def get(self):
        se_page = dp.SessionPage()
        response = se_page.get(self.url, headers=self.headers, params=self.params, data=self.data, json=self.json,
                               verify=self.verify)
        return response.text


class HttpsRequest:

    def __init__(self, url, headers=None, params=None, data=None, json=None, verify=False):
        self.url = url
        self.headers = headers
        self.params = params
        self.data = data
        self.json = json
        self.verify = verify

    def get(self):
        """发送 GET 请求"""
        response = requests.get(self.url, headers=self.headers, params=self.params, verify=self.verify)
        return response.json()

    def post(self):
        """发送 POST 请求"""
        response = requests.post(self.url, headers=self.headers, data=self.data, json=self.json, verify=self.verify)
        try:
            return response.json()
        except:
            return response.text
        # return response.json()


# def http_request(url, cookie, data, method='post'):
#     if method == 'get':
#         res = requests.get(url=url, params=data, verify=False,
#                            headers={'Content-Type': 'application/json', 'Cookie': cookie})
#     else:
#         res = requests.post(url, data)
#     print(res.text)
#     return res


if __name__ == '__main__':
    https_request = HttpRequesst(
        url='https://mihawk.oa.fenqile.com/rc_oa_gateway/hawk_decision/manage/edition_list.json', headers={
            'cookie': 'fp=294c4fecbc761f1a43dab35acee0b5be;fs_tag=D6D15689B9F89619D0F420B95DFE6AA5;''Hm_cv_6617828cdccae4d04f1557b9a67df803=1*uid*67957;oa_session=in8bq93q3d09fbo6iubtsfpko6;mid=67957;''Hm_lvt_6617828cdccae4d04f1557b9a67df803=1700204793,1701248364;channel_extend_info={"min":"jimzhang1",''"mid":"67957","retcode":30181032};sensorsdata2015session=%7B%7D;''sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2210000013900%22%2C%22%24device_id%22%3A''%2218952884ee73d3-027dfa73473a65-26031d51-1fa400-18952884ee8e46%22%2C%22props%22%3A%7B%7D%2C%22first_id%22''%3A%2218952884ee73d3-027dfa73473a65-26031d51-1fa400-18952884ee8e46%22%7D;''session=6c9f6f48c9f640dcb534f33ae6af744f;Hm_lpvt_6617828cdccae4d04f1557b9a67df803=1702447186;''rog_session_test=591e18b526a896c22ae56138082a8e75;''oa_token_id=anboW3C8kcXavWg0P81cNKIjxsyYix2i003HzQ%2BbIsvQoUB6mGzd8ZLP3e7HLiDlh%2B%2FOyuQbQIFsCQ3QkGYY2w''%3D%3D;Authorization=Bearer%20eyJhbGciOiJIUzUxMiJ9''.eyJzdWIiOiJqaW16aGFuZzEiLCJjcmVhdGVkIjoxNzAyNTQzNjA1OTAzLCJleHAiOjE3MzQwNzk2MDV9''.AbV2lAEJaSqQk9KxN5rqy1UNerDjci8ZN7JUKBOIh07vFZgmjyJE77hwAor2hVGeErM6zCfdO5xovK9bjN-D2Q;''rog_session=9752c2e496b8c868341d16cbc264f6bd'})
    re = https_request.get()
    # re = requests.post(url='http://10.9.22.52/rc_oa_gateway/hawk_decision/manage/edition_list.json', headers={'cookie': 'fp=294c4fecbc761f1a43dab35acee0b5be;fs_tag=D6D15689B9F89619D0F420B95DFE6AA5;''Hm_cv_6617828cdccae4d04f1557b9a67df803=1*uid*67957;oa_session=in8bq93q3d09fbo6iubtsfpko6;mid=67957;''Hm_lvt_6617828cdccae4d04f1557b9a67df803=1700204793,1701248364;channel_extend_info={"min":"jimzhang1",''"mid":"67957","retcode":30181032};sensorsdata2015session=%7B%7D;''sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2210000013900%22%2C%22%24device_id%22%3A''%2218952884ee73d3-027dfa73473a65-26031d51-1fa400-18952884ee8e46%22%2C%22props%22%3A%7B%7D%2C%22first_id%22''%3A%2218952884ee73d3-027dfa73473a65-26031d51-1fa400-18952884ee8e46%22%7D;''session=6c9f6f48c9f640dcb534f33ae6af744f;Hm_lpvt_6617828cdccae4d04f1557b9a67df803=1702447186;''rog_session_test=591e18b526a896c22ae56138082a8e75;''oa_token_id=anboW3C8kcXavWg0P81cNKIjxsyYix2i003HzQ%2BbIsvQoUB6mGzd8ZLP3e7HLiDlh%2B%2FOyuQbQIFsCQ3QkGYY2w''%3D%3D;Authorization=Bearer%20eyJhbGciOiJIUzUxMiJ9''.eyJzdWIiOiJqaW16aGFuZzEiLCJjcmVhdGVkIjoxNzAyNTQzNjA1OTAzLCJleHAiOjE3MzQwNzk2MDV9''.AbV2lAEJaSqQk9KxN5rqy1UNerDjci8ZN7JUKBOIh07vFZgmjyJE77hwAor2hVGeErM6zCfdO5xovK9bjN-D2Q;''rog_session=9752c2e496b8c868341d16cbc264f6bd'})
    # print(type(re))
    print(re)
    # http_request(url=url, cookie=cookie, data='', method='get')
