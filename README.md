
<h1 align="center">Desafio Técnico – NLT</h1>


## 🧾 Explicação do Projeto

Este projeto é um desafio técnico desenvolvido com uma arquitetura completa, composta por:

- **Front-end** acessível via navegador
- **Back-end** em Django REST Framework
- **Autenticação via JWT**
- **Painel administrativo do Django**
- **Documentação interativa com Swagger e Redoc**
- **Execução de tarefas assíncronas com Celery + RabbitMQ**

O objetivo da aplicação é simular um fluxo de autenticação e gerenciamento de dados por meio de uma API RESTful, oferecendo endpoints documentados e um painel administrativo acessível para visualização detalhada dos modelos.

---

## Requirements

- [Docker](https://www.docker.com/products/docker-desktop/)


## No terminal, na raiz do projeto, digite ou execute os comandos abaixo

### Para Criar um novo ambiente virtual

+ `cd challenge`
+ `docker-compose build`
+ `docker-compose up`

### login na aplicação

Agora você pode fazer login na aplicação

+ `http://localhost:5173`
+ `Login: admin@gmail.com`
+ `Password: admin`

### Admin

Login no admin para caso queira visualizar os modelos com mais detalhes

+ `http://localhost:8000/admin`
+ `Login: admin@gmail.com`
+ `Password: admin`


## 📚 Documentação da API

- [Swagger UI](http://localhost:8000/swagger/)
- [ReDoc](http://localhost:8000/redoc/)

