from random import vonmisesvariate
from numpy import empty
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import mysql.connector
import telebot
import json 

#declaracion de listas y variables 
producto = []
aProducto = []
test = []
lista = []
compra = []
comprobar = []
option = "" 

#conexion base de datos MySql
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="tienda"
)


bot = telebot.TeleBot("ingrese aqui su token")
@bot.message_handler(commands=["start"])
def  Bienvenida(message):
  bot.reply_to(message, "Hola, Como esta\nUse los siguientes comandos para empezar a gestionar sus productos\n/listar\n/insertar\n/actualizar\n/eliminar\n/comprar\n/agotandose")

#COMPRAR PRODUCTOS
@bot.message_handler(commands=["comprar"])
def comprar(message):
  global option 
  option = "comprar"

  if message.text == "/comprar":
    bot.send_message(message.chat.id,"Ingrese los siguientes datos en mensajes separados:")
    bot.send_message(message.chat.id,"Nombre del producto")
    bot.send_message(message.chat.id,"Cantidad a comprar")

  else:
    bot.send_message(message.chat.id,"check")
    item =  message.text
    compra.append(item)   

  nombreCompra = compra[0]
  cantidadCompra = compra[1] 
  stmt = mydb.cursor()
  sql = "SELECT id,NombreProducto,Cantidad,Precio FROM productos where NombreProducto = '"+nombreCompra+"'"
  stmt.execute(sql)
  hallarCantidad  = stmt.fetchone()

  
  


  if hallarCantidad:
    
    cantidad = hallarCantidad[2]
    id = hallarCantidad[0]
    cantidadComprai= int(cantidadCompra)
    if cantidad < cantidadComprai:
        bot.send_message(message.chat.id,"Error, solo hay "+str(cantidad)+" de "+str(nombreCompra))
        bot.send_message(message.chat.id,"/comprar o /volver")

        compra.clear()
    else:
      cantidadf = cantidad - cantidadComprai
      print(cantidadf)
      sqlUpdate = "UPDATE productos SET Cantidad = %s WHERE id=%s"
      valores = (cantidadf, id)
      stmt.execute(sqlUpdate, valores)
      mydb.commit()
      bot.send_message(message.chat.id,"Compra completada /listar")
      compra.clear()
  else:
    bot.send_message(message.chat.id,"El producto no existe o esta mal escrito, inténtelo de nuevo /comprar")
    compra.clear()

    




#LISTAR TODOS MIS PRODUCTOS
@bot.message_handler(commands=["listar"])
def  listar(message):
  stmt = mydb.cursor()
  stmt.execute("SELECT id,NombreProducto,Cantidad,Precio FROM productos")
  resultado  = stmt.fetchall()
  i = 0 
  
  totalfinal = 0
  for iteracion in resultado:
    test = resultado[i]
    i = i + 1
    cantidad = test[2] 
    precio = test[3]
    total = cantidad*precio

    totalfinal = totalfinal + total
    
    
  
  resultadoj = json.dumps(resultado , indent = 4)
  bot.reply_to(message, resultadoj)
  bot.send_message(message.chat.id,"Costo total inventario:"+ str(totalfinal))
  bot.reply_to(message, "Orden:\n id\nnombre\ncantidad\nprecio")
  bot.reply_to(message, "Escriba /volver para ver los comandos o utilice el que guste")

#MOSTRAR PRODUCTOS A PUNTO DE AGOTARSE
@bot.message_handler(commands=["agotandose"])
def agotando(message):
  stmt = mydb.cursor()
  stmt.execute("SELECT id,NombreProducto,Cantidad,CantidadInicial,Precio FROM productos")
  resultado  = stmt.fetchall()
  i = 0 
  for iteracion in resultado:
    lista = resultado[i]
    i = i + 1
    nombre = lista[1]
    cantidad = lista[2] 
    cantidadInicial = lista[3]

    
    porcentaje = cantidadInicial * 0.1  
    print(porcentaje)

    if cantidad < porcentaje:
      bot.send_message(message.chat.id,nombre+" se esta agotando")
      comprobar.append(nombre)

  if comprobar:
    print("si hay productos agotandose") 
  else:
    bot.send_message(message.chat.id," No hay productos agontandose aun, regrese mas tarde")



    
    
