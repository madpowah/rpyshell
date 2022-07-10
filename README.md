# rpyshell
A simple Python Reverse Shell client / server

Actually, 2 commands:

- info: to get OS and hardware information of the client
- exec <command>: to execute a command on the client

```
(venv) PS C:\\python\reverseshell> python .\rpyshellserv.py
>> Python Reverse Shell v0.1 - cloud (http://www.madpowah.org)
>> Listening as 0.0.0.0:8080 …
[+] 127.0.0.1:50868 connected.
$ info
[+] OS detection: Windows
[+] CPU number: 8
[+] CPU frequency: 2501.0 Mhz
[+] RAM: 16.3 Go
[+] Partitions: C:\ D:\
$ exec hostname
DESKTOP-XXXXXX
$ exit
>>> Exiting …
```
