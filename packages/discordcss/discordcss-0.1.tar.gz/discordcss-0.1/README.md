# discord.css
### A simple python package to use css for discord api

## Installation
run ```git clone https://github.com/CloudyDaKing/discord.css.git``` in your terminal
then cd into the directory and run ``pip install .```
use ```discordcss {css file path}``` to run  css file
ill update it to pypi soon 

## Documentation

no docs, view example below:

```css

.client {
    token: "";
    prefix: "!"
}

.command{
    command: "ping";
    description: "get bot latency";
    response: "Pong!";
}

.command{
    command: "bugsy";
    description: "get bot commands";
    response: "Hi bugsy!";
}

.onjoin{
    channel_id: "general";
    response: "Hello World!";
}

.onleave{
    channel_id: "general";
    response: "Hello World!";
}
```
