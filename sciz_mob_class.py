#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import sciz_globals as sg

# Class of a Mob
class MOB(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'mobs'
    id = Column(Integer, primary_key=True)                  # Identifiant unique du monstre
    sciz_notif = Column(Boolean)                            # SCIZ notifs ?
    metamob_id = Column(Integer, ForeignKey('metamobs.id')) # Metamob ID
    nom = Column(String(50))                                # Nom (incluant modificateurs)
    type = Column(String(50))                               # Type (Race) du monstre
    tag = Column(String(50))                                # Tatouage
    age = Column(String(50))                                # Age
    blessure = Column(Integer)                              # Pourcentage de blessure
    niv_min = Column(Integer)                               # Niveau minimum
    niv_max = Column(Integer)                               # Niveau maximum
    pv_min = Column(Integer)                                # Points de Vie minimum
    pv_max = Column(Integer)                                # Points de Vie maximum
    att_min = Column(Integer)                               # Attaque minimum en D6
    att_max = Column(Integer)                               # Attaque maximum en D6
    esq_min = Column(Integer)                               # Esquive minimum en D6
    esq_max = Column(Integer)                               # Esquive maximum en D6
    deg_min = Column(Integer)                               # Dégâts minimum en D3
    deg_max = Column(Integer)                               # Dégâts maximum en D3
    reg_min = Column(Integer)                               # Régénération minimum en D3
    reg_max = Column(Integer)                               # Régénération maximum en D3
    arm_phy_min = Column(Integer)                           # Armure physique minimum
    arm_phy_max = Column(Integer)                           # Armure physique maximum
    vue_min = Column(Integer)                               # Vue minimum en nombre de cases
    vue_max = Column(Integer)                               # Vue maximum en nombre de cases
    capa_desc = Column (String(150))                        # Descritpion de la capacité spéciale
    capa_effet = Column (String(150))                       # Effet de la capacité spéciale
    capa_tour = Column (Integer)                            # Nombre de tours d'effet de la capacité spéciale
    mm_min = Column(Integer)                                # Maitrise Magique minimum
    mm_max = Column(Integer)                                # Maitrise Magique maximum
    rm_min = Column(Integer)                                # Résistance Magique minimum
    rm_max = Column(Integer)                                # Résistance Magique maximum
    nb_att_tour = Column(Integer)                           # Nombre d'attaque par tour
    vit_dep = Column(String(10))                            # Vitesse de déplacement
    vlc = Column(Boolean)                                   # Voir la caché ?
    att_dist = Column(Boolean)                              # Attaque à distance ?
    
    # Relationships
    cdms = relationship("CDM", back_populates="mob")
    metamob = relationship("METAMOB", back_populates="mobs")
    att_events = relationship("BATTLE_EVENT", foreign_keys = '[BATTLE_EVENT.att_mob_id]', back_populates="att_mob")
    def_events = relationship("BATTLE_EVENT", foreign_keys = '[BATTLE_EVENT.def_mob_id]', back_populates="def_mob")

    # Constructor
    # Handled by SqlAlchemy, accept keywords names matching the mapped columns, do not override
    
    # Loop over every metamobs in the list to find the longest one matching the mob name...
    def link_metamob(self, metamobs):
        result_id = -1
        result_nom = ''
        if self.nom != None:
            for metamob in metamobs:
                if metamob.nom in self.nom and len(metamob.nom) > len(result_nom):
                    result_nom = metamob.nom
                    result_id = metamob.id
            if result_id > 0:
                self.metamob_id = result_id
            else:
                print 'Cannot match name of mob to a metamob'
        else:
            print 'Mob has no name, cannot search for a metamob to link'

    # Populate object from a CDM
    def populate_from_cdm(self, obj):
        self.id = obj.mob_id
        self.nom = obj.mob_name
        self.tag = obj.mob_tag
        self.age = obj.mob_age
        sg.copy_properties(obj, self, ['type', 'blessure', 'niv_min', 'niv_max', 'pv_min', 'pv_max', 'att_min', 'att_max', 'esq_min', 'esq_max', 'deg_min', 'deg_max', 'reg_min', 'reg_max', 'arm_phy_min', 'arm_phy_max', 'vue_min', 'vue_max', 'capa_desc', 'capa_effet', 'capa_tour', 'mm_min', 'mm_max', 'rm_min', 'rm_max', 'nb_att_tour', 'vit_dep', 'vlc', 'att_dist'], True)

    # Update mob definition with the more accurate value
    def update_from_new(self, mob):
        sg.copy_properties(mob, self, ['age', 'blessure', 'capa_desc', 'capa_effet', 'capa_tour', 'nb_att_tour', 'vit_dep', 'vlc', 'att_dsit'], False)
        
        self.niv_min = sg.do_unless_none((max), (self.niv_min, mob.niv_min))
        self.pv_min = sg.do_unless_none((max), (self.pv_min, mob.pv_min))
        self.att_min = sg.do_unless_none((max), (self.att_min, mob.att_min))
        self.esq_min = sg.do_unless_none((max), (self.esq_min, mob.esq_min))
        self.deg_min = sg.do_unless_none((max), (self.deg_min, mob.deg_min))
        self.reg_min = sg.do_unless_none((max), (self.reg_min, mob.reg_min))
        self.arm_phy_min = sg.do_unless_none((max), (self.arm_phy_min, mob.arm_phy_min))
        self.vue_min = sg.do_unless_none((max), (self.vue_min, mob.vue_min))
        self.mm_min = sg.do_unless_none((max), (self.mm_min, mob.mm_min))
        self.rm_min = sg.do_unless_none((max), (self.rm_min, mob.rm_min))
        
        self.niv_max = sg.do_unless_none((min), (self.niv_max, mob.niv_max))
        self.pv_max = sg.do_unless_none((min), (self.pv_max, mob.pv_max))
        self.att_max = sg.do_unless_none((min), (self.att_max, mob.att_max))
        self.esq_max = sg.do_unless_none((min), (self.esq_max, mob.esq_max))
        self.deg_max = sg.do_unless_none((min), (self.deg_max, mob.deg_max))
        self.reg_max = sg.do_unless_none((min), (self.reg_max, mob.reg_max))
        self.arm_phy_max = sg.do_unless_none((min), (self.arm_phy_max, mob.arm_phy_max))
        self.vue_max = sg.do_unless_none((min), (self.vue_max, mob.vue_max))
        self.mm_max = sg.do_unless_none((min), (self.mm_max, mob.mm_max))
        self.rm_max = sg.do_unless_none((min), (self.rm_max, mob.rm_max))
