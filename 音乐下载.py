import requests
import json
import os
from Crypto.Cipher import AES
from base64 import b64encode
import binascii
from tqdm import tqdm
import random


class NeteaseMusicCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Cookie': '_iuqxldmzr_=32; WM_TID=VJ3tCST2NDBBEUBFVAOB2jx%2BwNWx1p8c; NTES_P_UTID=e8gjnGyzt7LSETdPrVKVI7aqyUlDO4JN|1721043067; P_INFO=m17302256803@163.com|1721043067|0|mail163|00&99|null&null&null#guz&520100#10#0#0|173803&1||17302256803@163.com; nts_mail_user=17302256803@163.com:-1:1; MUSIC_U=00CFA1348405DEBC0CF9459B0F6CB7835CCFC35990E15932E245045B81893FCB2E2AB4A35393E03BA9DA40027D170670D7F7EE14E0439DC3C72CA45B22B5FAC68D39FB92F70F7B2CF5638C9C8D12C6B73302238503B48797D259CA89686D2C0EAE5566A5BCC75E874B24B2CF489E19D59032C32BC210D86F2BBC9B11B36C36D6CDF30D9F565E18CDC36A31CE55CD0CFCF320352E02733050CDCF506F3BA5D36880F30EBBF76A07D02CD7494BC3837B89E581E9C0716D9A8E73AF4C1A7B9BC3873ABDF70D20A66960977C7AC1594C6221866F891B40769460A00E8A5FA7461855CD51DB1954575E02DCE0D4E3F8841053FEDCEA1D06CDAEF9900A21161B22FF5F5B19789B905B970E8881EFCED84D316DAF89860D58C0C206D102A326E0033F138CC47C86B29088A2A5E304C208FBC676ABCBFB4CDD2A39491CDAC1D0F7EBF072E74120F9B601305192157D61C31C2FD7BB44F5F4B31FC9023567E60C954B1E93B2; __remember_me=true; __csrf=9738f3749d5462d7afe9ba04e91405e7; NMTID=00Ov9R2JvxA4jrHo0hKgOavYWdozI8AAAGUdCYDVA; __csrf=9738f3749d5462d7afe9ba04e91405e7; JSESSIONID-WYYY=geCBiZy8VXwKHfESaPBjKmHgI%2FiZ7KtFdwVdlt%2BmuHxn13DsFn6K3e4zSRaoKU86VTebTEj8N8JDrDw8y%2Fnk9FJGVjrr1e76xi%5CREI%5C87YrmxJaXgWtud2NmWrbIVgzmZhYZ4F17KqspFIvbmyDVF7z8lBe9hTtbJZvYh5ktiV%2FQ%2FSPj%3A1737117236068; _ntes_nnid=bdc620e200ee3348e618f1c22236aef6,1737115436081; _ntes_nuid=bdc620e200ee3348e618f1c22236aef6; WM_NI=4x5GMb9TQiRW4h9teBe%2BomOPYewrOn3S0bDa1e6jHk9Yxpv6LeKEUfp1U4f9e5xAHHgclAbrkGu3Ce8Vred%2F6VmAvLnx3pGeDoyPa%2FH9GZxnFAioEyVVlyuqyUjMaz3hYkg%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb7cc6a95aa82a3d95398b08eb2d54e838f9e86cb5395ada4b4d76888ebbb83d82af0fea7c3b92af8a8fba8d06afb8c9f8ad15df8b8f795e84aa7f5a18ece5c9bbbb993ce66f18d0083c76bf3bbfa8bcb61fb87b891f53e90bb85a6d86eb4ef9bd5e533a7ebb8a2cb44a5bda4a2e17aa999bbd4c26ffc8abe86e725f68aa3a2f548aea8fd91c66f88b1b7b1e4258ce789bbfb66869fa790c873968aa49af87bbb8ba6aee472f1b8978ce637e2a3',
            'Referer': 'https://music.163.com/',
            'Origin': 'https://music.163.com',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def create_secret_key(self, size):
        """生成随机字符串作为密钥"""
        return (''.join(map(lambda xx: (hex(xx)[2:]), os.urandom(size))))[0:16]

    def aes_encrypt(self, text, key):
        """AES加密"""
        pad = 16 - len(text) % 16
        text = text + chr(pad) * pad
        encryptor = AES.new(key.encode(), AES.MODE_CBC, b'0102030405060708')
        encrypt_text = encryptor.encrypt(text.encode())
        encrypt_text = b64encode(encrypt_text).decode()
        return encrypt_text

    def rsa_encrypt(self, text, pubkey, modulus):
        """RSA加密"""
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text.encode()), 16), int(pubkey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def generate_params(self, data):
        """生成请求参数"""
        text = json.dumps(data)
        secKey = self.create_secret_key(16)
        encText = self.aes_encrypt(text, '0CoJUm6Qyw8W8jud')
        encText = self.aes_encrypt(encText, secKey)
        encSecKey = self.rsa_encrypt(secKey, '010001',
                                     '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7')
        return {
            'params': encText,
            'encSecKey': encSecKey
        }

    def get_hot_songs(self):
        """获取热歌榜数据"""
        print("正在获取热歌榜数据...")
        url = "https://music.163.com/weapi/v6/playlist/detail"
        data = {
            'id': '3778678',
            'offset': '0',
            'total': 'true',
            'limit': '20',
            'n': '1000',
            'csrf_token': ''
        }

        try:
            params = self.generate_params(data)
            response = self.session.post(url, data=params)

            # 打印响应状态和内容，用于调试
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text[:200]}...")  # 只打印前200个字符

            if response.status_code != 200:
                raise Exception(f"请求失败，状态码: {response.status_code}")

            return response.json()
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {str(e)}")
            print(f"返回的内容: {response.text[:200]}...")
            raise
        except Exception as e:
            print(f"请求发生错误: {str(e)}")
            raise

    def download_song(self, song_id, song_name):
        """下载单首歌曲"""
        url = "https://music.163.com/weapi/song/enhance/player/url/v1"
        data = {
            'ids': [song_id],
            'level': 'lossless',
            'encodeType': 'aac',
            'csrf_token': ''
        }

        try:
            params = self.generate_params(data)
            response = self.session.post(url, data=params)
            song_info = response.json()['data'][0]
            song_url = song_info['url']
            file_size = song_info.get('size', 0)

            if not song_url:
                print(f'\n× 无法获取下载链接: {song_name} (可能需要VIP权限)')
                return

            # 创建下载目录
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'netease_music')
            if not os.path.exists(desktop_path):
                os.makedirs(desktop_path)

            file_path = os.path.join(desktop_path, f'{song_name}.mp3')

            # 下载歌曲并显示进度
            response = requests.get(song_url, stream=True)
            total_size = int(response.headers.get('content-length', file_size))
            block_size = 1024

            with tqdm(total=total_size, unit='iB', unit_scale=True,
                      desc=f'下载中: {song_name}') as pbar:
                with open(file_path, 'wb') as f:
                    for data in response.iter_content(block_size):
                        pbar.update(len(data))
                        f.write(data)

            if os.path.getsize(file_path) == total_size:
                print(f'\n√ 下载成功: {song_name}')
            else:
                print(f'\n× 下载可能不完整: {song_name}')

        except Exception as e:
            print(f'\n× 下载失败: {song_name}, 错误: {str(e)}')


def main():
    try:
        crawler = NeteaseMusicCrawler()
        hot_songs = crawler.get_hot_songs()

        if not hot_songs or 'playlist' not in hot_songs or 'tracks' not in hot_songs['playlist']:
            print("获取歌曲列表失败")
            return

        total_songs = len(hot_songs['playlist']['tracks'])
        print(f"\n共找到 {total_songs} 首歌曲")
        print("开始下载...\n")

        for index, song in enumerate(hot_songs['playlist']['tracks'], 1):
            print(f"\n[{index}/{total_songs}]")
            song_id = song['id']
            song_name = song['name']
            # 处理文件名中的非法字符
            song_name = "".join(c for c in song_name if c not in r'\/:*?"<>|')
            crawler.download_song(song_id, song_name)

        print("\n所有歌曲下载完成！")
        print(f"文件保存在: {os.path.join(os.path.expanduser('~'), 'Desktop', 'netease_music')}")

    except Exception as e:
        print(f"\n下载过程中出现错误: {str(e)}")


if __name__ == "__main__":
    main()