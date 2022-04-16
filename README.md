<h1>ErgoToolsBot</h1>
<p>ErgoToolsBot is a Telegram bot to receive real-time information from the <strong><a href="https://explorer.ergoplatform.com/en/" title="Ergo Blockchain" target="_blank">Ergo blockchain.</a></strong></p>
<p>The bot is working on a RaspberryPi 4 that has a 2x16 LCD screen connected showing me the username, id and some more information about the queries that are made.</p>

<img src="https://ergotokens.org/ErgoToolsBot.jpeg" alt="ErgoToolsBot display LCD image" width="500" />
<h3>ErgoToolsBot does not store anything in the database.</h3>
<p>This is the URL for Telegram<a href="https://t.me/ErgoToolsBot" title="ErgoToolsBot Telegram"> https://t.me/ErgoToolsBot.</a></p>


<h2>Project Instructions</h2>
<p>
  These instructions are still incomplete, once they are complete this message will disappear. They are divided into 3 main parts:
  <ul>
    <li><strong>BotFather Telegram</strong> - Interaction with BotFather to create the bot from Telegram.</li>
    <li><strong>Ergo with Python</strong> - Code written in Python to query the Ergo blockchain.</li>
    <li><strong>Raspberry Pi GPIO</strong> - Hardware libraries and connection schemes for Raspberry Pi.</li>
  </ul>
</p>

<hr>
<h2>BotFather Telegram</h2>
<p>I want to add new features little by little, for now this tool shows the following:</p>
  <ul>
    <li><strong>/start</strong> (Greetings from ErgoToolsBot)</li>
    <li><strong>/info</strong> (General information about Ergo's blockchain)</li>
    <li><strong>/instructions</strong> (General information about ErgoToolsBot)</li>
   <li><strong>/credits</strong> (Technology used)</li>
  </ul>
<p>You can send a message to the bot with a valid wallet it shows the amount of tokens and the balance in ERG</p>
<p>You can send a message to the bot with the ID of a token will show us the name, amount issued, description and URL of the image, audio or video if it is a NFT</p>

<hr>
<h2>Ergo with Python</h2>
<p>Remember that you can contribute to improve the code whenever you want.</p>

<hr>
<h2>Raspberry Pi GPIO</h2>
<img src="https://github.com/Gadgetoid/Pinout.xyz/blob/master/graphics/pinout-graphic-horizontal-72dpi.png" alt="Raspberry Pi GPIO" width="500"/>

<p>To display the data on my 16x2 LCD display I am using the <a href="https://gist.github.com/DenisFromHR/cc863375a6e19dce359d" title="LCD Library" target="_blank">LCD library</a>, modified to <a href="http://www.recantha.co.uk/blog/?p=4849" title="LCD Library" target="_blank">this other version.</a>
<br><strong>You just have to <a href="https://github.com/ladopixel/ErgoToolsBot/blob/master/lcd.py" title="Library LCD.py">include the LCD.py file</a> of the project.</strong></p>
