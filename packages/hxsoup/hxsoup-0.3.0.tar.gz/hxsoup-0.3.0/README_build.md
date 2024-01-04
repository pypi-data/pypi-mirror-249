이 설명은 최신 버전이 아닐 수 있습니다. 만약 최신 버전을 확인하고 싶으시다면 [이 깃허브 링크](https://github.com/ilotoki0804/hxsoup)를 참고하세요.
# hxsoup

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hxsoup)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hxsoup)](https://pypi.org/project/hxsoup)

**Various convenient features related to httpx and BeautifulSoup.** (<span style="color:blue">**h**</span>ttp<span style="color:blue">**x**</span> + Beautiful<span style="color:blue">**Soup**</span>)

hxsoup는 httpx를 기반으로 추가적인 기능을 추가한 라이브러리입니다.

## Getting started

파이썬을 설치하고 터미널에 다음과 같은 명령어를 입력하세요.

```console
pip install -U resoup
```

requests와 bs4는 같이 설치되지만 BeatifulSoup의 추가적인 parser인 lxml와 html5lib는 기본으로 제공하지 않습니다.

## How to use

> [!NOTE]
> 예시에서는 get 요청을 위주로 설명하지만, 다른 모든 메소드(options/head/post/put/patch/delete)에서도 동일하게 작동합니다.

### attempts

어떤 경우에서든 서버와의 연결이 실패할 수 있습니다. 이유는 다양할 수 있으나, 그저 다시 시도하는 것만으로도 해결되는 경우가 태반입니다.

만약 attempts를 1보다 큰 정수로 설정하면 연결을 실패했을 때 해당 숫자만큼 재시도합니다. 그리고 만약 결국 attempts 만큼 도전했는데도 불구하고 연결에 실패했을 경우 오류를 re-raise합니다.

연결에 바로 성공했을 경우:

```python
>>> import hxsoup.dev as hd
>>> hd.get("https://python.org", attempts=3)
<Response [200 OK]>
```

> [!NOTE]
> `hxsoup.dev`는 hxsoup와 거의 같지만 일부 기본값을 조정한 모듈입니다. hxsoup와 같다고 생각하셔도 무관합니다.
> 자세한 내용은 뒤에서 설명합니다.

연결에 끝까지 실패했을 경우:

```python
>>> import hxsoup.dev as hd
>>> hd.get("https://unreachable-service.com", attempts=3)
WARNING:root:Retrying...
WARNING:root:Retrying...
Traceback (most recent call last):
    ...
httpx.ConnectError: [Errno 11001] getaddrinfo failed
```

첫 연결에 실패하고 다시 몇 번 시도했을 때 성공했을 경우:

```python
>>> import hxsoup.dev as hd
>>> hd.get('https://www.webtoons.com/en/', attempts=4)
WARNING:root:Retrying...
WARNING:root:Retrying...
WARNING:root:Successfully retrieved: 'https://www.webtoons.com/en/'
<Response [200 OK]>
```

### raise_for_status

httpx에는 raise_for_status라는 기능이 있습니다.
`response.raise_for_status()`를 이용하면 상태 코드가 일반적이지 않을 때 오류를 냅니다.

```python
>>> import hxsoup.dev as hd
>>> response = hd.get("https://httpbin.org/status/404")
>>> response.raise_for_status()
Traceback (most recent call last):
    ...
httpx.HTTPStatusError: Client error '404 NOT FOUND' for url 'https://httpbin.org/status/404'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
```

hxsoup에서는 `raise_for_status`를 파라미터에서 그대로 사용할 수 있도록 합니다.

```python
>>> import hxsoup.dev as hd
>>> response = hd.get("https://httpbin.org/status/404", raise_for_status=True)
>>> response.raise_for_status()
Traceback (most recent call last):
    ...
httpx.HTTPStatusError: Client error '404 NOT FOUND' for url 'https://httpbin.org/status/404'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
```

Client에 `raise_for_status`를 추가하면 해당 클라이언트에서는 모두 raise_for_status가 적용됩니다.

```python
>>> import hxsoup.dev as hd
>>> with hd.Client(raise_for_status=True) as client:
...     try:
...         client.get("https://httpbin.org/status/404")
...     except Exception as e:
...         print(e)
...     try:
...         client.get("https://httpbin.org/status/404")
...     except Exception as e:
...         print(e)
...
Client error '404 NOT FOUND' for url 'https://httpbin.org/status/404'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
Client error '404 NOT FOUND' for url 'https://httpbin.org/status/404'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
```

일반적으로 상태 코드 이상은 모든 연결이 안정적으로 동작한 경우가 많기 때문에 raise_for_status에 의한 오류는 attempts에 의해 필터링되지 않습니다.

### Client

hxsoup.Client는 httpx.Client에 대응하는 기능입니다. 위에서 설명되었던 모든 추가 파라미터들(attempts, raise_for_status)는 Client에서도 사용할 수 있으며 Client를 initialize할 때 사용한다면 해당 client의 모든 통신에서 적용시킬 수 있습니다.

```python
>>> with hxsoup.Client(raise_for_status=True) as client:
...     # Client를 initialize할 때 raise_for_status를 True로 했기 때문에
...     # raise_for_status를 직접 적지 않았다면 raise_for_status가 자동을 적용됨.
...     client.get("https://httpbin.org/status/404")
...
Traceback (most recent call last):
    ...
httpx.HTTPStatusError: Client error '404 NOT FOUND' for url 'https://httpbin.org/status/404'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
```

하지만 개별 request에 해당 파라미터와 다른 파라미터를 적용했다면 해당 파라미터가 적용됩니다.

### SoupTools, SoupedResponse

`SoupTools`는 `BeautifulSoup`에 몇 가지 편리한 기능을 추가하고,
`SoupedResponse`는 `BeautifulSoup`를 respone 안에 멋지게 통합합니다.

`SoupedResponse`는 `httpx.Response`의 subclass이면서 `SoupTools`의 subclass이며,
hxsoup.dev를 포함하여 hxsoup의 모든 response는 SoupedResponse입니다.

#### The `SoupTools` methods that correspond to methods in BeautifulSoup

`SoupTools`에는 BeautifulSoup의 메소드에 대응하는 메소드들이 있습니다.

* `SoupTools.soup()`: `BeautifulSoup(...)`에 대응합니다.
* `SoupTools.soup_select(selector)`: `BeautifulSoup(...).select(selector)`에 대응합니다.
* `SoupTools.soup_select_one(selector)`: `BeautifulSoup(...).select_one(selector)`에 대응합니다.

#### `no_empty_result`

`BeautifulSoup.soup_select_one()`에는 한 가지 문제가 있습니다. 바로 해당하는 element를 찾는데 실패했을 때 오류가 아닌 None을 내밷는다는 점입니다. 이는 어쩔 때는 편리할지는 몰라도 typing도 어렵고 `.soup_select().text`와 같은 chaining도 어렵게 합니다.

hxsoup의 `response.soup_select_one()`에는 이러한 문제를 해결하기 위해 `no_empty_result`라는 파라미터를 도입했습니다.
아래는 `python.org`에 `never-gonna-selected`라는 선택자에 맞는 태그가 있는지 확인하고 있습니다. `python.org`에서는 그런 태그는 없기 때문에 일반적으로는 None을 반환받게 되는데, `no_empty_result`가 True라면 None이 아닌 오류를 raise하게 됩니다.

```python
>>> import hxsoup.dev as hd
>>> res = hd.get("https://python.org")
>>> res.soup_select_one("never-gonna-selected", no_empty_result=True)
Traceback (most recent call last):
    ...
hxsoup.exceptions.EmptyResultError: Selecting result is None. This error happens probably because of invalid selector or URL. Check whether selector and URL are both valid.
status code: HTTP 200 OK, URL: https://www.python.org/, selector: 'never-gonna-selected'
```

같은 방식이 response.soup_select()에도 적용됩니다. 이 경우 빈 리스트가 리턴될 때 EmptyResultError가 나게 됩니다.

```python
>>> import hxsoup.dev as hd
>>> res = hd.get("https://python.org")
>>> res.soup_select("never-gonna-selected", no_empty_result=True)
Traceback (most recent call last):
    ...
hxsoup.exceptions.EmptyResultError: Selecting result is empty list("[]"). This error happens probably because of invalid selector or URL. Check whether selector and URL are both valid.
status code: HTTP 200 OK, URL: https://www.python.org/, selector: 'never-gonna-selected'
```

`response.soup_select()`에도 `no_empty_result`가 있다는 점을 잊지 마세요. 따라서 `Client`나 `hxsoup.get` 자체에 `no_empty_result`를 사용할 때에는 이 기능이 `response.soup_select()`에도 적용된다는 점을 명심하세요.

#### `parser`

parser을 설정할 수 있도록 합니다. BeautifulSoup의 용어로는 `feature`입니다.

기본적으로는 `'html.parser'`를 사용하도록 되어 있습니다.

#### Broadcasting

`soup_select()`의 결과는 리스트입니다. Tag 관련 처리를 할 때에는 리스트 컴프리헨션을 이용해야 하는데, 여간 귀찮은 일이 아닙니다.

`broadcasting` 파라미터를 참으로 하면 BroadcastList가 사용됩니다.

BroadcastList는 `.bc`를 붙이면 브로드캐스팅 가능한 상황이 되고 그 뒤에 어떤 것을 붙이던 브로드캐스팅이 일어납니다.

예를 들면 다음의 코드는

```python
>>> import hxsoup.dev as hd
>>> res = hd.get("https://python.org")
>>> [tag.text for tag in res.soup_select("strong", broadcasting=True)]
['Notice:', 'A A', 'relaunched community-run job board']
```

아래의 코드로 대체될 수 있습니다.

```python
>>> import hxsoup.dev as hd
>>> res = hd.get("https://python.org")
>>> res.soup_select("strong", broadcasting=True).bc.text
['Notice:', 'A A', 'relaunched community-run job board']
```

브로드캐스팅을 더 하고 싶다면 `.bc`를 또 붙이면 됩니다.

```python
>>> import hxsoup.dev as hd
>>> res = hd.get("https://python.org")
>>> res.soup_select("strong", broadcasting=True).bc.text.bc[::2]
['Ntc:', 'AA', 'rluce omnt-u o or']
```

### ClientKeywordOptions

고정적으로 여러 request에 대해 같은 키워드를 사용해야 하는 경우가 있습니다. 대부분은 Client를 이용하면 해결되지만, AsyncClient와 Client를 같이 사용하거나, httpx.get처럼 클라이언트 없이 사용하고 싶은 경우도 있을 것입니다. 이럴 경우 이 클래스를 사용할 수 있습니다.

```python
from hxsoup import ClientKeywordOptions

```

### `hxsoup.dev`

일부 기본값을 재조정하고 caching이 포함된 모듈입니다.

#### Adjusted defaults

개발 중에는 일부 파라미터가 흔히 많이 사용됩니다. 예를 들어 `follow_redirects` 파라미터는 httpx에서 기본적으로 꺼져 있지만 이른 개발 사이클에 있는 경우 켜져 있는 것이 편한 경우가 많습니다.

개발자의 편의를 위해 `follow_redirects`를 비롯한 몇몇 파라미터들은 httpx의 기본 설정값과는 다른 값을 이용합니다.

| 파라미터 이름 | hxsoup 기본값 | `hxsoup.dev` 기본값 |
|--------------|--------------|---------------------|
| `follow_redirects` | False | True          |
| `headers`          | None  | `DEV_HEADERS` |
| `broadcasting`     | False | True          |

```python
>>> import hxsoup
>>> hxsoup.get("https://python.org")
<Response [301 Moved Permanently]>
>>>
>>> import hxsoup.dev as hd
>>> # follow_redirects가 True임.
>>> hd.get("https://python.org")
<Response [200 OK]>
```

`DEV_HEADERS`의 내용은 Chrome 브라우저의 기본 헤더이며 내용은 다음과 같습니다.

```python
{
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Arch": '"x86"',
    "Sec-Ch-Ua-Bitness": '"64"',
    "Sec-Ch-Ua-Full-Version-List": '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.130", "Google Chrome";v="120.0.6099.130"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Model": '""',
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Ch-Ua-Platform-Version": '"15.0.0"',
    "Sec-Ch-Ua-Wow64": "?0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
```

#### cached requests

활발한 개발 중에는, 특히 Jupyter를 이용할 때는, 일부 requests를 계속해서 보내게 되는 경우가 있습니다. 이는 서버에 부담을 주고 개발 속도를 늦춥니다.

각 메소드의 앞에 c를 붙이면 응답이 캐싱됩니다.

예를 들어 시간을 비교하면 아래와 같이 됩니다.

```python
>>> from timeit import timeit
>>> timeit('hd.get("https://python.org")', setup="import hxsoup.dev as hd", number=10)
0.7851526000013109
>>> timeit('hd.cget("https://python.org")', setup="import hxsoup.dev as hd", number=10)
0.061434000002918765
```

options/head/post/put/patch/delete들도 마찬가지로 대응되는 coptions/chead/cpost/cput/cpatch/cdelete가 있습니다.

```python
>>> from timeit import timeit
>>> timeit('hd.post("https://httpbin.org/post")', setup="import hxsoup.dev as hd", number=10)
9.307660000005853
>>> timeit('hd.cpost("https://httpbin.org/post")', setup="import hxsoup.dev as hd", number=10)
0.8557240999944042
```

캐시는 lru_cache 기본값을 사용하기 때문에 메소드 구분 없이 128개까지 저장됩니다.

## License information

이 프로그램의 일부는 [resoup(본인 제작)](https://github.com/ilotoki0804/resoup) 라이브러리에 있던 코드를 포함합니다.
Some part of this program contains code from [resoup(created and developed by me)](https://github.com/ilotoki0804/resoup) library.

이 프로그램의 일부는 [typeshed(Apache License 2.0 or MIT License)](https://github.com/python/typeshed) 라이브러리에 있던 코드를 포함합니다.
Some part of this program contains code from [typeshed](https://github.com/python/typeshed) library.

## Motivation and blathers

이전에 requests의 불편한 점을 느끼고 관련 내용을 입맛에 맞게 수정한 resoup라는 라이브러리를 만들어 사용하고 있었습니다.

하지만 어느 날 [ArjanCodes의 영상](https://www.youtube.com/watch?v=OPyoXx0yA0I)에서 httpx에 대해 다시 보게 되고 실제로 사용해보니 requests와 상위 호환되는 라이브러리라는 점을 알게 되었습니다.

따라서 httpx을 앞으로의 프로젝트들에서 사용하기로 결정했고, resoup의 기능을 포기할 수 없었기에 requests의 경우와 마찬가지로 resoup에 대응하는 httpx에 대한 유틸리티를 만들기로 했으며 그 결과가 hxsoup입니다.

resoup과 비교했을 때 개발 경험은 hxsoup 쪽이 압도적으로 좋았는데, requests는 type hint가 나오기 전 라이브러리라 그런지 효율적이지만 type hint를 적용하기에는 최악이었던 반면, httpx는 따로 type stub나 typing.overload를 거의 사용하지 않았을 정도로 매우 안정적이고 typing을 적용하면서 개발하기에도 좋았습니다. (물론 resoup을 만들면서 생긴 노하우도 많이 도움이 되었겠지만요.)

0.1.0을 버그가 많고 제대로 정리가 되지 않은 것들이 많습니다. 사용을 피하시기 바랍니다.

## Changelog

0.3.0 (2023-01-04): ClientOptions 추가, 코드 및 버그 수정

0.2.0 (2023-01-01): 여러 기능을 추가하고 수정.

0.1.0 (2023-12-28): 첫 (프리)릴리즈
