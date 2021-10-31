import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session

def connection():
    eng = sqlalchemy.create_engine("mariadb+mariadbconnector://root:Thalia97@localhost:3306/diccionario")
    Base = declarative_base()
    return [eng, Base]

[eng, Base] = connection()

class diccionario(Base):
    __tablename__ = "palabras"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    palabra = sqlalchemy.Column(sqlalchemy.Text, unique=True)
    significado = sqlalchemy.Column(sqlalchemy.Text)

Base.metadata.create_all(eng)

Sesion = sqlalchemy.orm.sessionmaker()
Sesion.configure(bind=eng)
#Esta es tu variable de la conexion a mi base de datos 
sesion = Sesion()

def palabraexistente(palabra):
                check = sesion.query(sesion.query(diccionario).filter(
                    diccionario.palabra == palabra).exists()).scalar()
                return check

def agregar_palabra(palabra, definicion):
    palabranueva = diccionario(palabra=palabra,
                       significado=definicion)
    sesion.add(palabranueva) 
    sesion.commit()
    print("\n palabra fue agregada correctamente!")

def palabra_actualizada(palabravieja, palabranueva, nuevadefinicion):
                select = sesion.query(diccionario).filter(
                    diccionario.palabra == palabravieja).one()
                select.palabra = palabranueva
                select.definicion =  nuevadefinicion
                session.commit()
                print("\n La palabra " + palabravieja + " fue actualizada!")

def eliminar_palabra(palabra):
            session.query(session.query(diccionario).filter(
                diccionario.palabra == palabra).delete())
            session.commit()
            print("\n Palabra eliminada!")


def mostrar_palabras():
            palabras = session.query(diccionario).all()
            print("\n Lista de palabras \n")
            i = 0
            for row in palabras:
                i += 1
                print(f'{i}. {row.palabra}')

while True:

    print("\n Ingrese el numero del menu que desee acceder \n")

    menuOpt = int(input(" 1 Agregar una palabra nueva \n 2 Editar la palabra que ya existe \n 3 Eliminar la palabra que ya existe \n 4 Ver el listado de palabras \n 5 Buscar el significado de la palabra \n 6 Salir \n"))

    if(menuOpt == 1):
        # obtenemos la palabra y su definicion
        palabraindrocida = input("\n Ingrese la palabra a agregar \n")
        significadointroducido = input(
            "\n por ultimo ingrese la definicion de la palabra \n")
        if(len(palabraindrocida) or len(palabraindrocida)): 
            if(palabraexistente(palabraindrocida)):
                print("\n Esta palabra ya existe por favor de agregar otra")
            else:
                agregar_palabra(palabraindrocida, significadointroducido )
        else:
            print("\n Por favor llenar ambos campos de informacion")

    elif(menuOpt == 2):
        

        inputPalabra = input("\n Ingrese la palabra que desea modificar \n")

        palabraNueva = input("\n Ingrese el nuevo valor de esta palabra \n")

        definicionNueva = input(
            "\n Ingrese la nueva definicion de la palabra \n")

        if(len(palabraNueva) or len(definicionNueva) or len(inputPalabra)):

            if(palabraexistente(inputPalabra)):
                palabra_actualizada(inputPalabra, palabraNueva, definicionNueva)
            else:
                print("\n La palabra no existe!, vuelva a intentarlo")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(menuOpt == 3):
        inputPalabra = input("\n Ingrese la palabra que desea eliminar \n")

        if(len(inputPalabra)):
            if(palabraexistente(inputPalabra)):
                eliminar_palabra(inputPalabra)

            else:
                print("\n La palabra no existe!")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(menuOpt == 4):
        mostrar_palabras()

    elif(menuOpt == 5):
        inputPalabra = input(
            "\n Ingrese la palabra que desea ver su significado \n")
        if(len(inputPalabra)):
            if(palabraexistente(inputPalabra)):
                palabra = session.query(diccionario).filter(
                    diccionario.palabra == inputPalabra).scalar()
                print(f'La definicion es: {palabra.definicion}')
            else:
                print("\n La palabra no existe!")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(menuOpt == 6):
        break

    else:
        print("\n Por favor ingrese una opcion valida \n")
