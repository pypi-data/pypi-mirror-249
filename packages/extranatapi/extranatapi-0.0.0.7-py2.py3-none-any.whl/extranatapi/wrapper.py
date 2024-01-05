# -*- coding: utf-8 -*-
# Structures: https://ffn.extranat.fr/webffn/structures.php
# Competition: https://ffn.extranat.fr/webffn/competitions.php?idact=nat
# Performance: https://ffn.extranat.fr/webffn/nat_recherche.php?idact=nat
"""Wrapper."""

import urllib
import urllib.request
import sys
from bs4 import BeautifulSoup

from .base import ExtranatObjectCollection
from .competition import Competition
from .location import Region, Departement, Club
from .nageur import Nageur
from .saison import Saison


class Wrapper():
    """CLASS : Wrapper."""

    def __init__(self, showprogress=False):
        """Constructor."""
        self.__region_exception__ = {'25': '988', '26': '971', '27': '972', '28': '973', '29': '974', '30': '987'}
        self.__showprogress__ = showprogress

    @staticmethod
    def __get_parameter__(text, name, default=None):
        """Get parameter."""
        result = default

        start = text.find(name)
        if start >= 0:
            len_name = len(name) + 1
            tmp = text[start + len_name:]
            end = tmp.find("&")
            if end >= 0:
                tmp = tmp[:end]
            result = tmp.strip()

        return result

    @staticmethod
    def __filter_endchar__(text, sfilter):
        """Filter with a end char."""
        result = text

        start = text.find(sfilter)
        if start >= 0:
            result = text[:start]

        return result.strip()

    @staticmethod
    def __filter_beginchar__(text, sfilter):
        """Filter with a begin char."""
        result = text

        start = text.find(sfilter)
        if start >= 0:
            result = text[start + 1:]

        return result.strip()

    def __progress__(self, text):
        if self.__showprogress__:
            sys.stdout.write("\r\x1b[K" + text)
            sys.stdout.flush()

    def get_regions(self):
        """Get regions."""
        # https://ffn.extranat.fr/webffn/structures.php
        results = ExtranatObjectCollection(Region())

        cmd = 'https://ffn.extranat.fr/webffn/structures.php'
        with urllib.request.urlopen(cmd) as url2:  # nosec

            bsdata = BeautifulSoup(url2.read(), 'html.parser')
            items = bsdata.find_all('a')
            for item in items:
                if 'href' in item.attrs:
                    val = item['href']
                    if val.find('structures.php') >= 0:
                        idreg = self.__get_parameter__(val, 'idreg')

                        if idreg is not None:
                            idstruct = self.__get_parameter__(val, 'idstruct')
                            name = self.__filter_endchar__(item.text, '(')

                            results.append(Region(idreg, idstruct, name))

        return results

    def get_departements(self):
        """Get Departements."""
        # https://ffn.extranat.fr/webffn/structures.php
        results = ExtranatObjectCollection(Departement())

        regions = self.get_regions()

        for region in regions:

            self.__progress__(region.name)

            if region.idreg in self.__region_exception__:
                results.append(Departement(self.__region_exception__[region.idreg], region.idstruct, region.name, region))
            else:
                cmd = f'https://ffn.extranat.fr/webffn/structures.php?idreg={region.idreg}&idstruct={region.idstruct}'
                with urllib.request.urlopen(cmd) as url2:  # nosec

                    bsdata = BeautifulSoup(url2.read(), 'html.parser')
                    items = bsdata.find_all('a')
                    for item in items:
                        if 'href' in item.attrs:
                            val = item['href']
                            if val.find('structures.php') >= 0:
                                idreg = self.__get_parameter__(val, 'idreg')

                                if idreg is not None:
                                    idstruct = self.__get_parameter__(val, 'idstruct')
                                    iddep = self.__get_parameter__(val, 'iddep')
                                    name = self.__filter_endchar__(item.text, '(')

                                    results.append(Departement(iddep, idstruct, name, region))

        self.__progress__('')

        return results

    def get_clubs(self):
        """Get clubs."""
        # https://ffn.extranat.fr/webffn/structures.php
        results = ExtranatObjectCollection(Club())

        departements = self.get_departements()

        for departement in departements:

            self.__progress__(departement.region.name + ' / ' + departement.name)

            cmd = f'https://ffn.extranat.fr/webffn/structures.php?idreg={departement.region.idreg}&idstruct={departement.idstruct}&iddep={departement.iddep}'
            with urllib.request.urlopen(cmd) as url2:  # nosec

                bsdata = BeautifulSoup(url2.read(), 'html.parser')
                # items = bsdata.find_all('td', {"class": "soustitrecfr"})
                items = bsdata.find_all('font', {"color": "#000000"})
                for item in items:
                    if item.text.find('Nom usuel') >= 0:
                        name = self.__filter_beginchar__(self.__filter_endchar__(item.text, '('), ':')
                        idclub = self.__filter_beginchar__(self.__filter_endchar__(item.text, ')'), '(')
                        index = idclub.rfind(' ')
                        if index >= 0:
                            idclub = idclub[index:]
                        results.append(Club(idclub=idclub, name=name, departement=departement))

        self.__progress__('')

        return results

    def get_saison(self, idclub, annee):
        """Get saison (filtre: idclub / annee)."""
        result = Saison(idclub=idclub, saison=annee)

        result.__competitions__ = self.get_competitions(idclub, annee)

        return result

    def get_competitions(self, idclub, annee):
        """Get competitions (filtre: idclub / annee)."""
        # https://ffn.extranat.fr/webffn/competitions.php?idact=nat&idrch=str%7C{idclub}&idann={annee}
        results = ExtranatObjectCollection(Competition())

        cmd = f"https://ffn.extranat.fr/webffn/competitions.php?idact=nat&idrch=str%7C{idclub}&idann={annee}"

        with urllib.request.urlopen(cmd) as url2:  # nosec

            bsdata = BeautifulSoup(url2.read(), 'html.parser')
            items = bsdata.find_all('a')
            for item in items:
                if "href" in item.attrs:
                    val = item["href"]
                    if val.find("resultats.php") >= 0:
                        self.__progress__(item.text)
                        idcpt = val[val.find("idcpt") + 6:]
                        compet = Competition(idclub, idcpt, item.text)
                        compet.__date__ = item.parent.parent.find('span').text
                        compet.nageurs = self.get_nageur_from_competition(idcpt, idclub)
                        results.append(compet)

        self.__progress__('')

        return results

    def get_nageur_from_competition(self, idcpt, idclub):
        """Get Nageur from a competition."""
        # https://ffn.extranat.fr/webffn/resultats.php?idact=nat&idcpt={idcpt}&go=res&idclb={idclub}
        cmd = f"https://ffn.extranat.fr/webffn/resultats.php?idact=nat&idcpt={idcpt}&go=res&idclb={idclub}"

        results = ExtranatObjectCollection(Nageur())

        with urllib.request.urlopen(cmd) as url2:  # nosec

            bsdata = BeautifulSoup(url2.read(), 'html.parser')

            # nageurs
            items = bsdata.find_all('tr')
            index = 0

            nageur = None
            for item in items:
                if index > 2:
                    tditems = item.find_all('td')
                    if item.parent.name != "thead":
                        nageur.addnage(
                            nage=tditems[1].text.strip(),
                            classement=tditems[0].text,
                            temps=tditems[4].text,
                            points=tditems[6].text)
                elif index == 2:
                    nageur = self.__create_nageur_from_tr(item)
                    results.append(nageur)
                    self.__progress__(nageur.name)

                index += 1

        self.__progress__('')

        return results

    def __create_nageur_from_tr(self, item):

        nageur = Nageur()

        # name
        nageur.setnamewithinfo(item.text)
        # sexe
        if item.find('i', {'class': 'fa-venus'}) is None:
            nageur.__sexe__ = 'M'
        else:
            nageur.__sexe__ = 'F'

        return nageur

    def __get_nageur_bage_from_tr(self, tritems, nageur):

        # nages
        bassin = '0'
        for item in tritems:
            thitems = item.find_all('th')
            tditems = item.find_all('td')

            if len(tditems) <= 3:
                if "Bassin : 50" in thitems[0].text:
                    bassin = '50'
                elif "Bassin : 25" in thitems[0].text:
                    bassin = '25'
                else:
                    bassin = '0'
            else:
                nageur.addnage(
                    nage=thitems[0].text,
                    classement=None,
                    temps=tditems[0].text,
                    points=tditems[2].text,
                    bassin=bassin,
                    date=tditems[4].text)

    def get_nageur_mpp(self, iuf):
        """Get Nageur (Meilleures Performances Personnelles)."""
        # https://ffn.extranat.fr/webffn/nat_recherche.php?idrch_id={iuf}&idopt=mpp
        cmd = f"https://ffn.extranat.fr/webffn/nat_recherche.php?idrch_id={iuf}&idopt=mpp"

        self.__progress__(f'{iuf}')

        with urllib.request.urlopen(cmd) as url2:  # nosec

            bsdata = BeautifulSoup(url2.read(), 'html.parser')
            item = bsdata.find("h5")

            # nageur
            nageur = self.__create_nageur_from_tr(item)
            if nageur.name == '[]':
                self.__progress__('')
                return None
            self.__progress__(nageur.name)

            # nages
            self.__get_nageur_bage_from_tr(bsdata.find_all('tr'), nageur)

        self.__progress__('')

        return nageur

    def get_nageur_all(self, iuf):
        """Get Nageur (Meilleures Performances Personnelles)."""
        # https://ffn.extranat.fr/webffn/nat_recherche.php?idrch_id={iuf}&idopt=prf&idbas=25
        # https://ffn.extranat.fr/webffn/nat_recherche.php?idrch_id={iuf}&idopt=prf&idbas=50
        cmd = f"https://ffn.extranat.fr/webffn/nat_recherche.php?idrch_id={iuf}&idopt=prf&idbas=25"

        self.__progress__(f'{iuf}')

        nageur = Nageur()

        with urllib.request.urlopen(cmd) as url2:  # nosec

            bsdata = BeautifulSoup(url2.read(), 'html.parser')
            item = bsdata.find("h5")

            # nageur
            nageur = self.__create_nageur_from_tr(item)
            if nageur.name == '[]':
                self.__progress__('')
                return None
            self.__progress__(nageur.name)

            # nages - 25 m
            self.__get_nageur_bage_from_tr(bsdata.find_all('tr'), nageur)

        # nages - 50 m
        cmd = f"https://ffn.extranat.fr/webffn/nat_recherche.php?idrch_id={iuf}&idopt=prf&idbas=50"

        with urllib.request.urlopen(cmd) as url2:  # nosec

            bsdata = BeautifulSoup(url2.read(), 'html.parser')
            self.__get_nageur_bage_from_tr(bsdata.find_all('tr'), nageur)

        self.__progress__('')

        return nageur
