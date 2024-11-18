# Vercel Cortes API

**¡Bienvenido a la API que ayuda a los quiteños a mantenerse informados sobre los cortes de luz! 💡**

## 🚀 Descripción del Proyecto

**Vercel Cortes API** es una herramienta creada con Flask que realiza **web scraping** y **PDF scraping** en la página oficial de la Empresa Eléctrica de Quito. El propósito es proporcionar información sobre los cortes de energía eléctrica en Quito basándose en la zona ingresada por el usuario.

### 🧐 ¿Qué hace esta API?

Al enviar una consulta con el nombre de una zona, la API devuelve detalles sobre los cortes programados en esa ubicación.

**Prueba la API aquí:**  
👉 [https://vercel-cortes-api.vercel.app/api?zona=cumbaya](https://vercel-cortes-api.vercel.app/api?zona=cumbaya)

### 🗣️ Alexa Skill Integrado

Además, esta API está integrada con un **Skill de Alexa**, que permite a los usuarios preguntar:  
**"¿Cuándo será el próximo corte de luz en mi [zona]?"**  
Alexa consulta la API y responde con la información correspondiente.

---

## 📄 Documentación de la API

### Endpoint Principal

**GET** `/api`  

#### Parámetros

| Parámetro | Tipo   | Descripción                                  | Obligatorio |
|-----------|--------|----------------------------------------------|-------------|
| `zona`    | String | Nombre de la zona para consultar los cortes. | Sí          |

#### Ejemplo de Uso
 
```curl "https://vercel-cortes-api.vercel.app/api?zona=cumbaya" ```


RESPUESTA


```
{"data":
  {
    "horarios":["0:00 - 04:00","12:00 - 16:00"],
    "zona":"cumbaya"
  }
}
```


## 🛠️ Cómo Colaborar

¡Este proyecto es open source y toda colaboración es bienvenida! Aquí tienes cómo puedes participar:

Si tienes ideas o experiencia en scraping, optimización de APIs, o nuevos enfoques para este tipo de proyectos, ¡anímate a contribuir!

Para colaborar:
	1.	Realiza un fork del proyecto.
	2.	Crea una rama con tu funcionalidad o mejora
	3.	Realiza un pull request (PR).


## Usar la API en tus proyectos

La API está disponible para todos. Úsala en aplicaciones móviles, otros Skills de Alexa o sistemas de monitoreo. **NO ABUSES CON LAS PETICIONES**

## Probar el Skill de Alexa

Únete a la beta pública del Skill.
Envíame un mensaje directo para incluirte. 🙌

## 📧 Contacto

Autor: Juan Francisco Cisneros

Correo: jfcisnerosg@icloud.com

GitHub: juanfranciscocis

LinkedIn: [Juan Francisco Cisneros](www.linkedin.com/in/juanfranciscocisneros)


 





