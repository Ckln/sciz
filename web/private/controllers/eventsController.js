'use strict';

var jwt = require('jsonwebtoken');
var config = require('../../config.js');
var db = require('../services/database.js');
var Event = require('../models/event.js');
var BattleEvent = require('../models/battle_event.js');
var CDM = require('../models/cdm.js');

var EventsController = {}

EventsController.getEvents = function (req, res) {
  
  var offset = (req.query.offset) ? parseInt(req.query.offset) : 0;


  Event.findAll({limit: 25, offset: offset, order: [['id', 'DESC']]})
    .then(function (events) {
      res.json(events);
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue :' + error.message});
    });
}

module.exports = EventsController;
