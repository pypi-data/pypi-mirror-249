from rebyte import RebyteAPIRequestor
requestor = RebyteAPIRequestor(
            key="sk-",
            api_base="https://rebyte.ai"
        )

# create an agent on rebyte platform and get the project_id and agent_id
# https://rebyte.ai/api/sdk/p/{test_project_id}/a/{test_agent_id}/r
# An example agent for Mark Zuckerberg: https://rebyte.ai/p/d4e521a67bb8189c2189/callable/a38ec8c60c3925696385/editor
project_id = "d4e521a67bb8189c2189"
callable_id = "a38ec8c60c3925696385"
path = f'/api/sdk/p/{project_id}/a/{callable_id}/r'
data = {
    "version": "latest",       
    "inputs": [{"messages": [{"role": "user","content": "My name is John"}]}],
    "config": {}
}
res, _, _ = requestor.request(
    method="POST",
    url=path,
    params=data,
    stream=False
)
print(res.data['run']['results'][0][0]["value"]["content"])