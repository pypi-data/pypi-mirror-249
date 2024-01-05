# -*- coding: utf-8 -*-
"""Tests Extranatcli."""

from io import StringIO
import csv
import json
import os

from extranatapi import Extranatcli


# def test_list_regions(tmp_path):

#     extranatcli = Extranatcli()
#     mystdout = StringIO()

#     extranatcli.set_output(mystdout, 'column')
#     extranatcli.run_list_regions()

#     extranatcli.set_output(mystdout, 'text')
#     extranatcli.run_list_regions()

#     # json
#     mystdout_json = StringIO()
#     extranatcli.set_output(mystdout_json, 'json')
#     extranatcli.run_list_regions()
#     result = json.loads(mystdout_json.getvalue())
#     assert 'regions' in result

#     # csv
#     mystdout_csv = StringIO()
#     extranatcli.set_output(mystdout_csv, 'csv')
#     extranatcli.run_list_regions()
#     reader = csv.DictReader(StringIO(mystdout_csv.getvalue()), delimiter=';')
#     assert 'idreg' in reader.fieldnames
#     assert 'region' in reader.fieldnames

#     # xlsx
#     excel_file = os.path.join(tmp_path, "regions.xlsx")
#     extranatcli.set_output(excel_file, 'xlsx')
#     extranatcli.run_list_regions()
#     os.remove(excel_file)


# def test_list_departements(tmp_path):

#     extranatcli = Extranatcli()
#     mystdout = StringIO()

#     extranatcli.set_output(mystdout, 'column')
#     extranatcli.run_list_departements()

#     extranatcli.set_output(mystdout, 'text')
#     extranatcli.run_list_departements()

#     # json
#     mystdout_json = StringIO()
#     extranatcli.set_output(mystdout_json, 'json')
#     extranatcli.run_list_departements()
#     result = json.loads(mystdout_json.getvalue())
#     assert 'departements' in result

#     # csv
#     mystdout_csv = StringIO()
#     extranatcli.set_output(mystdout_csv, 'csv')
#     extranatcli.run_list_departements()
#     reader = csv.DictReader(StringIO(mystdout_csv.getvalue()), delimiter=';')
#     assert 'iddep' in reader.fieldnames
#     assert 'region' in reader.fieldnames
#     assert 'departement' in reader.fieldnames

#     # xlsx
#     excel_file = os.path.join(tmp_path, "departements.xlsx")
#     extranatcli.set_output(excel_file, 'xlsx')
#     extranatcli.run_list_departements()
#     os.remove(excel_file)


# def test_list_clubs(tmp_path):

#     extranatcli = Extranatcli()
#     mystdout = StringIO()

#     extranatcli.set_output(mystdout, 'column')
#     extranatcli.run_list_clubs()

#     extranatcli.set_output(mystdout, 'text')
#     extranatcli.run_list_clubs()

#     # json
#     mystdout_json = StringIO()
#     extranatcli.set_output(mystdout_json, 'json')
#     extranatcli.run_list_clubs()
#     result = json.loads(mystdout_json.getvalue())
#     assert 'clubs' in result

#     # csv
#     mystdout_csv = StringIO()
#     extranatcli.set_output(mystdout_csv, 'csv')
#     extranatcli.run_list_clubs()
#     reader = csv.DictReader(StringIO(mystdout_csv.getvalue()), delimiter=';')
#     assert 'idclub' in reader.fieldnames
#     assert 'region' in reader.fieldnames
#     assert 'departement' in reader.fieldnames
#     assert 'club' in reader.fieldnames

#     # xlsx
#     excel_file = os.path.join(tmp_path, "regions.xlsx")
#     extranatcli.set_output(excel_file, 'xlsx')
#     extranatcli.run_list_clubs()
#     os.remove(excel_file)


def test_list_nages(tmp_path):

    extranatcli = Extranatcli()
    mystdout = StringIO()

    extranatcli.set_output(mystdout, 'column')
    extranatcli.run_list_nages()

    extranatcli.set_output(mystdout, 'text')
    extranatcli.run_list_nages()

    # json
    mystdout_json = StringIO()
    extranatcli.set_output(mystdout_json, 'json')
    extranatcli.run_list_nages()
    result = json.loads(mystdout_json.getvalue())
    assert 'noms' in result

    # csv
    mystdout_csv = StringIO()
    extranatcli.set_output(mystdout_csv, 'csv')
    extranatcli.run_list_nages()
    reader = csv.DictReader(StringIO(mystdout_csv.getvalue()), delimiter=';')
    assert 'nom' in reader.fieldnames

    # xlsx
    excel_file = os.path.join(tmp_path, "nages.xlsx")
    extranatcli.set_output(excel_file, 'xlsx')
    extranatcli.run_list_nages()
    os.remove(excel_file)


