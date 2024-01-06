# gradientchat
`gradientchat` is the official Python bot client module for GradientChat ~~that is OOP-based~~.
## Example
### TestBot
```py
%testbot%
```
## Docs
### `gradientchat.Bot(name, pref)`
If `name` is not `str`, raises `TypeError`, however if `pref` is not string and `name` is `str`, prefix will be lowercase of first character of `name` and a exclamation mark.
### `gradientchat.Bot.connect(servUrl)`
Connects to server; if `servUrl` is `str`, connects to URL specified on `servUrl`; raises `Exception` if already connected.
### `@gradientchat.Bot.cmd`
Decorator for adding a command; if called with a command name, command name will be set to the specified command name.

**NOTE**: The `help` command is already built-in, but can be overridden
### `gradientchat.Bot.sendMsg`
Sends a message.

**NOTE**: `sendMsg` is not required only if you are using the `cmd` decorator and can be replace by using the `return` keyword.
### `gradientchat.Bot.emit`
Emits an event with optional arguments to the server. An alias for `gradientchat.Bot.cli.emit`