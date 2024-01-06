$def with (micropub_endpoint, access_token, file_root)
#!/bin/bash

micropub_endpoint=https://ragt.ag/posts
access_token=secret-token:H/_MnZxm795q9.9bNLI//zqK3ex1wl94_+SKTNCwFqP_~/_i9wUmDJSYM_OE+PCwSMxP..mCJj7YV+iE~CtcH.cfsitG_RkibB3IDDUz.74oPEuKU_lPy60NF+pdsE.N
file_root="/root/ragt.ag"

curl -X POST -i $micropub_endpoint -H "Authorization: Bearer $access_token" \
  -H "Content-Type: application/json" \
  -d '{"type": ["h-entry"], "properties": {"content": {"html": "<p>Streaming Live</p><iframe width=640 height=360 src=/live></iframe>"}, "visibility": ["public"]}}' | grep location: | sed -En 's/^location: (.+)/\1/p' | tr -d '\r\n' > $file_root/last-url.txt
