const mongoose = require('mongoose');

const jugadorSchema = new mongoose.Schema({
  nombre: String,
  equipo: String
});

module.exports = mongoose.model('Jugador', jugadorSchema);