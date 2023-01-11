### Bot Telegram con Python y MySQL

El bot gestiona el inventario de una tienda con las siguientes funciones:

- /listar
- /insertar
- /actualizar
- /eliminar
- /comprar
- /agotandose (sin tilde)

### Botfather Telegram
Ingrese botfather en el buscador de Telegram 

Tendrá que inicializar** /start **el chat con botfather para posteriormente crear un nuevo bot **/newbot** para después nombrarlo como sea necesario.

**Le dará un token para poder acceder al HTTP API **

línea 26:   bot = telebot.TeleBot("ingrese aquí su token")

**nota: **no comparta su token o cualquier persona podrá manipular la información de su bot.

### Base de datos 

Puede usar la base de datos que prefiera, en este caso adjunto la mía exportada de phpMyAdmin como ejemplo.

### Metodos importantes


- **Mantiene el código en ejecución.**
```python
		#linea 295:
		if __name__ == '__main__':
		bot.infinity_polling()



- **Lee el texto ingresado para llamar a las funciones.**

Esta función lee los valores necesarios que son diferentes a los comandos como el nombre del producto, precio, cantidad.



	#línea 279:
	@bot.message_handler(content_types=["text"])
	def leer_mensaje(message):
	  if message.text.startswith("/"):
		 bot.send_message(message.chat.id,"el comando no existe")
	  else:
		if option == "insertar":
		  insertar(message)
		elif option == "actualizar":
		  actualizar(message)
		elif option == "eliminar":
		  eliminar(message)
		elif option == "comprar":
		  comprar(message)          

- **Función se ejecuta siendo llamada como comando, en este caso /start**
línea 27:
		@bot.message_handler(commands=["start"])
		def  Bienvenida(message):
	 	 bot.reply_to(message, 
	  "Hola, Como esta\nUse los siguientes comandos para empezar a gestionar sus productos\n/listar\n/insertar\n/actualizar\n/eliminar\n/comprar\n/agotandose")
