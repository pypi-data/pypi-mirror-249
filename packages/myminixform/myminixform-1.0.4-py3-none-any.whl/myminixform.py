# -*- coding: utf-8 -*-

# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [1] [Importation des modules ]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
from __future__ import unicode_literals
import pandas as pd
#from rich import print
import re
import codecs
import openpyxl
from humre import *
from yaml import load, dump,load_all
import yaml,csv
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [2] [Definition des fonctions ]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
def lire_yaml(fichier,encoding="utf-8"):
    """
    Lecture de fichier .yaml
    parameter:
        fichier: Chemin du fichier .yaml à lire
    """
    with codecs.open(fichier, 'r',encoding) as stream:
        try:
            return load(stream, Loader=Loader)
        except yaml.YAMLError as exc:
            print(exc)

def csv_to_yaml(fichier):
    """
    Lecture de fichier .csv et transformation en une données yaml
    parametre:
        fichier: Chemin du fichier .csv à lire
    """
    with codecs.open(fichier, 'r',"utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = []
        for row in csv_reader:
            new_row = {}
            for key, value in row.items():
                new_row[key] = value
            data.append(new_row)
    return yaml.dump(data)        

def csv_externe(my_dict):
    results = []
    for key, value in my_dict.items():
        if isinstance(value, str) and "_(" in value:
            start_index = value.find("_(") + 2
            end_index = value.find(")", start_index)
            if end_index != -1:
                text_between_parentheses = value[start_index:end_index]
                results.append((key, text_between_parentheses))
    return results

def add_source_externe(yaml_data):
    modele=yaml_data
    choix=modele["choix"]
    source_externe=csv_externe(choix)
    if len(source_externe)>0:
        for key,valeur in source_externe:
            data = csv_to_yaml(valeur)
            data_dic=load(data, Loader=Loader)
            modele["choix"][key] = data_dic
    return modele

def add_metadata(yaml_data):
    modele=yaml_data
    if "metadata" in modele["parametres"].keys():
        metadata={k:k for k in modele["parametres"]["metadata"]}
        modele["parametres"]["metadata"]= metadata
    return modele

def yaml_to_csv(yaml_data):
    """
    """
    data = yaml.safe_load(yaml_data)
    if not data:
        return []
    keys = data[0].keys()
    output = []
    output.append(keys)
    for item in data:
        output.append(item.values())
    return output
#===================================================================================================
#@VARIABLE "xform_types" 
# QUI REPRESENTE LA LISTE DES TYPES DE QUESTIONS XLSFORM ET LEURS EQUIVALENT MINIXFORM.
xform_types = """
            integer,i
            integer,e
            integer,entier
            integer,integer
            integer,int
            integer,ent
            decimal,r
            decimal,d
            range,rg
            text,t
            text,txt
            select_one,so
            select_one,s1
            select_one,liste_u
            select_one,lu
            select_multiple,sm
            select_multiple,lm
            select_one_from_file,sof
            select_multiple_from_file,smf
            rank,rk
            rank,rn
            note,n
            note,nt
            geopoint,point
            geotrace,trace
            geoshape,shape
            date,de
            date,date
            time,tm
            time,te
            dateTime,dtme
            image,img
            audio,audio
            audio,o
            background-audio,bg_audio
            video,video
            video,v
            file,f
            barcode,bc
            calculate,calc
            acknowledge,ack
            hidden,hd
            xml-external,xml
            begin_group,g
            begin_group,group
            end_group,end
            end_group,eg
            repeat_group,repeat
            repeat_group,re
            end_repeat,er
            end_repeat,endr
        """
#===================================================================================================
#@VARIABLE "template" 
# QUI REPRESENTE UN EXEMPLE DE TEMPLATE YAML FORMATE EN MINIXFORM.
template="""
parametres:
  titre: Titre du questionnaire
  description: >
    Il s'agit d'un modele de questionnaire yaml à utiliser avec MiniXform. 


  date: 2023-05-04
  auteur:
    - Nom: Nom de l'auteur
      Prenom: Prenom auteur
      Email: email.auteur@mail.com
      Tel: tel_auteur
  serveur:
  metadata: # Les metadata sont des informations recuperé automatiquement sur le telephone de l'enqueteur
    [
      start,
      end,
      today,
      deviceid,
      phonenumber,
      username,
      email,
      audit,
      simserial,
    ]
choix:
  sexe: &sexe
    - Homme
    - Femme
  bool: &bool [Oui, Non]
  ages: &age [18-25, 26-35, 36-45, 46-55, 56 et plus]
  structures: &structures
    - CNRA
    - ANADER
    - FIRCA
    - ONG
    - OPA
    - Autre
  regions: &regions
    - Abidjan
    - N'Zi
    - Iffou
    - Bélier
    - Moronou
    - Indénié-Djuablin
    - Sud-Comoé
  departement: &departs
    - Agboville
    - Sikensi
    - Taabo
    - Tiassalé
    - Koro
    - Ouaninou

questions:
  I:
    titre: DESCRIPTION DE L'ETUDE
    description: >
      <b>Objectif générale : </b>
       <br>
       L'objectif de l'étude est d'identifier les contraintes majeures à l'adoption des technologies et innovations 
       dans le domaine agricole, afin de proposer une stratégie de diffusion optimisant leur adoption. _note


    object_questionnaire: >
      - Identifier des innovations et technologies générées et diffusées ou non dans le cadre du FCIAD - Identifier les mécanismes de génération et de transfert de ces innovations - Forces et faiblesses de ces mécanismes - Quelques recommandations d'amélioration des mécanismes

  A:
    titre: >
      A: IDENTIFICATION DE L'ENQUETE


    2: A.1 Date d'enquete (………/05/2023) _date
    3: A.2 Nom
    4: A.3 Prénoms
    5:
      - A.5 Sexe ()
      - *sexe
    6: A.6 Tranche âge () $[18-25,26-35,36-45,46-55,56 et plus ] _s1
    7: A.7 Niveau étude () _s1 $[Sans niveau ,coranique ,Primaire,  Secondaire général, Secondaire technique ,Supérieur]
    8:
      - A.8 Région
      - *regions
    9:
      - A.9 Département
      - *departs
    10: A.10 Ville/village  ()
    11a: A.11-a Téléphone ()
    11b: A-11-b E-mail ()
    12a: A.12 Chaîne de valeur ()
    12b: Innovation ()
    13: A.13 Structure de vulgarisation ()
    14: A.14 Taille de l'exploitation (En Hectares) _e
    15: A.15 Taille de l'activité de la chaine de valeur ( En Hectares) _e
    16: A.16 Nombre d'années dans l'activité de la chaine de valeur () _e

  B:
    titre: B. EVALUATION DE L'ENVIRONNEMENT
    1:
      - B.1 Avez-vous déjà adopté d'autres innovations avant celle sous étude ?
      - *bool
    2:
      - Si oui, quelles ont été les structures de diffusion ?() $si(III_A=Oui)
      - *structures
    table-1:
      legende: B.2 En général comment appréciez-vous les interventions de ces structures ?
      colonnes:
        - CNRA () _s1 $[Très satisfaisant, Satisfaisant, Peu satisfaisant, Pas du tout satisfaisant]
        - ANADER () _s1 $[Très satisfaisant, Satisfaisant, Peu satisfaisant, Pas du tout satisfaisant]
        - FIRCA () _s1 $[Très satisfaisant, Satisfaisant, Peu satisfaisant, Pas du tout satisfaisant]
        - ONG () _s1 $[Très satisfaisant, Satisfaisant, Peu satisfaisant, Pas du tout satisfaisant]
        - OPA () _s1 $[Très satisfaisant, Satisfaisant, Peu satisfaisant, Pas du tout satisfaisant]
        - Autre () _s1 $[Très satisfaisant, Satisfaisant, Peu satisfaisant, Pas du tout satisfaisant]
      lignes: [1]
    3: B.3 Comment avez-vous été informé(e) de l'innovation du projet FCIAD dont vous a été bénéficiaire ?
    4:
      - B.4 Avez-vous été d'une manière ou d'une autre associé à l'identification du problème qui a permis de générer l'innovation dont vous êtes bénéficiaire ?
      - *bool
    5: B.5 Si oui, dans quel cadre ?() $[ Votre OPA , Consultation individuelle] $si(III_3=oui)
    6: Si autre préciser()
  # ---
  C:
    titre: >
      C. INNOVATIONS ADOPTEES


    note: >
      Identification de l'innovation ou la technologie adoptée dans le cadre du FCIAD () _note


    1:
      - C.1 Nature de l'innovation dont vous avez bénéficié. () _s1
      - [Production, Transformation, Valorisation]
    2: C.2	Période de diffusion()	_date
    3: C.3	Difficultés rencontrées pendant l'adoption	()
    4: C.4	Maîtrise de l'innovation à ce jour ()	_s1 $[Bien maîtrisée,Peu maîtrisée,Pas encore maîtrisée]
    5: C.5	Si peu ou pas maîtrisée, quelles sont les causes ? () _s1 $[Formation insuffisante, Ressources matérielles insuffisantes,Autre]
    5a: Si autres, préciser ()
    6: C.6Si vous avez abandonné l'innovation, après combien de temps  d'essai ? () _s1 $[Mois, Campagnes, Années]
    7: causes de l'abandon ()
  # ---
  D:
    titre: D. EVALUATION DE LA PERTINENCE
    1: D.1 .Pouvez-vous évaluer le niveau de pertinence de l'Innovation & technologie ?() _s1 $[Très pertinent,	pertinent,	Peu pertinent,	Pas pertinent NSP]

    2:
      - D.2. Globalement Pensez-vous que l'innovation répondait à vos besoins ?() _s1
      - *bool
    3:
      - >
        Si oui, pensez-vous qu'elle : () 

      - - introduit peu de changement sur l'exploitation
        - permet de résoudre un problème sectoriel et a des répercussions sur l'ensemble de l'exploitation
        - implique l'adoption simultanée de diverses techniques cohérentes entre elles
        - Autre
    4: Si l'innovation repondait à un autre besoins, précisez le. ()
  # ----------------------------------------------------------------
  E:
    titre: E. EVALUATION DE L'EFFICACITE
    table-1:
      legende: E.1	Si l'innovations a quelque peu répondu à vos besoins, quel impact sur votre activité ? (Justifiez votre réponse en donnant des chiffres avant et après l'adoption de l'innovation)
      colonnes: [Avant (Chiffre) _e, Après ( Chiffre) _e]
      lignes:
        - Gain de productivité
        - Gain de qualité
        - Gain de temps
        - Gain de revenu supplémentaire
        - Autre impact sur votre activité
  # --------------------------------
  F:
    titre: F	EVALUATION DU MECANISME DE TRANSFERT DES INNOVATIONS GENEREES A LA VULGARISATION ET DE LA DURABILITE
    1: F.1	L'innovation part du chercheur au vulgarisateur. Comment passe-t-elle du vulgarisateur à vous? ()
    2:
      - F.2	Avez-vous noté quelques difficultés de la diffusion de l'innovation?()
      - *bool
    2b: Si oui, lesquelles ?()
    3:
      - F.3	Rencontrez-vous des difficultés à maintenir l'innovation dans votre activité ?()
      - *bool
    3b: Si oui, lesquelles ? ()
    4: F.4 Selon vous, quelles sont les faiblesses qui pourraient entacher la pérennisation de l'adoption des innovations en général ? ()
  # ----------------------------------------------------------------
  G:
    titre: G. VOS RECOMMANDATIONS
    1: G.1	Au vu de tout ce qui précède, quelles recommandations pouvez-vous faire pour l'amélioration du mécanisme de diffusion et de transfert des innovations aux bénéficiaires ? ()
    2: G.2	Selon vous, que faut-il faire pour que les innovations ne soient pas abandonnées après leur adoption par vous après un moment donné ?()
    3: G.3	Que recommandez-vous au FCIAD pour pérenniser ses activités de transfert d'innovation et de technologies ? ()

"""

# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# [3] [Definition des class ]
# 〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜


#===================================================================================================
#++++ OBJET "Question" POUR CONVERTIR UNE QUESTION FORMATER EN MINIXFORM 
# Il prend en parametre une chaine de caractère "texte"
# qui correspond à la question formaté en minixform.
class Question:
    """
        Objet question
        Cet objet represente une question du formulaire, le type de la question et les autres attributs et methodes applicables à une question. 
        input: texte minixform
            ex: "Voici l'exemple de question ${I_1} pour tester minixform !  (Nous avons ici la description) $[choix 1, choix 2, choix 3] ** _e $si(I_5>0) =(.>10|Vous devez entrer un nombre superieur à │
│                               10) $app(coul 1) $calc(+3) $ro"
        propriétés:
            self.text = Chaine de caractère entré en parametre
            self.texte_type= type de la question au format minixform extrait de la question
            self.type = type XLSFORM correspondant a texte_type
            self.name= valeur de la variable "name" dans XLSFORM
            self.label= Valeur du la variable "label" dans XLSFORM
            self.required= Valeur de la variable required dans XLSFORM
            self.relevant= Valeur de la variable relevant dans XLSFORM
            self.calculation= Valeur de la variable calculation dans XLSFORM
            self.constraint= Valeur de la variable constraint dans XLSFORM
            self.constraint_message= Valeur de la variable constraint_message dans XLSFORM
            self.readonly= Valeur de la variable readonly dans XLSFORM
            self.appearance= Valeur de la variable appearance dans XLSFORM
            self.hint = Valeur de la variable hint dans XLSFORM
            self.showif = Valeur de la variable relevante dans XLSFORM
            self.choice = Valeur de la variable liste des choix pour la question
            self.ordre = ordre ou numéro de la question
            self.repeat_count= Valeur de la variable repeat_count dans XLSFORM
            self.minixform_types= DataFrame de la liste des types dans XLSFORM et Leurs Valeurs dans Minixform
    """
    def __init__(self, texte):
        self.text = texte
        self.texte_type=self.extraire_type()
        self.type = self.search_type(self.texte_type)
        self.name=""
        self.label=self.extaire_label()
        self.required=self.is_required()
        self.relevant=self.montrer_si()
        self.calculation=self.extraire_calculation()
        self.constraint=self.extraire_constraint()
        self.constraint_message=self.extraire_constraint_message()
        self.readonly=self.is_readonly()
        self.appearance=self.extraire_apparence()
        self.hint = self.extraire_hint()
        self.showif = self.montrer_si()
        self.choice = self.extaire_choix()
        self.ordre = ""
        self.repeat_count=""
        self.minixform_types=self.list_types()

    def clear_empty_lines(self, text):
        """
        Efface toutes les lignes vides d'une chainede caractères.
        ---
            Parametre:
                - text: string, chaine de caractères
            output: string, chaine de caractères
        """
        lines = text.split("\n")
        lines = [line for line in lines if line.strip() != ""]
        return "\n".join(lines)

    def replace_special_characters(self,chaine):
        """
        Remplace les caracteres speciaux dans un texte entré en parametre
        ---
        parametre: chaine de caractère
        output: cahine de caractere formaté avec caractère spéciaux remplacé par "_" 
        """
        
        pattern = r'[^a-zA-Z0-9_]'  # Expression régulière pour trouver les caractères spéciaux
        return re.sub(pattern, '_', chaine)

    def extracteur(self,texte,debut,fin):
        """
        Extrait du contenu d'une chaine de caractères compris entre deux(2) délimiteurs.
        ---
            Parametre :
                -texte : String, la chaine de caractères concernée par l'extraction
                -debut : String, la chaine de caractères de début
                -fin : String, la chaine de caractères de fin
            Output : list, elements compris entre 'debut' et 'fin' dans 'texte'
        """
        elements_textuels = []
        debut_motif = debut
        fin_motif = fin
        debut_index = texte.find(debut_motif)
        while debut_index != -1:
            debut_index += len(debut_motif)
            fin_index = texte.find(fin_motif, debut_index)
            if fin_index != -1:
                element_textuel = texte[debut_index:fin_index].strip()
                elements_textuels.append(element_textuel)
            debut_index = texte.find(debut_motif, fin_index)
        return elements_textuels

    def extaire_label(self):
        """
        Retorune le label de la question.
        La methode considère le texte avant la première parenthèse
        Output :
            String valeur de label dans la question
        """
        index_premiere_parenthese = self.text.find("(")
        return self.text if index_premiere_parenthese == -1 else self.text[:index_premiere_parenthese]
    
    def extraire_hint(self):
        """
        Permet d'extraire l'hint de la question
        Output :
            String valeur de hint dans la question
            Renvoie une liste des informations contenues entre parenthèses dans la chaîne.
        """
        resultat = self.extracteur(self.text," (",")")
        return resultat[0] if len(resultat)>0 else ""
    
    def extraire_apparence(self):
        """
        Pour extraire l'apparence de la question.
        On extrait pour ce faire le contenu entre les parenthèses de '_app()' ou '#()'
            Output :
            String valeur de appearance dans la question
        """
        reponses1=self.extracteur(self.text," $app(",")")
        reponses2=self.extracteur(self.text," #(",")")
        if len(reponses1)>0: return reponses1[0].replace(' $app(','').replace(')','').replace(' ','')
        elif len(reponses2)>0: return reponses2[0].replace(' #(','').replace(')','').replace(' ','')
        else: return ""

    def extraire_calculation(self):
        """        
        Output :
                String valeur de calculation dans la question
        """
        result = self.extracteur(self.text," $calc(",")")
        return result[0] if len(result) > 0 else ""

    def extraire_constraint(self):
        result=self.extracteur(self.text," =(",")")
        try: return result[0].split('|')[0] if len(result) > 0 else ""
        except: return result[0]

    def extraire_constraint_message(self):
        result=self.extracteur(self.text," =(",")")
        try: return result[0].split('|')[1] if len(result) > 0 else ""
        except: return result[0]

    def montrer_si(self):
        result=self.extracteur(self.text,"$si(",")")
        return result[0] if len(result) > 0 else ""

    def is_required(self):
        """
        Retourne un booleen selon que la question est ebligatoire ou pas.
        Pour celà, elle verifie s'il existe exactement ' **' dans la chaine de caractère prise en parametre
        Output: True or ""
        """
        return False if ' **' in self.text else ""
            
    def is_readonly(self):
        """
        Vérifie s'il s'agit d'une question en readonly
        Output: True or ""
        """
        return True if ' $ro' in self.text else ""
    
    def extaire_choix(self):
        try: return self.extracteur(self.text,"$[","]")[0].split(",")
        except: return self.extracteur(self.text,"$[","]")

    def extraire_type(self):
        mots = self.text.split(" ")
        mots=[mot for mot in mots if len(mot) > 0]
        typ=[mot[1:] for mot in mots if mot[0]=="_"]
        try : return typ[0]
        except: return None

    def search_type(self, valeur):
        df = self.list_types()
        qtype = None
        for x in range(len(df.minixform)):
            if valeur == df.minixform[x]: qtype = df.xform[x]
        return qtype

    def list_types(self):
        chaine = xform_types
        types_xlsform = [x.replace(" ", "").split(",")[0] for x in self.clear_empty_lines(chaine).split("\n") ]
        types_minixform = [ x.replace(" ", "").split(",")[1] for x in self.clear_empty_lines(chaine).split("\n")]
        types = list(zip(types_xlsform, types_minixform))
        types=pd.DataFrame(types, columns=["xform", "minixform"])
        return pd.DataFrame(types, columns=["xform", "minixform"])

    def formated(self):
        """
        Permet de formater une question liste tel que liste 1

        
        """
        
        dico=[
            {
            "type":self.type,
            "name":self.replace_special_characters(self.name),
            "label":self.label,
            "hint":self.hint,
            "required":self.required,
            "relevant":self.relevant,
            "calculation":self.calculation,
            "constraint":self.constraint,
            "constarint_message":self.constraint_message,
            "readonly":self.readonly,
            "appearance":self.appearance,
            "repeat_count":self.repeat_count
            },
            self.choice
        ]
        if "metadata" in dico[0]["name"]:
            dico[0]["type"]=dico[0]["label"]
            dico[0]["name"]=dico[0]["label"]
            
        return dico

#===================================================================================================
#++++ OBJET "yaml_form(Question)" POUR CONVERTIR UN FICHIER YAML EN UN FORMULAIRE XLSFORM
# Cet objet herite de Question et prend en parametre "filepath" 
# qui est le chemin d'accès au fichier '*.yaml' à convertir.
class yaml_form(Question):
    """
    Objet questionnaire yaml:
    ---
    Convertir un fichier formaté en yaml en un questionnaire respectant 
    la logique de syntaxe de XLSFORM
    """
    def __init__(self,filepath=None,encoding="utf-8"):
        self.filename=filepath
        self.g_questions=[]
        self.questionnaire=lire_yaml(filepath,encoding)
        self.feuilles_excel = ["survey", "choices", "settings"]
        self.source_externe_choix=csv_externe(self.questionnaire["choix"])
        self.questionnaire_edite=add_source_externe(self.questionnaire)
        self.questionnaire_edite_metadata=add_metadata(self.questionnaire)
        self.choix=self.questionnaire["choix"]
        self.metadata=self.questionnaire_edite_metadata["parametres"]["metadata"]
        self.questions=self.questionnaire_edite_metadata["questions"]
        self.questions["metadata"]=self.metadata
        self.groupes=[groupe for groupe in self.questions]
        self.xls_choices=""
        self.xls_survey=""

#===================================================================================================
#@METHODE POUR CONVERTIR CHAQUE GROUPE EN DICTIONNAIRE
    def groupe_to_dic(self,groupe="",name="",repeat=None):
        """
        Conversion des questions du groupe yaml en dictionnaires formatés.
        On obtien à la fin du d'execution, la liste de toutes las questions sous forme d'un dictionnaire python.
        Parametres:
            - groupe : yaml , liste des questions yaml
            - name : string, nom du groupe
        Output :
            -self.g_questions : list, valeur actualisée la propriété g_questions ( Liste de dictionnaire de questions)
        """
#-------------------------------------------------------------------------------------------------------
#=== Detection du type de groupe
        type_of_groupe="simple" #on commence par supposer qu'il s'agit d'un groupe simple entre en parametre
        if ("titre" or "title") in groupe: # Cette condition est vrai s'il exiwte une question de nom "titre" ou title dans le groupe
            try:
                q=Question(groupe["titre"])
            except:
                q=Question(groupe["title"])
            if repeat!= None: # Est vrai si la nature du groupe est de type repeat. "repeat" ici est un parametre de la fonction group_to_dic
                type_of_groupe="repeat" # On change type_of_groupe à repeat si c'est un repeate groupe
                q.type="begin_repeat"
                if type(repeat)==type(1):
                    q.repeat_count=repeat if int(repeat)>1 else ""
                else:
                    q.repeat_count=f"${{repeat}}"
            else:
                type_of_groupe="simple"
                q.type="begin_group"
            q.name=name
            self.g_questions.append(q.formated())
            groupe.pop("titre")
#-------------------------------------------------------------------------------------------------------
#=== Ajout de la description au groupe
        if "description" in groupe:
            q=Question(groupe["description"])
            q.name=name+"_"+"description"
            q.type="note"
            q.readonly=True
            self.g_questions.append(q.formated())
            groupe.pop("description")
        # Après avoir detecté le type de groupe et avoir ajouté le titre du groupe et sa description au dictionnaire
        # Nous allons maintenant parser chaques queestions et les ajouter au dictionnaire
#-------------------------------------------------------------------------------------------------------
# === Ajout des questionnaire du groupe au dictionnaire
        for k in groupe:
#-------------------------------------------------------------------------------------------------------
# === Detection et ajout de question de type select_one ou multiple de type simple
            if (type(groupe[k])==type([""])) and (type(groupe[k][1])==type([""])): #if true alors question de type "select"
                
                """
                modèle de type
                    5: 
                        - A.5 Sexe ()
                        - *sexe
                """
                q=Question(groupe[k][0])
                q.name=name+"_"+str(k)
                q.choice=groupe[k][1]
                if q.type==None:q.type="select_multiple"
                q.type=q.type+" choix_"+q.name
                self.g_questions.append(q.formated())

#-------------------------------------------------------------------------------------------------------
# === Detection et ajout de question de type select_one ou multiple de type complexe              
            elif type(groupe[k])==type(""): #if true alors question de type "select ou non select"
                
                q=Question(groupe[k])
                q.name=name+"_"+str(k)
                
                if not(len(q.formated()[1])==0): #if true alors question de type "select"
                    """
                    modèle de type
                        6: A.6 Tranche âge () $[18-25,26-35,36-45,46-55,56 et plus ] _s1
                    """
                    if q.type==None:q.type="select_multiple"
                    q.type=q.type+" choix_"+q.name
#-------------------------------------------------------------------------------------------------------
# === Detection et ajout de question de type text au cas ou aucun type n'est spécifié dans le yaml        
                else: # sinon alors question de type non select
                    if q.type==None:q.type="text"
                    
                self.g_questions.append(q.formated())
                
            elif type(groupe[k])==type([""]) and type(groupe[k][1])==type(" "):
                pass
#-------------------------------------------------------------------------------------------------------
# === Detection et ajout de question de type, group et repeat_group      
            elif type(groupe[k])==type([""]) and type(groupe[k][1])==type({"1":" ", "2":""}):
                
                name2=name+"_"+str(k)
                if "g" in groupe[k][1]:
                    groupe[k][1]["g"]["titre"]=groupe[k][0]
                    groupe2=groupe[k][1]["g"].copy()
                    self.groupe_to_dic(groupe2,name2)
                elif "g1" in groupe[k][1]:
                    groupe[k][1]["g1"]["titre"]=groupe[k][0]
                    groupe2=groupe[k][1]["g1"].copy()
                    self.groupe_to_dic(groupe2,name2)
                else:
                    groupe[k][1]["table-1"]["titre"]=groupe[k][0]
                    groupe2=groupe[k][1]["table-1"].copy()
                    self.groupe_to_dic(groupe2,name2)
#-------------------------------------------------------------------------------------------------------
# === Detection et ajout de question de type tableau                   
                    
            else :
                if "table" in k:
                    if "lignes" in groupe[k]:
                        if len(groupe[k]["lignes"])==1:
                            repeat = groupe[k]["lignes"][0]
                        else:
                            repeat=None
                        for ligne in groupe[k]["lignes"]:
                            groupe2={}
                            # Groupe 2 est un sting de type complexe 
                            # Il consiste a ajouter à la question le detail sur la du tableau
                            # Pour ce faire on remplace dans la question la premiere 
                            # parenthese "(" 
                            # par ": Detail pour ligneItem" 
                            # ligneItem etant ici l'element caractéristique de la ligne concerné
                            groupe2["titre"]=groupe[k]["legende"].replace("(",": Detail pour "+str(ligne)+" (")+ " $app(field-list)" if (len(groupe[k]["lignes"])>1) else groupe[k]["legende"]+" () $app(field-list)"
                            for col in range(len(groupe[k]["colonnes"])):
                                groupe2[str(col)] = groupe[k]["colonnes"][col]
                            name2=name+'_'+str(k)+"_"+str(ligne)
                            #------------------------------
                            #Appel reccursif de la fonction
                            self.groupe_to_dic(groupe2,name2,repeat)
                            
                else :
                    #------------------------------
                    #Appel reccursif de la fonction
                    self.groupe_to_dic(groupe[k],name+"_"+str(k))
                    
#-------------------------------------------------------------------------------------------------------
# === Fermerture de group ou de repeat_group     
        q=Question("")
        if type_of_groupe=="repeat":            
            q.type="end_repeat"
            type_of_groupe=""
        else:q.type="end_group"
        self.g_questions.append(q.formated())
#-------------------------------------------------------------------------------------------------------
# === fin de la convertion du groupe de questions en dictionnaire
        return self.g_questions    


#===================================================================================================
#@METHODE POUR CONVERTIR TOUS LES GROUPES DU FORMULAIRE EN DICTIONNAIRES
    def to_dicts(self):
        """
        Cette methode retourne la liste de toutes les questions sous forme de 
        liste de dictionnaire.
        ---
        Parametres:
            --
        Outpout:
            - reponse_dic: liste de dictionnaire de questions
        """
        for k in range(len(self.groupes)):
            groupe=self.questions[self.groupes[k]]
            reponse_dict=self.groupe_to_dic(groupe,self.groupes[k])
        return reponse_dict

#===================================================================================================
#@METHODE POUR CONVERTIR LE FORMULAIRE EN FICHIER EXCEL
    def to_xslform(self, output):
        """
        Convertie la liste des questions en un DataFrame puis l'enregistre dans un fichier excel
        ---
        input: 
            path: Chemin vers le fichier excel au format XLSFORM de sortie
        Output:
            dico: Dictionnaire {survey:DataFrame, choices:DataFrame, result:Bool}
            fichier: Un fichier excel (.xlsx) enregistré dans au chemin output path entré en parametre
        """
        questions_list=self.to_dicts()
        survey=[q[0] for q in questions_list]
        choices_list=[[{"list_name":q[0]["type"].split(" ")[-1],"name":x+1,"label":q[1][x]} for x in range(len(q[1]))] for q in questions_list if "select" in q[0]["type"] and len(q)>0]
        choices = []
        for dic in choices_list:
            for element in dic:
                if element not in choices:
                    choices.append(element)
        dico={"survey":pd.DataFrame(survey),"choices":pd.DataFrame(choices)}
        self.xls_choices=dico["choices"]
        self.xls_survey=dico["survey"]
        try:
            with pd.ExcelWriter(output) as writer:
                dico["survey"].to_excel(writer, sheet_name='survey',index=False)
                dico["choices"].to_excel(writer, sheet_name='choices',index=False)
            dico["result"]=True
        except:
            dico["result"]=False
        return dico


# ================[Fonction détachées]==============================================================
#===================================================================================================
#@FONCTION POUR LIRE LE CONTENU D'UN FICHIER
def content_file(file):
    with codecs.open(file, "r", "utf-8") as f:
        content = f.read()
    return content



