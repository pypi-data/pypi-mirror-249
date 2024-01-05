import asyncio
import hashlib
from typing import AsyncIterator, Iterator

import httpx

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
}
UNSUBSCRIBE_URL = "https://pages.awscloud.com/index.php/leadCapture/save2"


async def unsubscribe_all_async(
    emails: list[str], **kwargs
) -> AsyncIterator[tuple[str, httpx.Response]]:
    tasks = []
    async with httpx.AsyncClient(**kwargs) as client:
        for email in emails:
            tasks.append(unsubscribe_async(email, client))
        responses = await asyncio.gather(*tasks)

    for email, reponse in zip(emails, responses):
        yield (email, reponse)


def unsubscribe_all(
    emails: list[str], **kwargs
) -> Iterator[tuple[str, httpx.Response]]:
    with httpx.Client(**kwargs) as client:
        for email in emails:
            yield (email, unsubscribe(email, client))


def unsubscribe_data(email: str) -> dict:
    data = {
        "Email": email,
        "Unsubscribed": "yes",
        "UnsubscribedReason": "I already get email from another account",
        "unsubscribedReasonOther": "",
        "useCaseMultiSelect": "",
        "formid": "34006",
        "munchkinId": "112-TZM-766",
        "formVid": "34006",
    }

    checksum_fields = [
        "Email",
    ]

    checksum_str = "|".join([data.get(field, "") for field in checksum_fields])

    checksum = hashlib.sha256(checksum_str.encode("utf-8")).hexdigest()

    data["checksumFields"] = ",".join(checksum_fields)
    data["checksum"] = checksum

    return data


def unsubscribe(email: str, client: httpx.Client) -> httpx.Response:
    response = client.post(
        UNSUBSCRIBE_URL,
        data=unsubscribe_data(email),
        headers=HEADERS,
    )
    return response


async def unsubscribe_async(email: str, client: httpx.AsyncClient) -> httpx.Response:
    response = await client.post(
        UNSUBSCRIBE_URL,
        data=unsubscribe_data(email),
        headers=HEADERS,
    )
    return response
