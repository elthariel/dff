# DFF -- An Open Source Digital Forensics Framework
# Copyright (C) 2009-2010 ArxSys
# This program is free software, distributed under the terms of
# the GNU General Public License Version 2. See the LICENSE file
# at the top of the source tree.
#  
# See http://www.digital-forensic.org for more information about this
# project. Please do not directly contact any of the maintainers of
# DFF for assistance; the project provides a web site, mailing lists
# and IRC channels for your use.
# 
# Author(s):
#  Frederic Baguelin <fba@digital-forensic.org>


from api.vfs import *
from api.module.script import*
from api.module.module import *

from api.env import *
from api.env.libenv import *
from api.type.libtype import *
from api.module import *
from api.vfs.libvfs import *
from api.exceptions.libexceptions import *

import time

#On ne peut pas utiliser une seule classe pour decrire a la fois un fichier et un fd !!!
#Si on avait mis current_offset dans FileInfo, a chaque ouverture du fichier en question
#on perdrait les informations des fd ouverts precedent pour ce meme fichier !!!
#
# node.open(handle) retourne un fd. Pour un handle, j'ai stocke les informations interne au systeme
# de fichiers (offset, size)
#
#                FdInfo 1
#              /
#    HandleInfo - FdInfo 2
#              \ 
#               FdInfo 3
#
#


# Soit le systeme de fichier avec la structure suivante 
# (ne sert a rien en utilisation concrete... :)
#
#  _______________________ 
# |       Metadata 1      | ---> 16 octets
#  -----------------------
# |                       |
# |         Data 1        | ---> 64 octets
# |                       |
#  -----------------------
# |       Metadata 2      |
#  -----------------------
# |                       | 
# |         Data 2        |
# |                       |
#  -----------------------
# |         ...           |
#  -----------------------
# |       Metadata N      |
#  -----------------------
# |                       | 
# |         Data N        |
# |                       |
#  -----------------------
#
# Avec metadata ayant la structure suivante:
#
# 0 ________ 8 _________ 16  (en octets)
# | filename |  padding  |
#  ----------------------
#
# ce qui nous fait donc un nom de fichier de 8 octets max :) 
# Le reste c'est pour rester aligne et valider que c'est une
# entree de metadata valide ;)
#
# utiliser le script generate.py pour creer un dump de test
# Si vous le souhaitez vous pouvez regarder son contenu tel
# en mode hexa et ascii (a la hexdump...)
# le script genere un fichier dumb_fs.bin

MAX_FD = 100

#stocke les informations pour un fd donne qui est donc relatif a un fichier (donc un handle)
class FdInfo():
    def __init__(self, start_offset, size):
        self.start_offset = start_offset
        self.size = size
        self.current_offset = 0

#stocke les information pour un handle, c'est a dire pour une node qui a ete cree (donc un fichier)
class HandleInfo():
    def __init__(self, start_offset, size):
        self.start_offset = start_offset
        self.size = size