def test_saison(tmp_path):

    extranatcli = Extranatcli()
    mystdout = StringIO()

    extranatcli.set_output(mystdout, 'column')
    extranatcli.run_saison(idclub=3221, annee=2019)

    extranatcli.set_output(mystdout, 'text')
    extranatcli.run_saison(idclub=3221, annee=2019)

    # json
    mystdout_json = StringIO()
    extranatcli.set_output(mystdout_json, 'json')
    extranatcli.run_saison(idclub=3221, annee=2019)
    result = json.loads(mystdout_json.getvalue())
    assert 'competitions' in result
    assert 'saison' in result

    # csv
    mystdout_csv = StringIO()
    extranatcli.set_output(mystdout_csv, 'csv')
    extranatcli.run_saison(idclub=3221, annee=2019)
    reader = csv.DictReader(StringIO(mystdout_csv.getvalue()), delimiter=';')
    # saison;competitiondate;competitionname;nageur;annee;age;nationalite;iuf;sexe;bassin;nage;temps;classement;points
    assert 'saison' in reader.fieldnames
    assert 'nageur' in reader.fieldnames
    assert 'iuf' in reader.fieldnames
    assert 'annee' in reader.fieldnames
    assert 'age' in reader.fieldnames
    assert 'nationalite' in reader.fieldnames
    assert 'sexe' in reader.fieldnames
    assert 'temps' in reader.fieldnames

    # xlsx
    excel_file = os.path.join(tmp_path, "saison.xlsx")
    extranatcli.set_output(excel_file, 'xlsx')
    extranatcli.run_saison(idclub=3221, annee=2019)
    os.remove(excel_file)


def test_nageur_perf_mpp(tmp_path):
    # bassin  nage      pos.  temps     points
    allperf = False
    extranatcli = Extranatcli()
    mystdout = StringIO()

    extranatcli.set_output(mystdout, 'column')
    extranatcli.run_nageur_perf(iuf=189335, allperf=allperf)

    extranatcli.set_output(mystdout, 'text')
    extranatcli.run_nageur_perf(iuf=189335, allperf=allperf)

    # json
    mystdout_json = StringIO()
    extranatcli.set_output(mystdout_json, 'json')
    extranatcli.run_nageur_perf(iuf=189335, allperf=allperf)
    result = json.loads(mystdout_json.getvalue())
    assert 'nages' in result

    # csv
    mystdout_csv = StringIO()
    extranatcli.set_output(mystdout_csv, 'csv')
    extranatcli.run_nageur_perf(iuf=189335, allperf=allperf)
    reader = csv.DictReader(StringIO(mystdout_csv.getvalue()), delimiter=';')
    assert 'nage' in reader.fieldnames
    assert 'temps' in reader.fieldnames
    assert 'points' in reader.fieldnames

    # xlsx
    excel_file = os.path.join(tmp_path, "nageur.xlsx")
    extranatcli.set_output(excel_file, 'xlsx')
    extranatcli.run_nageur_perf(iuf=189335, allperf=allperf)
    os.remove(excel_file)


def test_nageurs_perf_all(tmp_path):
    # bassin  nage      pos.  temps     points
    allperf = True
    extranatcli = Extranatcli()
    mystdout = StringIO()

    extranatcli.set_output(mystdout, 'column')
    extranatcli.run_nageur_perf(iuf=189335, allperf=allperf)

    extranatcli.set_output(mystdout, 'text')
    extranatcli.run_nageur_perf(iuf=189335, allperf=allperf)

    # json
    mystdout_json = StringIO()
    extranatcli.set_output(mystdout_json, 'json')
    extranatcli.run_nageur_perf(iuf=189335, allperf=allperf)
    result = json.loads(mystdout_json.getvalue())
    assert 'nages' in result

    # csv
    mystdout_csv = StringIO()
    extranatcli.set_output(mystdout_csv, 'csv')
    extranatcli.run_nageur_perf(iuf=189335, allperf=allperf)
    reader = csv.DictReader(StringIO(mystdout_csv.getvalue()), delimiter=';')
    assert 'nage' in reader.fieldnames
    assert 'temps' in reader.fieldnames
    assert 'points' in reader.fieldnames

    # xlsx
    excel_file = os.path.join(tmp_path, "nageur.xlsx")
    extranatcli.set_output(excel_file, 'xlsx')
    extranatcli.run_nageur_perf(iuf=189335, allperf=allperf)
    os.remove(excel_file)
