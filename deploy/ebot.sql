PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
	id VARCHAR(10) NOT NULL, 
	email VARCHAR, 
	user_id INTEGER, 
	user_name VARCHAR, 
	first_name VARCHAR, 
	last_name VARCHAR, 
	level VARCHAR, 
	enabled BOOLEAN, 
	PRIMARY KEY (id), 
	CHECK (enabled IN (0, 1))
);
INSERT INTO "users" VALUES('NhzdzEMHDA','a.shutov@msk.enforta.com',168160767,NULL,'Andrey','Shutov','user',1);
INSERT INTO "users" VALUES('YSWrBIAiiP','d.iliyuschenko@enforta.com',452126992,NULL,'Dmitry','Ilyuschenko','user',1);
INSERT INTO "users" VALUES('ckKouULJxA','v.losev@enforta.com',255329414,'losev_vasiliy','Василий','Лосев','user',1);
INSERT INTO "users" VALUES('jKOWULWcwp','v.chernopazov@lpk.enforta.com',208126891,'vchernopazov','Vitaliy','Chernopazov','user',1);
INSERT INTO "users" VALUES('SlloEnrBVh','o.kondratev@krd.enforta.com',430840473,NULL,'Oleg','Kondratev','user',1);
INSERT INTO "users" VALUES('kXkNcslPVS','m.bondarenko@enforta.com',388360365,NULL,'Максим','Бондаренко','user',1);
INSERT INTO "users" VALUES('neKtaLnMiv','a.kondratiev@srk.enforta.com',482353500,NULL,'Алексей','Кондратьев','user',1);
INSERT INTO "users" VALUES('vzJlhCfRnH','i.singosin@msk.enforta.com',42561047,'nimbo78','nimbo78',NULL,'user',1);
INSERT INTO "users" VALUES('uQsUMzTiQH','a.belan@enforta.com',442333736,NULL,'Aleksey','Belan','user',1);
INSERT INTO "users" VALUES('EwUOQkhDLH','a.topolov@krd.enforta.com',455524336,NULL,'Алексей','Тополов','user',1);
INSERT INTO "users" VALUES('oOJxCCoawI','s.bryukhov@enforta.com',364672794,NULL,'Сергей','Брюхов','user',1);
INSERT INTO "users" VALUES('IADubNbZCr','s.rybkin@enforta.com',406068793,NULL,'Sergey','Rybkin','user',1);
INSERT INTO "users" VALUES('gFoStUfWcY','m.chen@enforta.com',195819500,'Maksimilli0n','Chen','Maksim','user',1);
INSERT INTO "users" VALUES('rmrNHkiOAe','k.rogozhin@srk.enforta.com',384160182,'rokon4eg','Константин','Рогожин','user',1);
INSERT INTO "users" VALUES('LYIORMHWqr','i.bratykin@yrl.enforta.com',376554419,'Ilyabratykin','Ilya','Bratykin','user',0);
INSERT INTO "users" VALUES('lmkVEQeUWF','e.molostov@enforta.com',468929261,NULL,'Eu','Mo','user',1);
INSERT INTO "users" VALUES('OZMDreYtql','y.dmitrenko@nsk.enforta.com',189766950,NULL,'Q',NULL,'user',1);
INSERT INTO "users" VALUES('iHsNtDGJNb','v.tarasov@krv.enforta.com',499085665,NULL,'Владимир','Тарасов','user',1);
INSERT INTO "users" VALUES('qHydNsntri','r.taktarov@pnz.enforta.com',362261560,NULL,'Radik','Taktarov','user',0);
INSERT INTO "users" VALUES('HNEZJAODso','a.yalovik@krd.enforta.com',340968583,'AlexanderFox','Alexander','Y','user',1);
INSERT INTO "users" VALUES('RFURWVUAbU','roman.leshchuk@domru.ru',391158244,'rleschuk','Roman','Leschuk','admin',1);
INSERT INTO "users" VALUES('wNmJUTdKOr','s.pogorelov@vvk.enforta.com',31235557,NULL,'Станислав','Погорелов','user',1);
INSERT INTO "users" VALUES('ulKkOqRXYb','d.belozerov@enforta.com',430019684,NULL,'Дмитри','Белозеров','user',0);
INSERT INTO "users" VALUES('nIFvicZpTE','stepan.popov@enforta.com',360674114,'Step249','Stepan','Popov','user',1);
INSERT INTO "users" VALUES('WmOYcCcxFn','y.sosnovsky@srt.enforta.com',447734520,'Sosnovsky_yiriy','Yuriy','Sosnovskiy','admin',1);
INSERT INTO "users" VALUES('UzwgtaXdiG','a.shapovalenko@enforta.com',449155910,NULL,'Aleksandr',NULL,'user',1);
INSERT INTO "users" VALUES('OlDBHekwUT','i.shibanov@srt.enforta.com',416109171,NULL,'Игорь','Шибанов','user',1);
INSERT INTO "users" VALUES('LUrCqoKHQM','d.orlov@rzn.enforta.com',297198017,'Dmitrydetected','Dmitry','Orlov','user',1);
INSERT INTO "users" VALUES('hzoBSbSOdR','d.kuznetcov@yrl.enforta.com',366956780,NULL,'dkuznetcov',NULL,'user',1);
INSERT INTO "users" VALUES('CNKaZhesyk','d.tabelek@sha.enforta.com',452075579,NULL,'Дмитрий','Табелек','user',1);
INSERT INTO "users" VALUES('GwiBLzoDGz','andrei.pelevin@enforta.com',339318776,'dr_proton','Андрей','Пелевин','user',1);
INSERT INTO "users" VALUES('xCIVPWpcjg','andrei.liu@enforta.com',384751469,NULL,'Andrey','Liu','user',1);
INSERT INTO "users" VALUES('JSiHzScrsy','d.salmin@enforta.com',221791740,NULL,'d.salmin','/enforta.com/','user',1);
INSERT INTO "users" VALUES('dstscztEDl','oleg.iu.gurov@enforta.com',442921552,NULL,'Oleg','Gurov','user',1);
INSERT INTO "users" VALUES('snKZsuigPl','m.gasretov@mhc.enforta.com',471507996,'mikail7121','Muslim','Gasretov','user',1);
INSERT INTO "users" VALUES('pJwFmOlgRQ','a.sitnikov@msk.enforta.com',274528628,'asitnikov26','Aleksandr',NULL,'user',1);
INSERT INTO "users" VALUES('LuDNygxfUf','o.shumarin@msk.enforta.com',386436216,'Oleg_Shumarin','Олег',NULL,'user',0);
INSERT INTO "users" VALUES('bNSnfPgYXn','i.kiryanov@msk.enforta.com',342271655,NULL,'Ivan','Kiryanov','user',1);
INSERT INTO "users" VALUES('lIphPuLnEd','s.gusev@msk.enforta.com',257597295,'Gusev_S','Sergey','Gusev','user',1);
INSERT INTO "users" VALUES('adgaYBXvLZ','n.maiorov@msk.enforta.com',394642765,'NickMayor','Nick','Mayor','user',1);
INSERT INTO "users" VALUES('PXgyfPJlOx','feliks.moiseev@enforta.com',436468068,'Felix_Moiseev','Felix',NULL,'user',1);
INSERT INTO "users" VALUES('ivvQWpszoY','anastasiia.barabanova@domru.ru',327329576,NULL,'Анастасия','Барабанова','user',1);
INSERT INTO "users" VALUES('YbzgXoPYwy','roman.mogilatov@enforta.com',303393178,'mogilatov','Роман','Могилатов','user',1);
INSERT INTO "users" VALUES('OHfFQSwipd','dmitrii.butenko@enforta.com',45660325,NULL,'Dmitry','Butenko','user',1);
INSERT INTO "users" VALUES('cHKSdqbEjN','afanasii.beliushin@domru.ru',328485370,'Afonya_1991','Afanasiy','Belyushin','user',1);
INSERT INTO "users" VALUES('yqZkNqaDEn','s.monchenko@enforta.com',422738602,'Shad0w_87','Sergey','Monchenko','user',1);
INSERT INTO "users" VALUES('bsIcYUIIPk','petr.kolotov@domru.ru',173282099,'diablozzz36','Petr','Kolotov','user',1);
INSERT INTO "users" VALUES('SgZoBDmmiw','v.kukushkina@enforta.com',385620547,'me444ta','Veronika','Kukushkina','user',1);
INSERT INTO "users" VALUES('dHaizHwjJU','n.novoselova@enforta.com',389300272,'natalie356vo','Natalya','Novoselova','user',1);
INSERT INTO "users" VALUES('lYFrWGwBgH','andrei.golushkov@enforta.com',472813596,NULL,'Andrey','Golushkov','user',1);
INSERT INTO "users" VALUES('WZenvPKtNF','mikhail.kushov@enforta.com',596803282,NULL,'Михаил','Кушов','user',1);
INSERT INTO "users" VALUES('BLSTXGHBEu','t.lalyko@enforta.com',483477265,NULL,'Tatyana','Rozhnovskaya','user',1);
INSERT INTO "users" VALUES('adTfLURNJK','bakhti.baimukhamedov@domru.ru',326070831,'EndlessNights','Бахти','Великолепный','user',1);
INSERT INTO "users" VALUES('PqeacjCXVY','evgenii.litvinov@enforta.com',519289507,NULL,'Евгений Л.',NULL,'user',1);
INSERT INTO "users" VALUES('fTDBodeztD','d.ryabuha@khb.enforta.com',136670752,'Dmitriy_Enforta','Dmitriy',NULL,'user',1);
INSERT INTO "users" VALUES('XjOMqOomjY','maksim.kobzar@enforta.com',132719160,'mkobzz','Maksim','Kobzar','user',1);
INSERT INTO "users" VALUES('AyYdZjMXtO','sergei.alekseev@domru.ru',209948520,'aleksgrey','Sergey','Alekseev R16 +3 GMT MSK','user',1);
INSERT INTO "users" VALUES('RddDgpZBYu','a.skudarnova@enforta.com',429602910,NULL,'Anna','Skudarnova','user',1);
INSERT INTO "users" VALUES('UyrIhuNUQB','s.burtcev@enforta.com',410319727,'s_burtsev_sha','Sergey','Burtsev','user',1);
INSERT INTO "users" VALUES('tHEwgvPtrX','f.krupin@enforta.com',263823016,NULL,'phil',NULL,'user',1);
INSERT INTO "users" VALUES('LWLzdWkbUL','a.dunin@srt.enforta.com',547557224,NULL,'Антон',NULL,'user',1);
INSERT INTO "users" VALUES('PDhKjZuyei','a.uspenskii@enforta.com',337772624,'Lexusk015yo','Алексей','Успенский','user',1);
INSERT INTO "users" VALUES('VRFYteisZd','daria.polozhentceva@domru.ru',685928326,NULL,'Darya','Polozhentseva','user',1);
INSERT INTO "users" VALUES('XuwWwRvkRV','n.zotov@enforta.com',446599113,NULL,'Nikolay Zotov','Nikolay Zotov','user',1);
INSERT INTO "users" VALUES('boAdpMWQtg','k.petrov@rzn.enforta.com',241488723,'yazlodey','Konstantin','Petrov','user',1);
INSERT INTO "users" VALUES('nEOjKKgFOf','mikhail.denisenko@enforta.com',553459631,'Mikhail_Denisenko','Михаил','Денисенко','user',1);
INSERT INTO "users" VALUES('OQMjPwuIvR','v.maksushina@enforta.com',432504251,NULL,'Виктория','Максюшина','user',1);
INSERT INTO "users" VALUES('vJiuQnEaDx','maksim.chirkin@domru.ru',555146881,'Maksim_GKU_Samara','Чиркин','Максим','user',1);
INSERT INTO "users" VALUES('tXSCxHormp','kirill.golovanov@enforta.ru',330486361,NULL,'Kirill','Golovanov','user',1);
COMMIT;