# la classe qui sera instanciee a chaque application du module
class DumbFs(fso):

    def __init__(self):
        # j'instancie la classe fso heritee
        fso.__init__(self)
        
        # je donne le nom de mon driver
        self.name = "dumbfs"

        #je cree ma variable result
        self.res = results(self.name)

        # variable globale a la classe qui servira a faire correspondre
        # pour un handle donne, ses informations 
        # dans le cas present ce sera handle --> HandleInfo
        self.handle_mapping = {}

        # variable globale a la classe qui servira a faire correspondre 
        # pour un fd donne, ses informations FdInfo
        self.opened_fds = {}
        
        # j'instancie un mapping de 50 elements. toutes les valeurs sont mises
        # a None. Cela servira par la suite a prendre le premier fd non alloue
        for i in range(0, MAX_FD):
            self.opened_fds[i] = None

        # cette variable servira a compter le nombre total de fichier
        self.total_files = 0


    # methode permettant de recuperer le premier fd non alloue
    def get_unallocated_fd(self):
        i = 1
        values = self.opened_fds.values()
        found = False
        while i != MAX_FD and not found:
            if values[i] == None:
                found = True
            else:
                i += 1
        if found:
            return i
        else:
            return 0


    def createFiles(self):
        # j'instancie une variable qui servira d'increment pour la generation 
        # d'handle ainsi que pour mon handle_mapping.
        handle_iter = 0

        # je recupere un buffer correspondant a la 1ere entree metadata de 16 octets
        buff = self.parent_file.read(16)

        # je boucle jusqu'a ce que j'arrive a la fin de mon dump
        while len(buff):

            # je verifie que j'ai bien a faire a une entree metadata valide
            if buff[8:16] == "\xDE\xAD\xBE\xEF" * 2:
                # je cree un nouvel attribut
                attr = attrib()
                
                # je precise a python qu'il n'est pas proprietaire de cette variable
                # cela evite des segfaults lorsque le garbage collector de python se
                # met en place...
                attr.this.own(False)

                # je lui defini un handle
                attr.handle = Handle(handle_iter)

                # ainsi qu'une taille (ici elle est unique: 64 octets...)
                attr.size = 64

                # je definir egalement l'heure du fichier. Vu que je n'ai pas d'informations sur
                # les MAC times des fichiers, je met l heure actuelle pour tous
                t = time.localtime()
                cur_time = vtime(t[0], t[1], t[2], t[3], t[4], t[5], 0)
                # je precise a python qu il n'est pas proprietaire de la variable
                cur_time.thisown = False
                attr.time["changed"] = cur_time
                attr.time["modified"] = cur_time
                attr.time["accessed"] = cur_time

                # je recupere le nom du fichier defini ds les 8 premiers octets de l'entree
                name = buff[0:8]

                # je defini l'offset des donnees concernant le fichier actuel.
                # Vu que j'ai deja fait un read de 16, l'offset actuel de mon
                # file parent est deja positionne au niveau des data
                data_offset = self.parent_file.tell()

                # j'ajoute a mon mapping d'handle mon HandleInfo
                self.handle_mapping[handle_iter] = HandleInfo(data_offset, 64)

                # maintenant je peux creer une node de type file que je cree a partir de ma node root
                self.CreateNodeFile(self.root, name, attr)

                # j incremente le handle
                handle_iter += 1

                # j'incremente ma variable comptant le nombre total de fichier
                self.total_files += 1

                # je me deplace a la prochaine entree de metadata. Je dois donc me
                # deplacer de 64 octets etant donne que mon offset actuel pointe
                # sur les datas
                self.parent_file.seek(64, 1)
            else:
                pass

            # je recupere la nouvelle entree
            buff = self.parent_file.read(16)


    def start(self, args):
        #je recupere l'argument parent de type node
        self.parent_node = args.get_node("parent")

        # je recupere l'argument tmp de type string
        tmp = args.get_string("tmp")

        # j'ouvre la node parent pour obtenir un vfile
        # je vais ainsi pouvoir lire et seek pour lire mon dumb fs
        self.parent_file = self.parent_node.open()

        # j'instancie un nouvel attrib pour ma premiere node de mon
        # driver qui se nommera "root" (la racine pour mon module)
        attr = attrib()

        # je precise a python qu'il n'est pas proprietaire de cette variable
        # cela evite des segfaults lorsque le garbage collector de python se
        # met en place...
        attr.this.own(False)

        # j'attribue un handle qui sera utilise lors de l'appel a vopen(handle)
        # attr.handle = Handle(1)

        # c'est un repertoire donc size = 0
        attr.size = 0

        # j'ajoute des nouveaux attributs sous la forme key --> value 
        # avec key et value qui sont des strings
        # au passage, voici comment on peut creer une map en python
        mysmap = {"attrib1": "value1", "attrib2": "value2"}

        # et voici un exemple d'iteration sur une map en python
        
        for key, value in mysmap.iteritems():
            # j ajoute des nouveaux attributs
            attr.smap[key] = value

        # je definir egalement l'heure du fichier. Vu que je n'ai pas d'informations sur
        # les MAC times des fichiers, je met l heure actuelle pour tous
        t = time.localtime()
        cur_time = vtime(t[0], t[1], t[2], t[3], t[4], t[5], 0)
        # je precise a python qu il n'est pas proprietaire de la variable
        cur_time.thisown = False

        attr.time["changed"] = cur_time
        attr.time["modified"] = cur_time
        attr.time["accessed"] = cur_time

        # maintenant, je peux creer ma node root
        self.root = self.CreateNodeDir(self.parent_node, "dumb_fs_root", attr)

        # j'appelle ma methode qui va creer toutes les nodes en fction des fichiers existants
        self.createFiles()
        #return self.res

        # j'ajoute comme resultat le nombre total de fichier trouve
        self.res.add_const("total files", self.total_files)


    def vopen(self, handle):
        # je recupere les informations du handle que l'on me passe et je verifie
        # qu'il existe egalement
        if handle.id in self.handle_mapping.keys():
            handleinfo = self.handle_mapping[handle.id]

            # je genere un FdInfo qui connaitra l offset de depart et la talle du fichier
            # en question et egalement l'offset actuel du fd. Vu que j'ouvre le fichier
            # mon fd en question aura comme current_offset 0.
            fdinfo = FdInfo(handleinfo.start_offset, handleinfo.size)

            # je recupere un fd
            fd = self.get_unallocated_fd()

            if fd == 0:
                # nombre de fd max atteint, je raise une erreur
                raise vfsError("[dumbfs::open] --> number of maximum opened fds reached")

            # j'associe a mon fd ouvert un fdinfo
            self.opened_fds[fd] = fdinfo

            #print "\nallocated fd:", fd, "\nfds opened:\n", self.opened_fds
            # et je retourne le fd attribue
            return fd

        else:
            # le fd n'est pas alloue, je raise une erreur
            raise vfsError("[dumbfs::open] --> handle does not exist")


    def vread(self, fd, buff, size):
        # je verifie que le fd est bien alloue
        if fd in self.opened_fds.keys() and self.opened_fds[fd] != None:
        
            # je recupere les infos du fd
            fdinfo = self.opened_fds[fd]

            # avant de faire quoique ce soit, je verifie que la size n'est pas plus
            # grande que la taille du fichier - l'offset courant.
            real_size = size
            if size > fdinfo.size - fdinfo.current_offset:
                real_size = fdinfo.size - fdinfo.current_offset

            # je positionne mon vfile parent a l offset des datas
            offset_to_go = fdinfo.start_offset + fdinfo.current_offset
            self.parent_file.seek(offset_to_go, 0)

            # je lis de la taille reelle et je recupere le buffer
            buff_read = self.parent_file.read(real_size)

            # je recupere la taille de ce qui a pu etre lu par le driver precedent,
            #celui responsable de self.parent_file
            bytes_read = len(buff_read)

            # je met a jour l'offset courant du fd
            fdinfo.current_offset += bytes_read

            # je retourne ce qui a pu reelement etre lu ainsi que la taille
            return (bytes_read, buff_read)

        else:
            # le fd n'est pas alloue, je raise une erreur
            raise vfsError("[dumbfs::vread] --> fd is not opened")


    def vseek(self, fd, offset, whence):
        # je verifie que le fd est bien alloue
        if fd in self.opened_fds.keys() and self.opened_fds[fd] != None:

            # je recupere les infos du fd
            fdinfo = self.opened_fds[fd]
            
            # aller a offset a partir de 0
            if whence == 0:
                # je verifie que je ne vais pas depasser la taille du fichier !!!
                if fdinfo.size < offset:
                    fdinfo.current_offset = fdinfo.size
                else:
                    fdinfo.current_offset = offset

            # aller a offset actuel + offset
            if whence == 1:
                # je verifie que je ne vais pas depasser la taille du fichier !!!
                if fdinfo.size < fdinfo.current_offset + offset:
                    fdinfo.current_offset = fdinfo.size
                else:
                    fdinfo.current_offset += offset

            # aller a la fin
            if whence == 2:
                fdinfo.current_offset = fdinfo.size

            # je retourne l'offset actuel
            return fdinfo.current_offset

        else:
            # le fd n'est pas alloue, je raise une erreur
            raise vfsError("[dumbfs::seek] --> fd is not opened")


    def vclose(self, fd):
        # je verifie que le fd est bien alloue, et je retourne 0
        if fd in self.opened_fds.keys() and self.opened_fds[fd] != None:
            self.opened_fds[fd] = None
            return 0
        else:
            # le fd n'est pas alloue, je raise une erreur
            raise vfsError("[dumbfs::close] --> fd is not opened")


    def status(self):
        return 0


# ATTENTION, pour le moment le nom de la classe qui herite de Module
# doit se nommer de maniere identique au nom du fichier
class dumbfs(Module):
    def __init__(self):
        # instantiation de la classe heritee
        # param1 --> toujours self
        # param2 --> le nom du module
        # param3 --> a chaque application du module, cette classe sera instanciee
        Module.__init__(self, "dumbfs", DumbFs)

        # prend une string optionnelle en entree qui s'appelle tmp
        self.conf.add("tmp", "string", True)

        # ajout de valeurs predefinies (de type string)
        # pour l argument tmp
        self.conf.add_const("tmp", "ex1")
        self.conf.add_const("tmp", "ex2")

        # prend en entree un argument de type node qui s'appelle dumb_fs
        self.conf.add("parent", "node")

        # Creer une categorie (en console (completion) et en gui (clic droit))
        self.tags = "dumb_fs"
