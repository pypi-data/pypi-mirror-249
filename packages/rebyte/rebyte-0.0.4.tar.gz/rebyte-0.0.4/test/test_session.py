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

# You may use any string as session_id and try to avoid duplicate session_ids
# Note that you must set session_id if you want to enable stateful actions, such as threads (aka, memory), in your agent.
# Or you can leave it as empty when the agent has no stateful actions.
data = {
    "version": "latest",       
    "inputs": [{"messages": [{"role": "user","content": "Please remember: My name is John"}]}],
    "config": {},
    "session_id" : "ANY_STRING"
}
res, _, _ = requestor.request(
    method="POST",
    url=path,
    params=data,
    stream=False
)
print(res.data['run']['results'][0][0]["value"]["content"])

data = {
    "version": "latest",       
    "inputs": [{"messages": [{"role": "user","content": "Please answer me: What is my name?"}]}],
    "config": {},
    "session_id" : "ANY_STRING"
}
res, _, _ = requestor.request(
    method="POST",
    url=path,
    params=data,
    stream=False
)
print(res.data['run']['results'][0][0]["value"]["content"])