# INSERTAR PRODUCTOS A MI DB
@bot.message_handler(commands=["insertar"])
def  insertar(message):
  global option 
  option = "insertar"   

  if message.text == "/insertar":
    bot.reply_to(message, "Ingrese los siguientes datos en mensajes separados")
    bot.send_message(message.chat.id,"Nombre de producto")
    bot.send_message(message.chat.id,"Cantidad")
    bot.send_message(message.chat.id,"Precio")


    
  else:
    bot.send_message(message.chat.id,"check")
    item =  message.text
    producto.append(item)
   

  print("--por indice---")
  if producto[0]:
    nombrep = producto[0]
  if producto[1]:
    cantidad = producto[1]
  if producto[2]: 
    precio = producto[2]

  

  print(nombrep+cantidad+precio) 

  #hacemos la consulta para insertar
  if producto[2]:
    stmt = mydb.cursor()
    sql = "INSERT INTO productos (NombreProducto,Cantidad,CantidadInicial,Precio) VALUES (%s,%s,%s,%s)"
    valores = (nombrep,cantidad,cantidad,precio)
    stmt.execute(sql, valores)
    mydb.commit()
    bot.send_message(message.chat.id,"Producto añadido")
    bot.send_message(message.chat.id,"Para verlo escriba /listar")
    producto.clear()


  

#ACTUALIZAR PRODUCTO
@bot.message_handler(commands=["actualizar"])
def  actualizar(message):
  global option 
  option = "actualizar"
  if message.text == "/actualizar":
    bot.send_message(message.chat.id, "Ingrese el -- ID -- del producto")
    bot.send_message(message.chat.id, "El campo que quiere modificar en minusculas(nombre,cantidad,precio)")
    bot.send_message(message.chat.id, "Ingrese el nuevo valor")
    bot.send_message(message.chat.id, "En mensajes separados")

  
  else: 
     bot.send_message(message.chat.id,"check")
     item =  message.text
     aProducto.append(item)

  if aProducto[0]:   
    id = aProducto[0]
  if aProducto[1]:   
    campo = aProducto[1]
  if aProducto[2]:   
    nuevoDato= aProducto[2]

  

  #print(campo, id , nuevoDato)

  if campo == "nombre":
    if aProducto[2]:
      stmt = mydb.cursor()
      sql = "UPDATE productos SET NombreProducto = %s WHERE id=%s"
      valores = (nuevoDato,id)
      stmt.execute(sql , valores)
      mydb.commit()
      bot.send_message(message.chat.id,"Producto actualizado")
      bot.send_message(message.chat.id,"/listar")
      aProducto.clear()

  elif campo == "cantidad":
    if aProducto[2]:
      stmt = mydb.cursor()
      sql = "UPDATE productos SET Cantidad = %s,CantidadInicial = %s WHERE id=%s"
      valores = (nuevoDato,nuevoDato,id)
      stmt.execute(sql , valores)
      mydb.commit()
      bot.send_message(message.chat.id,"Producto actualizado")
      bot.send_message(message.chat.id,"/listar")
      aProducto.clear()
    
  elif campo == "precio":
    if aProducto[2]:
      stmt = mydb.cursor()
      sql = "UPDATE productos SET Precio = %s WHERE id=%s"
      valores = (nuevoDato,id)
      stmt.execute(sql , valores)
      mydb.commit()
      bot.send_message(message.chat.id,"Producto actualizado")
      bot.send_message(message.chat.id,"/listar")
      aProducto.clear()
  else:
    #if aProducto[2]:
      bot.send_message(message.chat.id,"Error el campo a modificar no existe o esta mal escrito, inténtelo de nuevo /actualizar")
      aProducto.clear()
      print("Tiene: ")
      print( aProducto)    

      

#ELIMINAR PRODUCTO
@bot.message_handler(commands=["eliminar"])
def  eliminar(message):
  global option
  option = "eliminar"
  if message.text == "/eliminar":
    bot.reply_to(message, "Ingrese el id de el producto que desea eliminar")
  else:
    stmt = mydb.cursor()
    sql = "delete from productos where id=" + message.text
    stmt.execute(sql)
    mydb.commit()
    bot.send_message(message.chat.id,"Producto eliminado")
    bot.send_message(message.chat.id,"/listar")


@bot.message_handler(commands=["v","volver"])
def  volver(message):
    bot.reply_to(message, "Hola, Como esta\nUse los siguientes comandos para empezar\n/listar\n/insertar\n/actualizar\n/eliminar\n/comprar\n/agotandose")


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


#MAIN 
if __name__ == '__main__':
    bot.infinity_polling()


    