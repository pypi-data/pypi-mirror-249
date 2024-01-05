# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Tests Recherche Equipe."""

import os

from extranatapi import RechercheEquipe, FileTools

TEST_EQUIPE_ALL = [
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}]
]

TEST_EQUIPE_M = [
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}]
]

TEST_EQUIPE_F = [
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}]
]


TEST_EQUIPE_1 = [
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
]


TEST_EQUIPE_2 = [
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur_f12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur1': {'nage': '800 NL', 'points': 1500}}, {'nageur_f10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
    [{'nageur_f6': {'nage': '50 NL', 'points': 1500}}, {'nageur_f1': {'nage': '800 NL', 'points': 1500}}, {'nageur10': {'nage': '50 Bra.', 'points': 1500}}, {'nageur12': {'nage': '200 Bra.', 'points': 1500}}],
]


TEST_NAGES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'competition_nages.csv')
TEST_NAGEURS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'competition_nageurs.csv')
TEST_POINTS = 6000


def __search__(results, result_point, max_dames, max_messieurs):

    fileTools = FileTools()
    nageurs = fileTools.read_equipe_nageurs(TEST_NAGEURS_FILE)
    nages = fileTools.read_equipe_nages(TEST_NAGES_FILE)

    searchteam = RechercheEquipe()

    if searchteam.check_before_search(nages, nageurs):
        searchteam.search(nages, nageurs, [], 0, max_dames, max_messieurs)

        # Tests
        assert searchteam.__result_points__ == result_point
        assert len(searchteam.__result_equipe__) == len(results)
        index_nageurs = 0
        for item_nageurs in searchteam.__result_equipe__:
            index_nageur = 0
            for item_nageur in item_nageurs:
                assert item_nageur == results[index_nageurs][index_nageur]
                index_nageur += 1
            index_nageurs += 1


def test_equipe_all():

    __search__(TEST_EQUIPE_ALL, TEST_POINTS, 4, 4)


def test_equipe_M():

    __search__(TEST_EQUIPE_M, TEST_POINTS, 0, 4)


def test_equipe_F():

    __search__(TEST_EQUIPE_F, TEST_POINTS, 4, 0)


def test_equipe_1():

    __search__(TEST_EQUIPE_1, TEST_POINTS, 3, 3)


def test_equipe_2():

    __search__(TEST_EQUIPE_2, TEST_POINTS, 2, 2)
