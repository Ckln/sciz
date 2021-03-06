'use strict'; 

var sequelize = require('sequelize');
var TrollTemplate = {}

/*
 *  Methods
 */
TrollTemplate.changeBlasonURL = function (troll) {
  if(troll && troll.constructor === Array) {
    var arrayLength = troll.length;
    for (var i = 0; i < arrayLength; i++) {
      if (troll[i] && troll[i].blason_url && troll[i].blason_url.startsWith('http://www.mountyhall.com/images/Blasons/Blason_PJ')) {
        troll[i].blason_url = 'http://blason.mountyhall.com/Blason_PJ/' + troll[i].id;
      } else if (troll[i] && !troll[i].blason_url) {
        troll[i].blason_url = 'http://blason.mountyhall.com/Blason_PJ/MyNameIsNobody.gif';
      }
    }
  }
  else {
    if (troll && troll.blason_url && troll.blason_url.startsWith('http://www.mountyhall.com/images/Blasons/Blason_PJ')) {
      troll.blason_url = 'http://blason.mountyhall.com/Blason_PJ/' + troll.id;
    } else if (troll && !troll.blason_url) {
      troll.blason_url = 'http://blason.mountyhall.com/Blason_PJ/MyNameIsNobody.gif';
    }
  }
  return troll;
};

/*
 * Definition
 */
TrollTemplate.name = 'Troll';
TrollTemplate.table = 'trolls';

TrollTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: 'PrimaryKeyConstraint',
    allowNull: false
  },
  group_id: {
    type: sequelize.INTEGER,
    primaryKey: 'PrimaryKeyConstraint',
    allowNull: false
  },
  user_id: {type: sequelize.INTEGER},
  nom: {type: sequelize.STRING},
  race: {type: sequelize.STRING},
  niv: {type: sequelize.INTEGER},
  nb_kill: {type: sequelize.INTEGER},
  nb_mort: {type: sequelize.INTEGER},
  nb_mouche: {type: sequelize.INTEGER},
  id_guilde: {type: sequelize.INTEGER},
  rang_guilde: {type: sequelize.INTEGER},
  etat: {type: sequelize.STRING},
  pnj: {type: sequelize.BOOLEAN},
  ami_mh: {type: sequelize.BOOLEAN},
  inscription: {type: sequelize.DATE},
  blason_url: {type: sequelize.STRING},
  pos_x: {type: sequelize.INTEGER},
  pos_y: {type: sequelize.INTEGER},
  pos_n: {type: sequelize.INTEGER},
  pv: {type: sequelize.INTEGER},
  bonus_pv_phy: {type: sequelize.INTEGER},
  bonus_pv_mag: {type: sequelize.INTEGER},
  base_pv_max: {type: sequelize.INTEGER},
  bonus_pv_max_phy: {type: sequelize.INTEGER},
  bonus_pv_max_mag: {type: sequelize.INTEGER},
  base_bonus_pv_max: {type: sequelize.INTEGER},
  pa: {type: sequelize.INTEGER},
  dla: {type: sequelize.DATE},
  base_att: {type: sequelize.INTEGER},
  bonus_att_phy: {type: sequelize.INTEGER},
  bonus_att_mag: {type: sequelize.INTEGER},
  base_esq: {type: sequelize.INTEGER},
  bonus_esq_phy: {type: sequelize.INTEGER},
  bonus_esq_mag: {type: sequelize.INTEGER},
  base_deg: {type: sequelize.INTEGER},
  bonus_deg_phy: {type: sequelize.INTEGER},
  bonus_deg_mag: {type: sequelize.INTEGER},
  base_reg: {type: sequelize.INTEGER},
  bonus_reg_phy: {type: sequelize.INTEGER},
  bonus_reg_mag: {type: sequelize.INTEGER},
  base_vue: {type: sequelize.INTEGER},
  bonus_vue_phy: {type: sequelize.INTEGER},
  bonus_vue_mag: {type: sequelize.INTEGER},
  base_arm_phy: {type: sequelize.INTEGER},
  malus_base_arm_phy: {type: sequelize.INTEGER},
  bonus_arm_phy: {type: sequelize.INTEGER},
  bonus_arm_mag: {type: sequelize.INTEGER},
  base_mm: {type: sequelize.INTEGER},
  bonus_mm_phy: {type: sequelize.INTEGER},
  bonus_mm_mag: {type: sequelize.INTEGER},
  base_rm: {type: sequelize.INTEGER},
  bonus_rm_phy: {type: sequelize.INTEGER},
  bonus_rm_mag: {type: sequelize.INTEGER},
  nb_att_sub: {type: sequelize.INTEGER},
  fatigue: {type: sequelize.INTEGER},
  intangible: {type: sequelize.BOOLEAN},
  camouflage: {type: sequelize.BOOLEAN},
  invisible: {type: sequelize.BOOLEAN},
  immobile: {type: sequelize.BOOLEAN},
  terre: {type: sequelize.BOOLEAN},
  course: {type: sequelize.BOOLEAN},
  levite: {type: sequelize.BOOLEAN},
  nb_parade_prog: {type: sequelize.INTEGER},
  nb_ctr_att_prog: {type: sequelize.INTEGER},
  base_tour: {type: sequelize.INTEGER},
  bonus_tour_phy: {type: sequelize.INTEGER},
  bonus_tour_mag: {type: sequelize.INTEGER},
  base_poids: {type: sequelize.INTEGER},
  malus_poids_phy: {type: sequelize.INTEGER},
  malus_poids_mag: {type: sequelize.INTEGER},
  base_concentration: {type: sequelize.INTEGER},
  bonus_concentration_phy: {type: sequelize.INTEGER},
  bonus_concentration_mag: {type: sequelize.INTEGER},
  pi: {type: sequelize.INTEGER},
  nb_retraite_prog: {type: sequelize.INTEGER},
  dir_retraite: {type: sequelize.STRING}
};

TrollTemplate.modelOptions = {
  name: {
    singular: 'troll',
    plural: 'trolls'
  },
  hooks: {
    afterFind: TrollTemplate.changeBlasonURL
  }
};
module.exports = TrollTemplate;

