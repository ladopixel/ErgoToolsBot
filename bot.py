from telegram import ParseMode, Update
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackContext
import requests
from telegram.utils.helpers import escape_markdown

import RPi.GPIO as GPIO
import lcd

mylcd = lcd.lcd()

GPIO.setmode(GPIO.BCM)

updater = Updater('yourBotToken')

URLHeight = 'https://api.ergoplatform.com/api/v1/networkState'
URLprecio = 'https://api.nanopool.org/v1/ergo/prices'
URLHashRate = 'https://api.ergoplatform.com/api/v0/info'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('*{}*:\n{}'.format('Welcome to ErgoToolsBot ' + str(update.effective_user.first_name),'\n\nThis project is OpenSource https://github.com/ladopixel/ErgoToolsBot'),  parse_mode=ParseMode.MARKDOWN)
    print('Entro el usuario: ' + str(update.effective_user.username) + ' - Id: ' + str(update.effective_user.id))
    mylcd.lcd_clear()
    mylcd.lcd_display_string('Welcome', 1, 0)
    mylcd.lcd_display_string(str(update.effective_user.username), 2, 0)

def info(update: Update, context: CallbackContext) -> None:

    data = requests.get(URLHeight) 
    data = data.json()
    altura = str(data['height'])

    dataprecio = requests.get(URLprecio)
    dataprecio = dataprecio.json()
    precioEUR = str(dataprecio['data']['price_eur'])
    precioUSD = str(dataprecio['data']['price_usd'])
    precioBTC = str(dataprecio['data']['price_btc'])

    dataHashRate = requests.get(URLHashRate) 
    dataHashRate = dataHashRate.json()
    hashRate = str('{0:.2f}'.format(dataHashRate['hashRate']/1000000000000))
    supply = str('{0:.0f}'.format(dataHashRate['supply']/1000000000))

    update.message.reply_text('*{}*'.format('ℹ️ Info Ergo Blockchain'),  parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text('Prices' + '\n' + precioEUR + ' EUR · ' + precioUSD + ' USD ·  ' + precioBTC + ' BTC \nCreation Height: ' + altura + '\nHashrate: ' + hashRate + ' TH/s \nSupply: ' + supply + ' ERG / 97739924 ERG')
    print('User ' + update.effective_user.username + '\nInfo')
    mylcd.lcd_clear()
    mylcd.lcd_display_string(update.effective_user.username, 1, 0)
    mylcd.lcd_display_string('Info ' + precioEUR + ' EUR', 2, 0)

def instructions(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('*{}*'.format('ℹ️ Instructions ErgoToolsBot'),  parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text(f'\n\nHi ' + str(update.effective_user.username) + '\nI am gaining knowledge, for the moment you can send me a message with a valid Ergo wallet address or token ID and I will show you some information.')
    print('User ' + update.effective_user.username + '\nInstructions')
    mylcd.lcd_clear()
    mylcd.lcd_display_string(update.effective_user.username, 1, 0)
    mylcd.lcd_display_string('Instructions', 2, 0)

def credits(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('*{}*'.format('ℹ️ Technology used in ErgoToolsBot'),  parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text(f' · Raspberry Pi 4\n · BotFather Telegram user\n · Python\n · Ergo API Explorer\n')

    print('User ' + update.effective_user.username + '\nCredits')
    mylcd.lcd_clear()
    mylcd.lcd_display_string(update.effective_user.username, 1, 0)
    mylcd.lcd_display_string('Credits', 2, 0)

def escuchoMensajes(update: Update, context: CallbackContext) -> None:

    valorIntroducido = str(update.message.text)
    walletOK = 400
    tokenOK = 400
    searchOK = 400
    
    if requests.get('https://api.ergoplatform.com/api/v1/addresses/' + valorIntroducido + '/balance/confirmed').status_code == 200:
        walletOK = 200
        update.message.reply_text('*{}*'.format('ℹ️ Info Wallet'),  parse_mode=ParseMode.MARKDOWN)
        dataWallet = requests.get('https://api.ergoplatform.com/api/v1/addresses/' + valorIntroducido + '/balance/confirmed')
        tokenOK = 400
    elif requests.get('https://api.ergoplatform.com/api/v0/assets/' + valorIntroducido + '/issuingBox').status_code == 200:
        tokenOK = 200
        searchOK = 400
        update.message.reply_text('*{}*'.format('ℹ️ Info Token'),  parse_mode=ParseMode.MARKDOWN)
        dataToken = requests.get('https://api.ergoplatform.com/api/v0/assets/' + valorIntroducido + '/issuingBox')
        walletOK = 400
        searchOK = 400
    elif requests.get('https://api.ergoplatform.com/api/v1/tokens/search?query=' + valorIntroducido).status_code == 200:
        dataTokenSearch = requests.get('https://api.ergoplatform.com/api/v1/tokens/search?query=' + valorIntroducido)
        walletOK = 400
        tokenOK = 400
        searchOK = 200
        

    ############ WALLET
    if walletOK == 200:
        dataWallet = dataWallet.json()
        totalWallet = str(dataWallet['nanoErgs']/1000000000)
        totalTokens = str(len(dataWallet['tokens']))
        ############ Muestro el mensaje
        update.message.reply_text(totalWallet + ' ERG\n' + totalTokens + ' tokens')
        print('User: ' + update.effective_user.username + '\nWallet: ' + valorIntroducido)
        mylcd.lcd_clear()
        mylcd.lcd_display_string(update.effective_user.username, 1, 0)
        mylcd.lcd_display_string(valorIntroducido, 2, 0)
    ############ TOKEN
    elif tokenOK == 200:
        dataToken = dataToken.json()
        nameToken = str(dataToken[0]['assets'][0]['name'])
        amountToken = str(dataToken[0]['assets'][0]['amount'])
        descriptionToken = toUtf8String(dataToken[0]['additionalRegisters']['R5'])[2:]
        
        # Detect NFT
        try:
            tokenNFT = dataToken[0]['additionalRegisters']['R7']
        except:
            tokenNFT = ''
        
        # Detect NFT type
        if tokenNFT == '0e020101':
            try:
                urlArchivo = resolveIpfs(toUtf8String(dataToken[0]['additionalRegisters']['R9'])[2:])
            except:
                urlArchivo = 'No URL available in R9'
        elif tokenNFT == '0e020102':
            url1ArchivoAudio = resolveIpfsAudio(toUtf8String(dataToken[0]['additionalRegisters']['R9'])[4:])
            url2ArchivoAudio = resolveIpfsAudio2(toUtf8String(dataToken[0]['additionalRegisters']['R9'])[4:])
        elif tokenNFT == '0e020103':
            urlArchivo = resolveIpfs(toUtf8String(dataToken[0]['additionalRegisters']['R9'])[2:])
        else:
            urlArchivo = 'No NFT'
            print('User: ' + update.effective_user.username + '\nNo NFT')
            mylcd.lcd_clear()
            mylcd.lcd_display_string(update.effective_user.username, 1, 0)
            mylcd.lcd_display_string('No NFT', 2, 0)


        ############ Muestro el mensaje
        try:
            update.message.reply_text('Name: ' + nameToken + '\n' + 'Amount: ' + amountToken + '\nImage: ' + urlArchivo + '\nDescription: ' + descriptionToken)
        except:
            update.message.reply_text('Name: ' + nameToken + '\n' + 'Amount: ' + amountToken + '\nAudio: ' + url1ArchivoAudio + '\nAudio Image: ' + url2ArchivoAudio + '\nDescription: ' + descriptionToken)
        print('User: ' + update.effective_user.username + '\nToken query:' + nameToken)
        mylcd.lcd_clear()
        mylcd.lcd_display_string(update.effective_user.username, 1, 0)
        mylcd.lcd_display_string(nameToken, 2, 0)
    
    if searchOK == 200:
        dataTokenSearch = dataTokenSearch.json()
        totalTokenSearch = str(dataTokenSearch['total'])
        update.message.reply_text('*{}*'.format('ℹ️ There are ' + totalTokenSearch +' tokens with this name'),  parse_mode=ParseMode.MARKDOWN)
        print('User: ' + update.effective_user.username + '\nToken: ' + valorIntroducido)
        mylcd.lcd_clear()
        mylcd.lcd_display_string(update.effective_user.username, 1, 0)
        mylcd.lcd_display_string(valorIntroducido, 2, 0)
        
        if dataTokenSearch['total'] == 1:
            dataToken = requests.get('https://api.ergoplatform.com/api/v0/assets/' + dataTokenSearch['items'][0]['id'] + '/issuingBox')
            dataToken = dataToken.json()
            nameToken = str(dataToken[0]['assets'][0]['name'])
            amountToken = str(dataToken[0]['assets'][0]['amount'])
            descriptionToken = toUtf8String(dataToken[0]['additionalRegisters']['R5'])[2:]
            try:
                urlArchivo = resolveIpfs(toUtf8String(dataToken[0]['additionalRegisters']['R9'])[2:])
            except:
                urlArchivo = 'No URL available in R9'
            ############ Muestro el mensaje
            update.message.reply_text('Name: ' + nameToken + '\nImage: ' + urlArchivo + '\nDescription: ' + descriptionToken)
            print('User: ' + update.effective_user.username + '\nToken query: ' + nameToken)
            mylcd.lcd_clear()
            mylcd.lcd_display_string(update.effective_user.username, 1, 0)
            mylcd.lcd_display_string(nameToken, 2, 0)

def toUtf8String(hex):
    valorUTF8= '' 
    aux = ''
    contador = 0
    for i in hex:
        contador = contador + 1
        if contador < 3:
            aux = aux + i
        if contador == 2:
            valorUTF8 = valorUTF8 + str(chr(int(aux, 16)))
            contador = 0
            aux = ''
    return valorUTF8

def resolveIpfs(url):
    ipfsPrefix = 'ipfs://'
    if url[0:7:1] != ipfsPrefix:
        return url
    else:
        print(url.replace(ipfsPrefix, 'https://cloudflare-ipfs.com/ipfs/'))
        return url.replace(ipfsPrefix, 'https://cloudflare-ipfs.com/ipfs/')

def resolveIpfsAudio(urls):
    ipfsPrefix = 'ipfs://'
    posicion = urls.find('B')
    if urls[0:7:1] != ipfsPrefix:
        return urls
    else:
        url1 = urls[0:posicion:1]
        url1 = url1.replace(ipfsPrefix, 'https://cloudflare-ipfs.com/ipfs/')
        print(url1.replace(ipfsPrefix, 'https://cloudflare-ipfs.com/ipfs/'))
    return str(url1)

def resolveIpfsAudio2(urls):
    ipfsPrefix = 'ipfs://'
    posicion = urls.find('B')
    if urls[0:7:1] != ipfsPrefix:
        return urls
    else:
        url2 = urls[posicion+1:]
        url2 = url2.replace(ipfsPrefix, 'https://cloudflare-ipfs.com/ipfs/')
        print(url2.replace(ipfsPrefix, 'https://cloudflare-ipfs.com/ipfs/'))
    return str(url2)

def main() -> None:
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, escuchoMensajes))
    updater.dispatcher.add_handler(CommandHandler('info', info))
    updater.dispatcher.add_handler(CommandHandler('instructions', instructions))
    updater.dispatcher.add_handler(CommandHandler('credits', credits))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()