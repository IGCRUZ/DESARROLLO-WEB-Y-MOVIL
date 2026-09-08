const express = require('express');
const { ApolloServer, gql } = require('apollo-server-express');
const mongoose = require('mongoose');
const cors = require('cors');
const Jugador = require('./models/jugador');

mongoose.connect('mongodb://localhost:27017/torneo_nacional');

const typeDefs = gql`
  type Jugador {
    id: ID!
    nombre: String!
    equipo: String!
  }
  
  input JugadorInput {
    nombre: String!
    equipo: String!
  }
  
  type Respuesta {
    mensaje: String
  }
  
  type Query {
    obtenerJugadores: [Jugador]
    obtenerJugadorPorId(id: ID!): Jugador
  }
  
  type Mutation {
    ficharJugador(input: JugadorInput): Jugador
    actualizarFicha(id: ID!, input: JugadorInput): Jugador
    darDeBaja(id: ID!): Respuesta
  }
`;

const resolvers = {
  Query: {
    async obtenerJugadores() {
      return await Jugador.find();
    },
    async obtenerJugadorPorId(_, { id }) {
      const jugadorEncontrado = await Jugador.findById(id);
      return jugadorEncontrado ? jugadorEncontrado : null;
    }
  },
  Mutation: {
    async ficharJugador(_, { input }) {
      const nuevoJugador = new Jugador(input);
      await nuevoJugador.save();
      return nuevoJugador;
    },
    async actualizarFicha(_, { id, input }) {
      return await Jugador.findByIdAndUpdate(id, input, { new: true });
    },
    async darDeBaja(_, { id }) {
      await Jugador.deleteOne({ _id: id });
      return {
        mensaje: "El jugador ha sido dado de baja exitosamente"
      };
    }
  }
};

const opcionesCors = {
  origin: "http://localhost:8090",
  credentials: false
};

async function arrancarServidor() {
  const servidorApollo = new ApolloServer({ typeDefs, resolvers });
  await servidorApollo.start();
  
  const aplicacion = express();
  aplicacion.use(cors());
  
  servidorApollo.applyMiddleware({ app: aplicacion, cors: false });
  
  aplicacion.listen(8090, () => {
    console.log("API de fichajes corriendo en el puerto 8090");
  });
}

arrancarServidor();