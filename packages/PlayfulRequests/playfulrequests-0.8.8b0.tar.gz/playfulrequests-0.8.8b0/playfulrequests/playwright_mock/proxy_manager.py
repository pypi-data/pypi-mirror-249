import httpx
from async_class import AsyncObject, link


class SplitError(Exception):
    pass


class ProxyCheckError(Exception):
    pass


class ProxyManager(AsyncObject):
    async def __ainit__(self, inst, proxy) -> None:
        link(self, inst)

        self.proxy = proxy.strip() if proxy else None
        self.http_proxy = None
        self.ip = None
        self.port = None
        self.username = None
        self.password = None
        self.browser_proxy = None
        self.plain_proxy = None
        self.timeout = httpx.Timeout(20.0, read=None)

        if self.proxy:
            self.split_proxy()
            self.proxy = (
                f"{self.username}:{self.password}@{self.ip}:{self.port}"
                if self.username
                else f"{self.ip}:{self.port}"
            )
            self.plain_proxy = f"http://{self.proxy}"

            if self.username:
                self.browser_proxy = {
                    "server": self.plain_proxy,
                    "username": self.username,
                    "password": self.password,
                }
            else:
                self.browser_proxy = {"server": self.plain_proxy}

        self.http_proxy = (
            {"http": self.http_proxy, "https": self.http_proxy} if self.proxy else None
        )

        self.phttpx = httpx.AsyncClient(proxies={"http://": self.plain_proxy})
        self.httpx = httpx.AsyncClient()

        await self.check_proxy()

    async def __adel__(self) -> None:
        await self.httpx.aclose()
        await self.phttpx.aclose()

    def split_helper(self, split) -> None:
        if not any(_.isdigit() for _ in split):
            raise SplitError("No ProxyPort could be detected")
        if split[1].isdigit():
            self.ip, self.port, self.username, self.password = split
        elif split[3].isdigit():
            self.username, self.password, self.ip, self.port = split
        else:
            raise SplitError(f"Proxy Format ({self.proxy}) isn't supported")

    def split_proxy(self) -> None:
        split = self.proxy.split(":")
        if len(split) == 2:
            self.ip, self.port = split
        elif len(split) == 3:
            if "@" in self.proxy:
                helper = [_.split(":") for _ in self.proxy.split("@")]
                split = [x for y in helper for x in y]
                self.split_helper(split)
            else:
                raise SplitError(f"Proxy Format ({self.proxy}) isn't supported")
        elif len(split) == 4:
            self.split_helper(split)
        else:
            raise SplitError(f"Proxy Format ({self.proxy}) isn't supported")

    async def check_proxy(self) -> None:
        try:
            ip_request = await self.phttpx.get(
                "https://api.ipify.org?format=json", timeout=self.timeout
            )
            ip = ip_request.json().get("ip")
        except Exception:
            raise ProxyCheckError("Could not get IP-Address of Proxy (Proxy is Invalid/Timed Out)")
        try:
            r = await self.httpx.get(f"http://ip-api.com/json/{ip}", timeout=self.timeout)
            data = r.json()
            self.country = data.get("country")
            self.country_code = data.get("countryCode")
            self.region = data.get("regionName")
            self.city = data.get("city")
            self.zip = data.get("zip")
            self.latitude = data.get("lat")
            self.longitude = data.get("lon")
            self.timezone = data.get("timezone")
            if not self.country:
                raise ProxyCheckError(
                    "Could not get GeoInformation from proxy (Proxy is probably not Indexed)"
                )
        except Exception as e:
            raise ProxyCheckError(
                "Could not get GeoInformation from proxy (Proxy is probably not Indexed)"
            ) from e
