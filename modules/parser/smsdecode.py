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
#  Solal Jacob <sja@digital-forensic.org>
# 

import struct
import binascii 


from api.vfs import *
from api.module.module import *
from api.module.script import *


class SMS(Script):
   def __init__(self):
      Script.__init__(self, "smsdecode")

   def start(self, args): 
      self.unpack(args)
      if not args.get_bool("header"):
        res = self.info()
      else:
        res = self.header()
      self.res.add_const("result", res) 

   def unpack(self, args):
      self.vfs = vfs.vfs()
      node = args.get_node("file")
      f = node.open()
      buff = f.read()
      f.close()
      off = 0
      self.status = struct.unpack('B', buff[off])
      off += 1
      self.smsc_info_len = struct.unpack('B', buff[off])
      off += 1
      self.smsc_info_type_of_addr = struct.unpack('B', buff[off])
      off += 1
      self.smsc_info_center_number_len = self.smsc_info_len[0] - 1 
      noff = off
      noff += self.smsc_info_center_number_len
      self.smsc_info_center_number_oct = struct.unpack(str(self.smsc_info_center_number_len) + 'B', buff[off:noff])
      off = noff
      if (("%x" % self.smsc_info_type_of_addr) == "91"):
        self.smsc_info_center_number = "+"
      else:
        self.smsc_info_center_number = ""
      for i in self.smsc_info_center_number_oct:
           self.smsc_info_center_number += self.byte_swap(i)
           if i < 10:
             self.smsc_info_center_number += "0"
      self.smsc_info_center_number = self.smsc_info_center_number.strip('f')
      self.sms_deliver_msg_start = struct.unpack('B', buff[off])
      off += 1
      self.sender_number_len_dig = struct.unpack('B', buff[off])
      off += 1
      self.sender_number_type = struct.unpack('B', buff[off])
      off += 1
      self.sender_number_len_oct = self.sender_number_len_dig[0] / 2  
      if self.sender_number_len_dig[0] % 2:
        self.sender_number_len_oct += 1
      noff = off + self.sender_number_len_oct
      self.sender_number_oct = struct.unpack(str(self.sender_number_len_oct) + 'B', buff[off:noff])
      off = noff
      if (("%x" % self.sender_number_type) == "91"):
        self.sender_number = "+"
      else:
        self.sender_number = ""
      for i in self.sender_number_oct:
         self.sender_number +=  self.byte_swap(i)
         if i < 10:
           self.sender_number +="0"
      self.sender_number = self.sender_number.strip('f')
      self.tp_pid = struct.unpack('B', buff[off])
      off += 1
      self.tp_dcs = struct.unpack('B', buff[off])
      off += 1
      noff = off + 7
      self.timestamp = struct.unpack('7B', buff[off:noff])
      off = noff 
      self.tp_udl = struct.unpack('B', buff[off])
      off += 1
      if self.tp_dcs[0]: 
        self.sms_len = self.tp_udl[0]
      else:
        self.sms_len = self.tp_udl[0] - (self.tp_udl[0] / 8) 
      noff = off + self.sms_len
      self.sms_byte = struct.unpack(str(self.sms_len) + 'B', buff[off:noff]) 
      self.sms_buff = self.s7bit_to_ascii(self.sms_byte)
      self.year = self.byte_swap(self.timestamp[0])
      self.month = self.byte_swap(self.timestamp[1])
      self.day = self.byte_swap(self.timestamp[2])
      self.hour = self.byte_swap(self.timestamp[3])
      self.minute = self.byte_swap(self.timestamp[4])
      self.second = self.byte_swap(self.timestamp[5])
      self.gmt  = self.byte_swap(self.timestamp[6])

   def byte_swap(self, buff):
      tmp = "%x" % buff
      if len(tmp) == 1:
        return tmp[0]
      return tmp[1] + tmp[0]

   def tup_hex(self, buff):
      res = ""
      for i in buff:
        res += "%x" % i 
      return res

   def byte_to_bits_string(self, x):
      return "".join(map(lambda y:str((x>>y)&1), range(7, -1, -1))) 

   def bytes_to_bits(self, bytes):
     bits_list = []
     for i in bytes:
       bits_list += self.byte_to_bits_string(i)[::-1]
     return bits_list
   
   def s7bit_to_ascii(self, buff):
     bits_list = self.bytes_to_bits(buff)
     i = 0
     lchar = ""
     while i < len(bits_list):
       x = 6
       bstr = "0"
       while x >= 0:
	 if (x+i) < len(bits_list):
           bstr +=  bits_list[x+i]
           x -= 1
         else:
           return lchar
       i += 7 
       lchar +=  "%c" % int(bstr, 2)
     return lchar

   def header(self):
      h = ""
      h += "Status 0x%x\n" % self.status
      h += "SMSC information, length: %d octets\n" % self.smsc_info_len
      h += "SMSC information, type of address: 0x%x \n" % self.smsc_info_type_of_addr 
      h += "debug SMSC information, center number length: %d octects\n" % self.smsc_info_center_number_len
      h += "SMSC information, center number: " + self.tup_hex(self.smsc_info_center_number_oct) + "\n"
      h += "SMS-Deliver message first octect: 0x%x\n" % self.sms_deliver_msg_start
      h += "Length of the sender number: %d digits\n" % self.sender_number_len_dig
      h += "Length of the sender number: %d octet\n" % self.sender_number_len_oct
      h += "Type of sender number: 0x%x\n" % self.sender_number_type
      h += "Sender number: " + self.tup_hex(self.sender_number_oct) + "\n"
      h += "TP Protocol Identifier: 0x%x\n" % self.tp_pid
      h += "TP Data coding scheme: 0x%x\n" % self.tp_dcs
      h += "Time Stamp: "+ self.tup_hex(self.timestamp) + "\n"
      if self.tp_dcs[0]:
        h += "TP User data length: %d in octect\n" % self.sms_len 
      else:
        h += "TP User data length: %d in septet \n" % self.sms_len 
      h += "SMS buff: " + self.sms_buff + "\n"
      return h

   def info(self):
      i = ""
      if self.status[0] == 0:
        i += "Status: unused\n"
      elif self.status[0] == 1:
        i += "Status: read\n"
      elif self.status[0] == 3:
        i += "Status: unread\n"
      elif self.status[0] == 5:
        i += "Status: send\n"
      elif self.status[0] == 7:
        i += "Status: unsend\n"
      i += "Center number: " + self.smsc_info_center_number + "\n" 
      i += "Sender number: " + self.sender_number + "\n"
      i += "Date :" + self.day + "/" + self.month + "/" + self.year + " " +  self.hour + ":" + self.minute + ":" + self.second + " GMT:" + self.gmt + "\n"
      i += "Message : " + self.sms_buff + "\n"
      return i 

class smsdecode(Module):
  def __init__(self):
    """ A sms decoder
ex: smsdecode /myfile.sms"""
    Module.__init__(self, "smsdecode", SMS)
    self.conf.add("file", "node")
    self.conf.add("header", "bool")
    self.tags = "mobile"
