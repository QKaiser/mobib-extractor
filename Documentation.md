# Documentation

If you launch the original MOBIB extractor code, you will find that it is no longer selecting and reading at the right locations except for the holder data. To observe the new commands, I launched a Windows VM, setup a proxy and went to [https://www.stib-mivb.be/mystib/Home/Index] . There you can download a browser plugin that allows you to connect to their website and do online top-ups.

The software is installed in `C:\Users\pentest\AppData\Local\Programs\MOBIB_Reader`. The interesting part is that the software was built with .Net: `MOBIB_Reader.exe: PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows`. If you open it with a .Net disassembler like Telerik's JustDecompile, you'll see that the software is logging everything it does at `%HOMEDRIVE%%HOMEPATH%mobib_reader.log`.

Small excerpt of that log file:

```
[2017-09-14 19:22:27.244] INFO: ================================================================================
[2017-09-14 19:22:27.244] INFO: Start native Windows URL handler version 2
[2017-09-14 19:22:27.244] INFO: ================================================================================
[2017-09-14 19:22:27.254] INFO: Windows version: Windows 7 Professional (Microsoft Windows NT 6.1.7601 Service Pack 1)
[2017-09-14 19:22:27.254] INFO: URL: mobibreader://2/fr/ReadCard/39f10c5f-0ec7-4436-bc9c-9d82e681a270?https://webapi-wf1.stib-mivb.be/2.0/sales/cards/
[2017-09-14 19:22:27.254] INFO: Parameters: version=2, language=fr, operation=ReadCard, transactionId=39f10c5f-0ec7-4436-bc9c-9d82e681a270, serverUrl=https://webapi-wf1.stib-mivb.be/2.0/sales/cards/
[2017-09-14 19:22:27.414] INFO: Detecting card
[2017-09-14 19:25:02.921] INFO: Card detected: reader="Generic Smart Card Reader Interface 0", protocol=T0, ATR=3B6F0000805A3C23C4141001C0D4FDCE829000
[2017-09-14 19:25:02.921] INFO: Requesting exclusive card access
[2017-09-14 19:25:03.011] INFO: Calling Init
[2017-09-14 19:25:04.354] INFO: Server request: url=https://webapi-wf1.stib-mivb.be/2.0/sales/cards/init, data={
  "transactionId": "39f10c5f-0ec7-4436-bc9c-9d82e681a270",
  "operation": "ReadCard"
}
[2017-09-14 19:25:05.326] INFO: Server response: http 200, data=[
  "AKQEAA4xVElDLklDQdBWAAGRAQA=",
  "ALIBPB0=",
  "ALICPB0=",
  "ALIBzB0=",
---snip---
```

The plugin receives base64 encoded raw APDUs from the server, send them to the card, then sends the results back to the server as base64 encoded raw response APDUs.

Exemple of such request:

```
POST /2.0/sales/cards/init HTTP/1.1
Content-Type: application/json; charset=utf-8
Host: webapi-wf1.stib-mivb.be
Content-Length: 91
Expect: 100-continue
Connection: close


{
  "transactionId": "8d98c67f-5444-4f77-972f-75277721b1dc",
  "operation": "ReadCard"
}
```

```
HTTP/1.1 100 Continue


HTTP/1.1 200 OK
Date: Thu, 14 Sep 2017 20:44:17 GMT
Server: Microsoft-IIS/8.0
Cache-Control: no-cache
Pragma: no-cache
Content-Type: application/json; charset=utf-8
Expires: -1
X-AspNet-Version: 4.0.30319
X-Powered-By: ASP.NET
Content-Length: 414
Connection: close


[
  "AKQEAA4xVElDLklDQdBWAAGRAQA=",
  "ALIBPB0=",
  "ALICPB0=",
  "ALIBzB0=",
  "ALIBTB0=",
  "ALICTB0=",
  "ALIDTB0=",
  "ALIETB0=",
  "ALIFTB0=",
  "ALIGTB0=",
  "ALIHTB0=",
  "ALIITB0=",
  "ALIBvB0=",
  "ALICvB0=",
  "ALIDvB0=",
  "ALIEvB0=",
  "ALIB7B0=",
  "ALIC7B0=",
  "ALID7B0=",
  "ALIE7B0=",
  "ALIBtB0=",
  "ALIB9B0=",
  "AKQEAAugAAACkdBWAAGQAQA=",
  "ALIB5B0=",
  "ALIC5B0="
]
```


## APDUs

Here is the list of hex encoded APDUs. They need to be sent in that order (at least for the select-then-read order). I figured out most of them but some (marked "unknown") still needs to be analyzed.

| Operation                   | HEX                                                        |
|-----------------------------|------------------------------------------------------------|
| select                      | `00 A4 04 00 0E 31 54 49 43 2E 49 43 41 D0 56 00 01 91 01` |
| read unknown record         | `00 C0 00 00 2A`                                           |
| read unknown record         | `00 B2 01 3C 1D`                                           |
| read unknown record         | `00 B2 02 3C 1D`                                           |
| read counter                | `00 B2 01 CC 1D`                                           |
| read contract record        | `00 B2 01 4C 1D`                                           |
| read contract record        | `00 B2 02 4C 1D`                                           |
| read contract record        | `00 B2 03 4C 1D`                                           |
| read contract record        | `00 B2 04 4C 1D`                                           |
| read contract record        | `00 B2 05 4C 1D`                                           |
| read contract record        | `00 B2 06 4C 1D`                                           |
| read contract record        | `00 B2 07 4C 1D`                                           |
| read contract record        | `00 B2 08 4C 1D`                                           |
| read event log record 1     | `00 B2 01 BC 1D`                                           |
| read event log record 2     | `00 B2 02 BC 1D`                                           |
| read event log record 3     | `00 B2 03 BC 1D`                                           |
| read event log record 4(?)  | `00 B2 04 BC 1D`                                           |
| read unknown record 1       | `00 B2 01 EC 1D`                                           |
| read unknown record 2       | `00 B2 02 EC 1D`                                           |
| read unknown record 3       | `00 B2 03 EC 1D`                                           |
| read unknown record 4       | `00 B2 04 EC 1D`                                           |
| read unknown record 1       | `00 B2 01 B4 1D`                                           |
| read connection list record | `00 B2 01 F4 1D`                                           |
| select                      | `00 A4 04 00 0B A0 00 00 02 91 D0 56 00 01 90 01`          |
| read unknown                | `00 C0 00 00 00`                                           |
| subsequent read unknown     | `00 C0 00 00 27`                                           |
| read holder record 1        | `00 B2 01 E4 1D`                                           |
| read holder record 2        | `00 B2 02 E4 1D`                                           |
