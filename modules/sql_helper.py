#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import ConfigParser
from sqlalchemy import create_engine, exc, orm
from classes.user import USER
from classes.troll import TROLL
from classes.metamob import METAMOB
from classes.mob import MOB
from classes.cdm import CDM
from classes.battle_event import BATTLE_EVENT
from classes.notif import NOTIF
from modules.pretty_printer import PrettyPrinter
import modules.globals as sg

## SCIZ SQL Help

class SQLHelper:

    # Constructor
    def __init__(self, config):
        self.config = config
        self.check_conf()
        self.connect()
        self.pp = PrettyPrinter(config)

    # Configuration loader and checker
    def check_conf(self):
        try:
            # Load DB conf
            self.db_host = self.config.get(sg.CONF_DB_SECTION, sg.CONF_DB_HOST)
            self.db_port = self.config.get(sg.CONF_DB_SECTION, sg.CONF_DB_PORT)
            self.db_name = self.config.get(sg.CONF_DB_SECTION, sg.CONF_DB_NAME)
            self.db_user = self.config.get(sg.CONF_DB_SECTION, sg.CONF_DB_USER)
            self.db_pass = self.config.get(sg.CONF_DB_SECTION, sg.CONF_DB_PASS)
        except ConfigParser.Error as e:
            print('Fail to load config! (ConfigParser error:' + str(e) + ')')
            raise

    # Init the DB
    def init(self):
        try:
            sg.SqlAlchemyBase.metadata.create_all(self.engine)
        except (exc.SQLAlchemyError, exc.DBAPIError) as e:
            print 'Fail to init the DB! (SQLAlchemy error:' + str(e) + ')' 
            raise
    
    # Connect to the DB
    def connect(self):
        try:
            self.engine = create_engine('mysql+mysqldb://' + self.db_user + ':' + self.db_pass + '@' + self.db_host + ':' + self.db_port + '/' + self.db_name + '?charset=utf8', encoding=sg.DEFAULT_CHARSET)
            self.sessionMaker = orm.sessionmaker(bind=self.engine)
            self.session = self.sessionMaker()
        except (exc.SQLAlchemyError, exc.DBAPIError) as e:
            print 'Fail to conect to the DB! (SQLAlchemy error:' + str(e) + ')' 
            raise

    # Add any object (dispatcher)
    def add(self, obj):
        if isinstance(obj, MOB):
            self.__add_mob(obj)
        elif isinstance(obj, CDM):
            self.__add_cdm(obj)
        elif isinstance(obj, TROLL):
            self.__add_troll(obj)
        elif isinstance(obj, BATTLE_EVENT):
            self.__add_battle_event(obj)
        elif isinstance(obj, USER):
            self.__add_user(obj)

    # Add a USER
    def __add_user(self, user_new):
        try:
            user_old = self.session.query(USER).filter(USER.id == user_new.id).one() 
            #FIXME : mode verbose / logger
            #print 'User %s already found, updating but password...' % (user_old.id,) 
            user_old.update_from_new(user_new) 
            self.session.add(user_old) 
        except orm.exc.NoResultFound:
            #FIXME : mode verbose / logger
            #print 'New user %s, creating...' % (user_new.id,)  
            troll = TROLL() 
            troll.id = user_new.id
            troll.sciz_notif = True
            self.__add_troll(troll)
            self.session.add(user_new) 

    # Add a NOTIF
    def add_notif(self, obj):
        notif = NOTIF()
        notif.text = self.pp.pretty_print(obj, True)
        if notif.text:
            if isinstance(obj, CDM) and (not obj.mob.sciz_notif or not obj.troll.sciz_notif):
                notif.to_push = False
            elif isinstance(obj, BATTLE_EVENT) and ((obj.att_troll != None and not obj.att_troll.sciz_notif) or (obj.att_mob != None and not obj.att_mob.sciz_notif) or (obj.def_troll != None and not obj.def_troll.sciz_notif) or (obj.def_mob != None and not obj.def_mob.sciz_notif)):
                notif.to_push = False
            else:
                notif.to_push = True
            self.session.add(notif)
        return notif
        
    # Add a TROLL
    def __add_troll(self, troll_new):
        try:
            troll_old = self.session.query(TROLL).filter(TROLL.id == troll_new.id).one()
            #FIXME : mode verbose / logger
            #print "TROLL %s already found in the DB, updating it with new data" % (troll_old.id, )
            troll_old.update_from_new(troll_new)
            self.session.add(troll_old)
        except orm.exc.NoResultFound:
            #FIXME : mode verbose / logger
            #print "New Troll %s, creating it on the fly" % (troll_new.id, )
            self.session.add(troll_new)
            
    # Add a MOB
    def __add_mob(self, mob_new):
        try:
            mob_old = self.session.query(MOB).filter(MOB.id == mob_new.id).one()
            #FIXME : mode verbose / logger
            #print "MOB %s already found in the DB, updating it with new data" % (mob_old.id, )
            mob_old.update_from_new(mob_new)
            if mob_old.metamob_id == None:
                mob_old.link_metamob(self.session.query(METAMOB).all())
            self.session.add(mob_old)
        except orm.exc.NoResultFound:
            #FIXME : mode verbose / logger
            #print "New MOB %s, creating it on the fly" % (mob_new.id, )
            mob_new.sciz_notif = True
            mob_new.link_metamob(self.session.query(METAMOB).all())
            self.session.add(mob_new)

    # Add a CDM
    def __add_cdm(self, cdm):
        mob = MOB()
        mob.populate_from_cdm(cdm)
        self.__add_mob(mob)
        troll = TROLL()
        troll.id = cdm.troll_id
        self.__add_troll(troll)
        self.session.add(cdm)
    
    # Add a BATTLE_EVENT
    def __add_battle_event(self, event):
        if event.att_troll_id != None:
            att_troll = TROLL()
            att_troll.id = event.att_troll_id
            att_troll.nom = event.att_troll_nom
            self.__add_troll(att_troll)
        if event.def_troll_id != None:
            def_troll = TROLL()
            def_troll.id = event.def_troll_id
            def_troll.nom = event.def_troll_nom
            if event.att_mob_id != None: # Pas d'info en TvT
                def_troll.pv = event.vie
            self.__add_troll(def_troll)
        if event.att_mob_id != None:
            att_mob = MOB()
            att_mob.id = event.att_mob_id
            att_mob.nom = event.att_mob_nom
            att_mob.age = event.att_mob_age
            att_mob.tag = event.att_mob_tag
            self.__add_mob(att_mob)
        if event.def_mob_id != None:
            def_mob = MOB()
            def_mob.id = event.def_mob_id
            def_mob.nom = event.def_mob_nom
            def_mob.age = event.def_mob_age
            def_mob.tag = event.def_mob_tag
            self.__add_mob(def_mob)
        self.session.add(event)

    # Destructor
    def __del__(self):
        pass