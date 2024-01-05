# -*- coding: utf-8 -*-
"""Tests Cotation."""

from extranatapi import Cotation, Nageur


def test_cotation_Messieur_NL():

    cotation = Cotation()

    # 50 NL	00:31.14	(41 ans)	770 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=41), nage='50 NL', temps='0.3114')
    assert res == 770

    # 100 NL	01:09.61	(41 ans)	717 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=41), nage='100 NL', temps='1.0961')
    assert res == 717

    # 200 NL	02:41.00	(40 ans)	579  pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=40), nage='200 NL', temps='2.4100')
    assert res == 579

    # 200 NL	02:40.64	(43 ans)	521 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=40), nage='200 NL', temps='2.4064', coeff_enable=False)
    assert res == 521

    # 200 NL	02:46.37	(42 ans)	518 pts     -  50 m
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=42), nage='200 NL', temps='2.4637')
    assert res == 518

    # 400 NL	06:08.61	(42 ans)	407 pts     -  50 m
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=42), nage='400 NL', temps='6.0861')
    assert res == 407

    # 800 NL	12:20.70	(41 ans)	462 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=41), nage='800 NL', temps='12.2070')
    assert res == 462


def test_cotation_Messieur_Dos():

    cotation = Cotation()

    # 50 Dos	00:41.41	(43 ans)	539 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=43), nage='50 Dos', temps='0.4141')
    assert res == 539

    # 100 Dos	01:27.64	(44 ans)	553 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=44), nage='100 Dos', temps='1.2764')
    assert res == 553

    # 200 Dos 03:12.86		(44 ans)	397 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=44), nage='200 Dos', temps='3.1286', coeff_enable=False)
    assert res == 397

    # 200 Dos	03:09.55	(43 ans)	425 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=43), nage='200 Dos', temps='3.0955', coeff_enable=False)
    assert res == 425


def test_cotation_Messieur_Brasse():

    cotation = Cotation()

    # 50 Bra.	00:43.39	(45 ans)	628 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=45), nage='50 Bra.', temps='0.4339')
    assert res == 628


def test_cotation_Messieur_4N():

    cotation = Cotation()

    # 100 4 N.	01:23.65	(40 ans)	622 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=40), nage='100 4 N.', temps='1.2365')
    assert res == 622

    # 200 4 N.	03:02.65	(41 ans)	558 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=41), nage='200 4 N.', temps='3.0265')
    assert res == 558


def test_cotation_Messieur_Pap():

    cotation = Cotation()

    # 50 Pap.	00:37.58	(42 ans)	537 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='M', age=42), nage='50 Pap.', temps='0.3758')
    assert res == 537


def test_cotation_Dames_NL():

    cotation = Cotation()

    # 50 NL	00:41.11	(14 ans)	366 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=14), nage='50 NL', temps='0.4111')
    assert res == 366

    # 50 NL	00:38.47	(45 ans)	586 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=45), nage='50 NL', temps='0.3847')
    assert res == 586

    # 100 NL	01:35.39	(14 ans)	221 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=14), nage='100 NL', temps='1.3539')
    assert res == 221

    # 100 NL	01:27.37	(41 ans)	445 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=41), nage='100 NL', temps='1.2737')
    assert res == 445

    # 200 NL	03:44.33	(13 ans)	141 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=13), nage='200 NL', temps='3.4433')
    assert res == 141

    # 200 NL	03:12.98	(42 ans)	450 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=42), nage='200 NL', temps='3.1298')
    assert res == 450

    # 400 NL	06:39.35	(43 ans)	455 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=43), nage='400 NL', temps='6.3935')
    assert res == 455


def test_cotation_Dames_Dos():

    cotation = Cotation()

    # 50 Dos	00:45.83	(14 ans)	461 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=14), nage='50 Dos', temps='0.4583')
    assert res == 461

    # 50 Dos	00:46.66	(44 ans)	516 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=44), nage='50 Dos', temps='0.4666')
    assert res == 516

    # 100 Dos	01:39.63	(14 ans)	407 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=14), nage='100 Dos', temps='1.3963')
    assert res == 407

    # 200 Dos	03:52.69	(13 ans)	231 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=13), nage='200 Dos', temps='3.5269')
    assert res == 231


def test_cotation_Dames_Brasse():

    cotation = Cotation()

    # 50 Bra.	01:02.30	(14 ans)	132 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=14), nage='50 Bra.', temps='1.0230')
    assert res == 132

    # 50 Bra.	00:52.03	(41 ans)	470 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=41), nage='50 Bra.', temps='0.5203')
    assert res == 470

    # 100 Bra.	02:18.11	(13 ans)	138 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=13), nage='100 Bra.', temps='2.1811')
    assert res == 138


def test_cotation_Dames_Pap():

    cotation = Cotation()

    # 50 Pap.	00:52.05	(14 ans)	145 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=14), nage='50 Pap.', temps='0.5205')
    assert res == 145

    # 50 Pap.	00:50.53	(43 ans)	258 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=43), nage='50 Pap.', temps='0.5053')
    assert res == 258


def test_cotation_Dames_4N():

    cotation = Cotation()

    # 100 4 N.	01:59.45	(13 ans)	143 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=13), nage='100 4 N.', temps='1.5945')
    assert res == 143

    # 100 4 N.	01:43.29	(41 ans)	441 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=41), nage='100 4 N.', temps='1.4329')
    assert res == 441

    # 200 4 N.	03:47.84	(43 ans)	255 pts
    res = cotation.get_cotation_nageur(Nageur(name='test', sexe='F', age=43), nage='200 4 N.', temps='3.4784', coeff_enable=False)
    assert res == 255
