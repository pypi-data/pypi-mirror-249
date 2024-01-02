import asyncio
from rebyte import RebyteAPIRequestor

async def main():
    requestor = RebyteAPIRequestor(
        key="sk-",
        api_base="https://rebyte.ai"
    )
    project_id = "d4e521a67bb8189c2189"
    callable_id = "a38ec8c60c3925696385"
    path = f'/api/sdk/p/{project_id}/a/{callable_id}/r'
    data = {
        "version": "latest",       
        "inputs": [{"messages": [{"role": "user","content": "My name is John"}]}],
        "config": {},
        "stream": True
    }
    res, _, _ = await requestor.arequest(
        method="POST",
        url=path,
        params=data,
        stream=True
    )
    async for msg in res:
        # print streaming output message
        stream_text = msg.get_stream_chunk()
        if msg and stream_text:
            print(stream_text)

asyncio.run(main())